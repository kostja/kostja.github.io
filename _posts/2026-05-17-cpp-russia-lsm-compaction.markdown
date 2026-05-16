---
layout: post
date:    2026-05-17
title:   "Compaction в LSM: за пределами Leveled и Tiered"
permalink: /talks/cpp-russia-lsm-compaction
---

<style>
.post-content blockquote {
    font-size: 14px;
    letter-spacing: 0;
    font-style: normal;
    color: #555;
    border-left: 3px solid #4dabf7;
    background: #f8f9fa;
    padding: 10px 15px;
    margin-top: 8px;
}
.post-content blockquote strong { color: #333; }
.post-content hr {
    border: none;
    border-top: 2px solid #dee2e6;
    margin: 40px 0;
}
</style>

## 0. Title

# Compaction в LSM

### За пределами Leveled и Tiered

Константин Осипов — C++ Russia, 17 мая 2026

> Today's topic is LSM compaction — not as a Vinyl-specific subject,
> but as a general design problem any LSM engine faces. I'll use
> Cassandra, RocksDB, and Vinyl as concrete examples, and close with
> a proposal for what the next generation of LSM file formats should
> look like.

---

## 1. LSM на одном слайде

![LSM recap](/assets/img/talks/lsm_recap.svg)

> Quick recap. Writes land in an in-memory memtable. When it fills up,
> it is frozen and flushed to disk as a sorted immutable file — an
> SSTable in Cassandra, an SST in RocksDB, a run-file in Vinyl. Reads
> must consult the memtable and every on-disk file, so over time the
> engine compacts files together: it merges several sorted files into
> one larger sorted file, collapsing updates and dropping tombstones.
> Compaction is where almost all of the engineering happens.

---

## 2. Size-Tiered Compaction (STCS)

![Size-Tiered Compaction](/assets/img/talks/size_tiered_compaction.svg)

- Файлы одного размера складываются в уровень
- При накоплении N (по умолчанию 4) — слияние в один файл
- Результат становится файлом следующего уровня

> STCS is the original Cassandra strategy and the simplest. It keeps
> a stack of size buckets — when enough files of the same size
> accumulate, they get merged and the result starts a new, bigger
> bucket. Write amplification is low because each byte is rewritten
> only when its tier fills.

---

## 3. Когда STCS — правильный выбор

![STCS shines](/assets/img/talks/stcs_workload_shine.svg)

- Поток записи доминирует, чтения редкие
- Низкий write amp — сливаются только файлы одного размера
- Минимальный износ SSD
- Подходит для: audit-логи, event-стримы, CDC-журналы, архивное хранение

> STCS earns its place in workloads where writes dominate and reads
> are rare or batched. Audit logs, event streams, CDC pipelines,
> archival storage — all want low write amp and tolerate high read
> amp because reads are uncommon or do scans rather than point lookups.

---

## 4. Когда STCS подводит

![STCS pain](/assets/img/talks/stcs_workload_pain.svg)

- Версии одного ключа разбросаны по N уровням → read amp растёт
- Major compaction крупнейшего уровня требует диск ≈ 2× датасета
- Классический инцидент: «Cassandra переполнила диск при compaction»

> The trouble surfaces at scale. Imagine a Cassandra cluster ingesting
> metrics — billions of writes per day, keys updated frequently. Each
> key's versions end up scattered across many tiers. To read one row,
> the engine merges fragments from every tier — read amp grows
> unbounded. Worse, the largest tier eventually needs to be compacted
> itself: that operation reads N files of the biggest size class and
> writes one merged file, doubling the disk footprint for the duration.
> If you provisioned for 1× your data, you are out of space and the
> merge fails. This is the canonical "Cassandra ran out of disk"
> outage.

---

## 5. Leveled Compaction (LCS)

![Leveled Compaction](/assets/img/talks/leveled_compaction.svg)

- Файлы организованы по уровням L0, L1, L2, …
- Каждый следующий уровень ≈ ×10 больше предыдущего
- Внутри уровня файлы не пересекаются по диапазону ключей
- Продвижение между уровнями = перезапись затронутого диапазона

> LCS, originally LevelDB's contribution, fixes the read-amp problem.
> Within each level, files cover disjoint key ranges — a point lookup
> consults at most one file per level. Read amplification is bounded
> by the number of levels, roughly log₁₀(dataset). Space amplification
> is also tight because each level holds exactly one copy of its key
> range.

---

## 6. Когда LCS — правильный выбор

![LCS shines](/assets/img/talks/lcs_workload_shine.svg)

- OLTP с горячим набором ключей, точечные чтения по PK
- p99 чтения — продуктовый SLA
- read amp = O(log₁₀ N), space amp ≈ 1.1×
- Подходит для: профили, сессии, корзины, справочники, API-поиск по PK

> LCS shines on read-heavy OLTP: profiles, sessions, shopping carts,
> API lookups by primary key. The bounded read amp and tight space
> amp translate directly into predictable p99 latency, which is what
> the product SLA usually measures. The cost — write amp — is
> acceptable because the workload is read-heavy by definition.

---

## 7. Когда LCS подводит

![LCS pain](/assets/img/talks/lcs_workload_pain.svg)

- 1 байт на L0 → ≈ 30 байт через каскад продвижений
- Износ SSD упирается в DWPD-потолок
- Bulk-ingest проседает: backfill, CDC, IoT, потоковая загрузка

> The cost of bounded read amp is unbounded write amp. To keep levels
> non-overlapping, every promotion rewrites the touched range at the
> next level. With the default 10× ratio, one byte at L0 may be
> rewritten 10× at L1, 10× at L2, and so on. Total write amp is the
> sum: typically 20–30×. For bulk-ingest workloads — backfilling a
> year of metrics, loading a CDC stream, ingesting IoT events — write
> amp is the wall you hit. The SSD wears out, write quota drains,
> sustained throughput collapses to whatever the bottom level can
> absorb.

---

## 8. Треугольник RUM

![RUM trilemma](/assets/img/vinyl/amplification_triangle.svg)

- **Read** amp — байт прочитано на байт запрошенных данных
- **Write** amp — байт записано на байт сохранённых данных
- **Space** amp — байт на диске на байт живых данных

> Harvard's DASlab framed it crisply: you cannot minimize all three.
> STCS optimizes write amp at the cost of read and space. LCS
> optimizes read and space at the cost of write. Every strategy is a
> point in this triangle — and the right point depends on the
> workload, not on a universal answer.

---

## 9. Universal Compaction — компромисс

![Universal Compaction](/assets/img/talks/universal_compaction.svg)

- Cassandra **UCS** (5.0) и RocksDB **Universal** объединяют STCS и LCS
- Параметр `scaling_parameter` (W) задаёт поведение каждого уровня
- Адаптируется к нагрузке — но остаётся компромиссом

> Cassandra and RocksDB converged on the same idea: parameterize the
> strategy. UCS gives each level a knob — negative W behaves like
> tiered, positive like leveled. You can tune it, but tuning assumes
> you know the workload, that it doesn't change, and that one knob
> is enough to describe it. In practice these assumptions are wrong,
> and even a well-tuned UCS leaves performance on the table compared
> to a strategy that observes the workload at runtime.

---

## 10. Vinyl — per-range, shape-based

![Slices and ranges](/assets/img/vinyl/slices_and_ranges.svg)

![Shape-based compaction](/assets/img/vinyl/shape_based_compaction.svg)

- Ключевое пространство разбито на независимые диапазоны (по умолчанию 128 МБ)
- У каждого диапазона своя «форма» LSM-дерева — пирамида run-файлов
- Run-файл может быть виден из нескольких диапазонов через slice-ссылки

> Vinyl partitions the keyspace into ranges, each its own mini-LSM
> with its own shape and compaction decisions. Range size bounds the
> worst-case compaction cost: a major compaction of one 128 MB range
> needs only 128 MB of temporary space, no matter how big the dataset.
> Run-files can be shared across ranges via slices — a slice is a
> (file, start_page, end_page) tuple. A range split creates new
> slices, not new files.

---

## 11. Bloat временны́х рядов после split-а

![Time-series bloat](/assets/img/vinyl/timeseries_bloat.svg)

- Append-only вставки, затем split диапазона
- Нижняя половинка выглядит «идеально» — один большой run-файл
- Но 50% его данных уже устарели: page-index сидит в RAM зря
- Удаление старых строк деградирует в квадратику

> The exact bug that triggered our scheduler rewrite. Time-series data
> appended in key order; the range grew past its threshold, split,
> and the lower half — never written to again — looked perfect to the
> shape-based scheduler. But half of its bytes were dead, copied
> across during the split. The page index sat in RAM for nothing.
> Worse, a delete-old scan from the cold end triggered quadratic
> behavior — each scan re-read all the tombstones the previous scans
> had created.

---

## 12. Усечение плана — сливаем только пересекающееся

![Overlapping cluster](/assets/img/vinyl/overlapping_cluster.svg)

- Внутри диапазона ищем максимальный кластер run-файлов с пересекающимися ключами
- Сливаем только этот кластер
- Непересекающиеся run-файлы пропускаем — write amp экономится

> The fix: don't take the shape at face value. Within a range, find
> the maximal cluster of run-files that actually share key ranges,
> compact only that cluster. Non-overlapping runs — common in
> time-series, append-only, tenant-isolated workloads — get skipped
> entirely. The change required making the compaction *plan* a
> first-class object in the scheduler. Once you have a plan, you can
> have multiple drivers competing to fill it.

---

## 13. Read-amp драйвер — замыкаем цикл

- Считаем mux на чтении: полезные байты ÷ просканированные байты
- Mux упал ниже порога — планируем compaction для этого диапазона
- Чтения сами говорят compaction-у, что делать

> The second driver is feedback from reads. The shape-based driver
> looks at the file layout; the read-amp driver looks at what queries
> actually pay. When read efficiency drops — too many tombstones,
> too much dead data after a split — we compact the range even if
> its shape looks fine. This closes the feedback loop classical LSM
> schedulers lack. It also gracefully handles workloads the engine
> has no model for: if reads suffer, compaction kicks in.

---

## 14. File stitching — что нам даёт ФС

![File stitching](/assets/img/talks/file_stitching.svg)

- Linux: ioctl `FICLONERANGE`, syscall `copy_file_range`
- ФС с reflink: btrfs, XFS, ZFS, APFS
- Сращивание фрагмента файла в другой файл без копирования байт
- Результирующие файлы делят физические экстенты, пока их не перезаписать

> Modern filesystems splice file fragments by reference. btrfs and XFS
> expose this as reflink copies; the Linux kernel offers FICLONERANGE
> and copy_file_range. Two files share the same physical blocks until
> one of them is modified — then copy-on-write kicks in. For an LSM
> engine this is enormously tempting: instead of physically rewriting
> megabytes during a merge, splice existing data pages into the new
> run-file at near-zero I/O cost.

---

## 15. Когда stitching помогает *несмотря на* усечение плана

![Stitching workload](/assets/img/talks/stitching_workload.svg)

- Два run-файла в одном кластере пересечений
- Пересечение — на 10% ключей (например, k–l)
- Остальные 90% независимы — кандидат на reflink
- Нагрузки: out-of-order backfill, миграция схемы, пакетные корректировки, запоздавшие CDC

> Plan trimming excludes run-files that don't overlap at all. But
> within a single overlapping cluster, two files often share keys
> only on a narrow band. Out-of-order backfills land mostly in new
> regions, touching a few old ones. Schema migrations rewrite a
> column across the keyspace, touching every old run on a small
> subset of pages. Batch corrections rewrite specific transactions.
> In all of these, plan trimming says "compact these two files" —
> but 90% of the bytes don't need to move. Stitching is the natural
> answer: merge the narrow overlap conventionally, reflink the rest.

---

## 16. Ловушка bloom-фильтра

- На SSTable / run-файл — **один** bloom-фильтр на весь набор ключей
- У сшитого файла другой набор ключей — фильтр инвалидирован
- Пересборка фильтра требует читать все ключи — экономия I/O аннулирована
- Та же проблема с page-index, min/max и MinHash-скетчем

> Here's why naïve stitching doesn't work. A bloom filter is computed
> once when the file is written, and is a function of the file's exact
> key set. Stitch two fragments together and the resulting file has
> a new key set — the old filters are invalid. To rebuild them you
> must read every key from every fragment, which means reading every
> page — exactly the I/O cost you were trying to skip. The same holds
> for the page index, key min/max, and any other per-file metadata.
> *The file-level granularity of metadata is the obstacle.*

---

## 17. Трёхуровневая структура — run › block › page

![Three-level format](/assets/img/talks/three_level_format.svg)

- **Run-файл** — SSTable, принадлежит уровню LSM
- **Блок** — 50–100 страниц, новый промежуточный уровень
- **Page** — единица I/O (4–8 КБ)
- У каждого **блока** свои метаданные: key min/max, ttl min/max, bloom, MinHash

> The proposal. Today's LSM files are two-level: pages and the file.
> Page-level metadata is too granular for compaction planning;
> file-level metadata is too coarse for stitching. Insert a third
> level between them: a block of 50–100 pages, with its own filter,
> key range, TTL bounds, MinHash sketch. The block is the smallest
> unit the scheduler reasons about, and the smallest unit that can
> be stitched without rebuilding metadata. The block directory stays
> small enough to live in RAM; the blocks themselves are paged in on
> demand.

---

## 18. Что даёт per-block метаданные

![Per-block workload](/assets/img/talks/block_workload.svg)

- **TTL drop** — блок целиком expire без слияния
- **MinHash skip** — планировщик доказывает, что блоки почти не пересекаются, и пропускает слияние
- **Per-block fuse8** — фильтр переживает stitching, пересборка не нужна
- **Меньше RAM** — каталог блоков на терабайте занимает десятки МБ

> Concretely: multi-tenant SaaS with per-tenant TTL gets free
> expiration — when every key in a block has expired, drop the block
> without reading it. MinHash sketches let the scheduler compute
> Jaccard similarity in O(1) between two blocks; if it's near zero,
> skip the merge. The fuse8 filter at block granularity survives any
> stitching, because stitching moves whole blocks. And the catalog
> of block metadata for a terabyte dataset is tens of megabytes,
> not hundreds.

---

## 19. Почему это будущее OLTP LSM

- Per-file метаданные — наследие эпохи до reflink
- Per-block метаданные включают stitching, TTL drop, MinHash pruning одной структурой
- Уже релизится в **Picodata Vinyl 2.11.8** как формат `.index2`
- Следующий шаг для RocksDB, Cassandra, ScyllaDB — если они захотят сломать формат на диске

> File-level metadata made sense when the only way to move data was
> to copy it. Reflinks change the economics: the unit of data
> movement is now decoupled from the unit of metadata ownership.
> Any serious OLTP LSM engine will eventually need the three-level
> layout. We're shipping it in Picodata Vinyl as the .index2 format —
> backwards compatible, automatic upgrade, opt-out by deleting
> .index2 files and restarting with --force-recovery. I expect
> RocksDB and ScyllaDB to follow within a few years.

---

## 20. Спасибо

- Блог: [kostja.github.io](https://kostja.github.io)
- Telegram: [@kostja_osipov](https://t.me/kostja_osipov)
- Профильные чаты: [@picodataru](https://t.me/picodataru), [@tarantoolru](https://t.me/tarantoolru), [@databaseinternalschat](https://t.me/databaseinternalschat)
- Подробнее: [Как мы пересобрали сборку мусора в Vinyl](/tarantool/vinyl/2026/03/11/vinyl-compaction-scheduler.html)

> Questions welcome — on stage, in the hallway, or in the chats above.
> Everything described is open source. Vinyl ships with Picodata; the
> new scheduler is in 2.11.8 and Picodata 26.1.
