---
layout: post
date:    2026-05-17
title:   "Advanced LSM Compaction"
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

# Advanced LSM Compaction

### Beyond Leveled vs. Tiered

Konstantin Osipov — C++ Russia, 2026

> Today I want to talk about LSM compaction — not as a Vinyl-specific
> topic, but as a general design problem that any LSM engine faces.
> I'll use Cassandra, RocksDB, and Vinyl as concrete examples, and
> close with a proposal for what the next generation of LSM file
> formats should look like.

---

## 1. LSM in one slide

![LSM recap](/assets/img/talks/lsm_recap.svg)

> Quick recap. Writes land in an in-memory **memtable**. When it fills
> up, it's frozen and **flushed** to disk as a sorted immutable file —
> Cassandra calls it an SSTable, RocksDB calls it an SST, Vinyl calls
> it a run-file. Reads must consult the memtable and every on-disk
> file, so over time the system **compacts** files together: it merges
> several sorted files into one larger sorted file, collapsing updates
> and dropping tombstones. *Compaction* is where almost all of the
> engineering happens.

---

## 2. Size-Tiered Compaction (STCS)

![Size-Tiered Compaction](/assets/img/talks/size_tiered_compaction.svg)

- Group files of **similar size** into tiers
- When a tier has **N** files (default 4), merge them into one
- The result joins the next-larger tier

> STCS is the original Cassandra strategy and the simplest one. It
> just keeps a stack of size buckets. When enough files of roughly
> the same size accumulate, they get merged and the result starts a
> new, bigger bucket. Write amplification is low — each byte is
> rewritten only when its tier fills. Conceptually beautiful.

---

## 3. STCS in production — when it hurts

![STCS workload pain](/assets/img/talks/stcs_workload_pain.svg)

- **Time-series ingest** at high write rate produces many tiers
- One key's history is **scattered across N tiers** — read amp blows up
- **Major compaction** of the largest tier needs disk = 2× dataset
- Cassandra outages routinely traced to "ran out of disk during compaction"

> The trouble starts at scale. Imagine a Cassandra cluster ingesting
> metrics or sensor data — billions of writes per day. Each key gets
> updated frequently, and its versions end up scattered across many
> tiers. To read one row, the engine must merge fragments from every
> tier — read amplification grows unbounded. Worse, the largest tier
> eventually needs to be compacted itself. That compaction reads N
> files of the *biggest* size class and writes one merged file —
> doubling the disk footprint for the duration. If you provisioned
> for 1× your data, you're now out of space, and the merge fails.
> This is the canonical "Cassandra ran out of disk" outage.

---

## 4. Leveled Compaction (LCS)

![Leveled Compaction](/assets/img/talks/leveled_compaction.svg)

- Files organized into **levels** L0, L1, L2, …
- Each level is ~10× the size of the previous
- Within a level, files **do not overlap** by key range
- New files at L0 get promoted by merging into L1, then L2, …

> LCS, originally LevelDB's contribution, fixes the read-amp problem.
> Within each level, files cover disjoint key ranges — so a point
> lookup only needs to consult *one* file per level. Read amplification
> is bounded by the number of levels — log₁₀(dataset). Space
> amplification is also tight, because each level holds exactly one
> copy of its key range.

---

## 5. LCS in production — when it hurts

![LCS workload pain](/assets/img/talks/lcs_workload_pain.svg)

- **Bulk ingest** (backfill, IoT pipelines, batch loaders)
- One byte at L0 cascades through every level → ~**30× write amp**
- SSD wear becomes the hard ceiling — not CPU, not network
- Sustained write throughput collapses once levels are full

> The cost of bounded read amp is unbounded write amp. To keep
> levels non-overlapping, every file promotion rewrites the touched
> range at the next level. With the default 10× ratio, one byte
> written to L0 may be rewritten 10 times at L1, 10 at L2, and so on.
> Total write amplification is the sum: 10 + 10 + 10 + … = O(levels).
> Typical numbers are 20–30×. For bulk-ingest workloads — backfilling
> a year of metrics, loading a CDC stream — write amp is the wall you
> hit. The SSD wears out, the write quota drains, and sustained
> throughput collapses to whatever the bottom level can absorb.

---

## 6. The RUM trilemma

![RUM trilemma](/assets/img/vinyl/amplification_triangle.svg)

- **Read** amp — bytes read per byte requested
- **Write** amp — bytes written per byte stored
- **Space** amp — bytes on disk per byte of live data

> Harvard's DASlab framed it crisply: you cannot minimize all three.
> STCS optimizes write amp, sacrifices read and space. LCS optimizes
> read and space, sacrifices write. Every compaction strategy is a
> point in this triangle — and the right point depends on your
> workload, not on a universal answer.

---

## 7. Universal Compaction — the compromise

![Universal Compaction](/assets/img/talks/universal_compaction.svg)

- Cassandra **UCS** (5.0) and RocksDB **Universal** unify STCS and LCS
- A single `scaling_parameter` (W) tunes each level between tiered and leveled
- Adapts to workload — but is still a compromise

> Both Cassandra and RocksDB converged on the same idea: parameterize
> the strategy. UCS gives each level a knob — negative W behaves like
> tiered, positive like leveled, zero is somewhere in between. You
> can tune it. But "tuning" assumes you know your workload, that it
> doesn't change, and that one knob is enough to describe it. In
> practice these assumptions are wrong, and even a well-tuned UCS
> leaves performance on the table compared to a strategy that
> *observes* the workload at runtime.

---

## 8. Vinyl — per-range shape-based

![Slices and ranges](/assets/img/vinyl/slices_and_ranges.svg)

![Shape-based compaction](/assets/img/vinyl/shape_based_compaction.svg)

- Key space split into independent **ranges** (default 128 MB)
- Each range maintains its own LSM **shape** — pyramid of run-files
- A run-file may be referenced from many ranges via **slices**

> Vinyl partitions the keyspace into ranges. Each range is its own
> mini-LSM with its own shape — independent compaction decisions per
> region of the keyspace. Range size bounds the worst-case compaction
> cost: a major compaction of one 128 MB range needs only 128 MB of
> temporary space, no matter how big the dataset.
> Run-files can be shared across ranges via slices — a slice is a
> `(file, start_page, end_page)` tuple. A range split creates new
> slices, not new files.

---

## 9. Per-range randomization — avoiding the stampede

![Randomization](/assets/img/vinyl/randomization.svg)

- 1000 ranges, all flushed together, all hit the threshold together
- Naïve scheduler triggers 1000 simultaneous merges — throughput collapses
- Vinyl **randomizes** the per-range trigger to spread merges over time

> A subtle trap. If every range follows the same canonical shape,
> every range reaches its compaction threshold at the same time —
> right after a memtable flush. The scheduler tries to merge all 1000
> ranges at once, write bandwidth saturates, the next flush is
> blocked, memory fills up, transactions stall. Cassandra and RocksDB
> hit variants of this regularly. Vinyl injects per-range randomness
> into the shape — after a few cycles, merge work is evenly spread.

---

## 10. When shape isn't enough — time-series bloat

![Time-series bloat](/assets/img/vinyl/timeseries_bloat.svg)

- Append-only data, then a range **split**
- The lower half looks "ideal" — one big run-file
- But that file holds 50% **dead** data, sitting in RAM and on disk
- Delete-old scan turns **quadratic** as tombstones accumulate

> The exact bug that triggered our scheduler rewrite. Time-series
> data appended in key order. The range grew past its size threshold,
> split, and the lower half — never written to again — looked perfect
> to the shape-based scheduler. But half of its bytes were already
> dead, copied across during the split. The page index sat in RAM
> for nothing. Worse, a delete-old scan from the cold end of the
> data triggered quadratic behavior, because each scan re-read all
> the tombstones the previous scans had created.

---

## 11. Plan trimming — only merge what overlaps

![Overlapping cluster](/assets/img/vinyl/overlapping_cluster.svg)

- Inside one range, find the largest **cluster of run-files that overlap by key**
- Compact only that cluster
- Non-overlapping run-files are left alone — write amp avoided

> The fix: don't take the shape at face value. Within a range, find
> the maximal cluster of run-files that actually share key ranges,
> and compact only that cluster. Non-overlapping runs — common in
> time-series, append-only, and tenant-isolated workloads — get
> skipped entirely. Conceptually simple, but it required making the
> compaction *plan* a first-class object in the scheduler. Once you
> have a plan, you can have multiple drivers competing to fill it.

---

## 12. Read-amp driver — close the loop

- Track **mux** at read time: useful bytes / scanned bytes
- When mux drops below a threshold, **schedule compaction** for that range
- Reads tell compaction what to do — no more guessing from shape alone

> The second driver is feedback from reads. The shape-based driver
> looks at the file layout; the read-amp driver looks at what queries
> are actually paying. When a range's read efficiency drops — too
> many tombstones, too much dead data after a split — we compact it,
> even if the shape looks fine. This closes the feedback loop that
> classical LSM schedulers lack. It also gracefully handles workloads
> the engine has no model for: if reads suffer, compaction kicks in.

---

## 13. File stitching — what the filesystem offers

![File stitching](/assets/img/talks/file_stitching.svg)

- Linux: `FICLONERANGE` ioctl, `copy_file_range()` syscall
- Filesystems: **btrfs**, **XFS** (with reflinks), ZFS, APFS
- Splice a range of one file into another **without copying bytes**
- The result shares physical extents until either side is overwritten

> Modern filesystems can splice file fragments by reference. btrfs
> and XFS expose this as reflink copies. The Linux kernel offers
> `FICLONERANGE` and `copy_file_range`. Two files share the same
> physical blocks until one of them is modified — then copy-on-write
> kicks in. For an LSM engine, this is enormously tempting: instead
> of physically rewriting megabytes during a merge, splice the
> existing data pages into the new run-file at near-zero I/O cost.

---

## 14. When stitching pays *despite* plan trimming

![Stitching workload](/assets/img/talks/stitching_workload.svg)

- Two run-files in the same overlapping cluster
- They overlap on **10%** of keys (recent updates)
- The other **90%** is independent — perfect candidate for stitching
- Workloads: out-of-order backfill, schema migrations, batch corrections

> Plan trimming excludes run-files that don't overlap *at all*. But
> within a single overlapping cluster, two files often share keys
> only on a narrow band. Out-of-order backfills land mostly in new
> regions but touch a few old ones. Schema migrations rewrite a
> column across the keyspace, touching every old run on a small
> subset of pages. Batch corrections rewrite specific transactions.
> In all of these, plan trimming says "compact these two files" —
> but 90% of the bytes don't need to move. Stitching is the natural
> answer: merge the narrow overlap conventionally, reflink the rest.

---

## 15. The bloom-filter trap

- Each SSTable / run-file has **one bloom filter** for its entire key set
- Stitched output has a different key set — the old filter is wrong
- To build a new filter you must **scan every key** — defeating the optimization
- The same problem hits the page index, min/max stats, MinHash sketches

> Here's why naïve stitching doesn't work. A bloom filter is computed
> once when the file is written, and it's a function of the file's
> exact key set. Stitch two fragments together and the resulting
> file has a new key set — the old filters are invalid. To rebuild
> them you must read every key out of every fragment, which means
> reading every page, which is exactly the I/O cost you were trying
> to skip. The same holds for the page index, the key min/max stats,
> and any other per-file metadata. *The file-level granularity of
> metadata is the obstacle.*

---

## 16. Three-level layout — run › block › page

![Three-level format](/assets/img/talks/three_level_format.svg)

- **Run-file** — the SSTable, logically owned by an LSM level
- **Block** — 50–100 pages, the new intermediate unit
- **Page** — the physical I/O unit (4–8 KB)
- Each **block** owns its own metadata: key min/max, ttl min/max, bloom filter, MinHash sketch

> The proposal. Today's LSM files are two-level: pages and the file.
> Page-level metadata is too granular to be useful for compaction
> planning; file-level metadata is too coarse for stitching. Insert
> a third level between them: a *block* of 50–100 pages, with its
> own filter, its own key range, its own TTL bounds, its own MinHash
> sketch. The block is the smallest unit the scheduler reasons about,
> and the smallest unit that can be stitched without rebuilding
> metadata. The directory of block metadata stays small enough to
> live in RAM; the blocks themselves are paged in on demand.

---

## 17. What per-block metadata unlocks

![Block-level workload](/assets/img/talks/block_workload.svg)

- **Per-block TTL drop** — expire whole blocks without merging
- **MinHash skip** — scheduler proves two blocks barely overlap, skips the merge
- **Per-block fuse8 filter** — survives stitching; no rebuild needed
- **Smaller in-RAM index** — catalog of blocks fits where the page index didn't

> Concretely: multi-tenant SaaS with per-tenant TTL gets free
> expiration — when every key in a block has expired, drop the block
> without reading it. MinHash sketches let the scheduler compute
> Jaccard similarity in O(1) between two blocks; if it's near zero,
> skip the merge — they're not really overlapping. The fuse8 filter
> at block granularity survives any stitching operation, because
> stitching moves whole blocks. And the catalog of block metadata
> for a terabyte dataset is tens of megabytes, not hundreds — the
> rest paged in through a small cache.

---

## 18. Why this is the future of OLTP LSM

- File-level metadata is a **legacy of the pre-reflink era**
- Block-granular metadata enables **stitching, TTL drop, merge pruning** in one design
- Already shipping in **Picodata Vinyl 2.11.8** as the `.index2` format
- The next step for RocksDB, Cassandra, ScyllaDB, and anyone else willing to break their on-disk format

> File-level metadata made sense when the only way to move data was
> to copy it. Reflinks change the economics: now the unit of *data*
> movement is decoupled from the unit of *metadata* ownership. Any
> serious OLTP LSM engine will eventually need the three-level
> layout. We're shipping it in Picodata Vinyl as the `.index2`
> format — backwards compatible, automatic upgrade, opt-out by
> deleting `.index2` files and restarting with `--force-recovery`.
> I expect RocksDB and ScyllaDB to follow within a few years.

---

## 19. Thank you

- Blog: [kostja.github.io](https://kostja.github.io)
- Telegram: [@kostja_osipov](https://t.me/kostja_osipov)
- Project chats: [@picodataru](https://t.me/picodataru), [@tarantoolru](https://t.me/tarantoolru), [@databaseinternalschat](https://t.me/databaseinternalschat)
- Full article: [Как мы пересобрали сборку мусора в Vinyl](/tarantool/vinyl/2026/03/11/vinyl-compaction-scheduler.html)

> Questions welcome — on stage, in the hallway, or in the chats
> above. Everything I described is open source. Vinyl ships with
> Picodata; the new scheduler is in 2.11.8 and Picodata 26.1.
