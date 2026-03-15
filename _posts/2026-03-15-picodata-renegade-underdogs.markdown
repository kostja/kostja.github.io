---
layout: post
date:    2026-03-15
title:   "Picodata: Shard-Per-Core In-Memory Database"
permalink: /talks/picodata-renegade-underdogs
---

<style>
/* Speaker notes styling */
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
.post-content blockquote strong {
    color: #333;
}
/* Slide separator */
.post-content hr {
    border: none;
    border-top: 2px solid #dee2e6;
    margin: 40px 0;
}
</style>

## 0. Title

![Title](/assets/img/talks/title.svg)

---

## 1. Three database architectures

![Three database architectures](/assets/img/talks/db_architectures.svg)

> There are three major architectures for distributed databases.
> **Shared-storage** (Neon, Aurora) separates compute from storage — compute nodes
> talk to a shared storage layer over the network. **Shared-memory** (PostgreSQL)
> runs multiple workers inside one process, all contending on shared memory
> structures. **Shared-nothing** (Picodata) gives each CPU core its own shard
> of data — no locks, no contention, no shared state. This is the architecture
> Picodata uses.

---

## 2. Shard-per-core: a new architecture trend

Message-passing runtimes that partition work per CPU core:

![Shard-per-core trend](/assets/img/talks/shard_per_core_trend.svg)

> Shard-per-core isn't a Picodata invention — it's a broader industry trend.
> Go's runtime, Tokio in Rust, and Seastar in C++ all use message-passing
> with per-core isolation. ScyllaDB and Redpanda are built on Seastar.
> Picodata applies the same pattern to an in-memory distributed database,
> using Rust and Tokio-style concurrency.

---

## 3. Picodata architecture

- One computer runs **one DB process per CPU core**
- Each process has an independent replica (or replicas)
- Replicas of one process form a **replica set** -
  the unit of cluster scaling

![Architecture: shared-nothing with replication rings](/assets/img/talks/architecture.svg)

> This is a shared-nothing architecture. Each instance runs on a dedicated
> CPU core and owns its data exclusively. Instances form replica sets
> that span failure domains (data centers). Each replica set uses Raft
> for consensus: one leader handles writes, followers provide read
> scaling and fault tolerance.
> Picodata is an **in-memory database** — 100% of data lives in RAM,
> persisted via write-ahead logging. "In-memory" doesn't mean "volatile" —
> RAM is the primary storage tier, not a cache. This lets us use data
> structures optimized for RAM access patterns rather than disk page layouts.

---

## 4. Buckets: unit of data distribution

![Buckets](/assets/img/talks/buckets.svg)

> Data is split into **3 000 buckets** (by default) — fixed-size units of
> distribution and rebalancing. When a new replica set joins the cluster,
> it starts with zero buckets. Rebalancing begins only when the new RS is
> **fully online** — all replicas present, replication factor satisfied.
> Bucket transfer happens **leader to leader**: the source RS master sends
> buckets directly to the destination RS master. Followers learn about the
> new data via regular replication — they never participate in rebalancing
> directly. Drivers cache the bucket→shard map so most queries go directly
> to the right node without an extra hop.

---

## 5. Data distribution

![Data distribution](/assets/img/talks/distribution.svg)

```sql
CREATE TABLE orders (...)    USING MEMTX DISTRIBUTED BY (o_w_id);
CREATE TABLE customer (...)  USING MEMTX DISTRIBUTED BY (c_w_id);
CREATE TABLE warehouse (...) USING MEMTX DISTRIBUTED GLOBALLY;
```

> Tables sharing a distribution key are **co-distributed** — their rows
> land on the same replica set, enabling local joins with no network hops.
> **Global** tables are replicated to every node, ideal for small dimension
> tables (think star schema). Together, these let Picodata execute complex
> joins locally — the key to fast, horizontally scalable OLTP.

---

## 6. Failure domains and tiers

![Cluster tiers](/assets/img/talks/tiers.svg)

> Each **tier** groups instances by purpose and has its own bucket count,
> replication factor, and `can_vote` setting.
> **Hot storage** keeps everything in RAM for microsecond access.
> **Cold storage** uses the LSM engine (Vinyl) for large datasets that
> don't fit in RAM. **Compute** tiers run SQL queries and plugins but
> store no data. **Arbiter** tiers are lightweight voters — they participate
> in Raft elections to provide quorum without storing user data.
> For example, a third DC can host just an arbiter tier — a single small VM
> that gives you quorum for automatic failover without the cost of a full DC.
> The data schema is global, but data and code (plugins) are local to a tier,
> so each tier scales independently.
> All instances across all tiers share a single **Raft ring** that
> maintains global cluster metadata: schema, topology, bucket map,
> users, and ACL.
> **Failure domains** are key-value labels attached to instances (like K8s
> node labels). Picodata uses them to place replicas in different domains
> automatically. Example config: `DC=1, S=2 (servers/DC), NCPU=2
> (instances/server), RF=2`. If a server or DC fails, the system knows
> which replicas are affected and promotes followers in other domains.

---

## 7. Cluster assembly

![Cluster assembly](/assets/img/talks/cluster_assembly.svg)

```
# Start first node
picodata run --data-dir tmp/i1 --listen :3301 \
    --peer :3301 --init-replication-factor 2 \
    --failure-domain '{"dc": "dc1"}'

# Add more nodes
picodata run --data-dir tmp/i2 --listen :3302 --peer :3301
picodata run --data-dir tmp/i3 --listen :3303 --peer :3301
picodata run --data-dir tmp/i4 --listen :3304 --peer :3301

# Remove a node
picodata expel --instance-uuid a022c8f5-...24755e2d5c81
```

> Assembling a cluster is just running the same binary with different
> arguments. The first node bootstraps the cluster, subsequent nodes
> join by pointing to any existing peer. Removing a node is a single
> `expel` command. No configuration management required.

---

## 8. Availability & Scalability: summary

1. **Synchronous disk writes** - durable persistence in sync mode
2. **Synchronous replication** - a full DB copy in 2+ data centers
3. **Logical replication** between clusters (similar to Oracle GoldenGate) -
   an asynchronous live copy for blue/green upgrades and DR

Picodata implements ACID guarantees with **SERIALIZABLE** isolation -
the highest possible level.

The **tier** mechanism separates compute, operational, and archival storage.
Each layer scales independently.

Production numbers: **10,000+ TPS** per core, **2–100 TB** managed data,
up to **2,000+ nodes** in a cluster.

> We provide SERIALIZABLE isolation -- the strongest guarantee in the
> SQL standard. Combined with synchronous replication, this means
> committed transactions are durable across data centers. You don't
> need to choose between consistency and availability for normal operations.
> **2-DC deployment**: leaders distributed evenly across both DCs. If one DC
> fails, the other has all data and continues serving reads. Writes need quorum,
> so a 2-DC setup uses an arbiter tier (a single small VM in a 3rd location).
> **3-DC deployment**: each DC holds a full data copy. A transaction commits when
> written to at least 2 DCs. If any DC fails, the system stays fully operational
> (RTO 0, RPO 0). All DCs are active. Rolling upgrades with zero downtime.

---

## 9. Live demo

<link rel="stylesheet" type="text/css" href="https://unpkg.com/asciinema-player@3.8.0/dist/bundle/asciinema-player.css" />
<div id="demo-player"></div>
<script src="https://unpkg.com/asciinema-player@3.8.0/dist/bundle/asciinema-player.min.js"></script>
<script>
AsciinemaPlayer.create('/assets/img/talks/demo.cast', document.getElementById('demo-player'), {
  theme: 'monokai',
  cols: 90,
  rows: 35,
  idleTimeLimit: 2,
  speed: 1.5,
  fit: 'width'
});
</script>

> Three parts. **Part 1** assembles a 3-node cluster with RF=3 — just
> `picodata run` with `--peer` pointing to the first node.
> **Part 2** creates a user via the admin socket and grants `CREATE TABLE` —
> the only extra privilege needed, since read access to `_pico_*` system
> tables is already public.
> **Part 3** connects with standard `psql` — the SQL is PostgreSQL-compatible,
> `DISTRIBUTED BY` controls sharding, `USING MEMTX` selects the in-memory
> engine. The `_pico_instance` and `_pico_tier` queries show all 3 nodes
> online in one replicaset with RF=3.

---

## 10. PostgreSQL-compatible SQL

![SQL tag cloud](/assets/img/talks/sql_cloud.svg)

PostgreSQL-compatible type system: INTEGER, TEXT/VARCHAR, BOOLEAN,
DOUBLE, DECIMAL, UUID, DATETIME, JSON.

> Picodata implements a broad SQL surface compatible with PostgreSQL syntax
> and types. Queries, joins, CTEs, window functions, subqueries — all work
> as expected. On top of standard SQL we add `DISTRIBUTED BY` and
> `DISTRIBUTED GLOBALLY` to control data placement across the cluster.
> The full reference: [SQL index](https://docs.picodata.io/picodata/stable/reference/sql/).

---

## 11. PostgreSQL wire protocol & tools

![PostgreSQL ecosystem](/assets/img/talks/pg_ecosystem.svg)

> PostgreSQL compatibility means **zero migration friction** — your existing
> tools, ORMs, and BI pipelines work out of the box. DBAs use DBeaver,
> data engineers use Spark, developers use Django or SQLAlchemy.
> For high-throughput OLTP, our **native drivers** (Go, Rust, JDBC) are
> shard-aware and topology-aware — they cache the bucket→shard map and
> route each query directly to the owning node. No proxy, no extra hop.

---

## 12. Ouroboros & blue/green deploy

![Ouroboros](/assets/img/talks/ouroboros.svg)

[Ouroboros manual](https://docs.picodata.io/picodata/25.5/architecture/ouroboros/)

> **Ouroboros** is a proprietary async logical replication engine
> (similar to Oracle GoldenGate). It maintains a second cluster as a
> live copy of production — bootstrap at ~3 Gbit/s (~5 min for 1 TB).
> You test new plugin versions and schema migrations on **real production
> data** with zero impact on production. Once validated, you upgrade
> the production cluster with confidence. Each step is backward-compatible,
> so rollback is always possible.

---

## 13. Co-located compute — why plugins

![Co-located compute](/assets/img/talks/colocated.svg)

- Plugins are **compiled Rust** modules running inside the database process
- No GC pauses, type-safe, shipped as a single binary
- Standard source control, testing, and CI/CD — just a Rust crate

> Traditional architectures put a network boundary between application
> and database — every data access costs ~1 ms. Picodata plugins run
> in the same address space as the data. A hash table lookup in RAM
> takes ~1 μs — that's 1000x faster. This is the key reason plugins
> exist: they bring compute to where data lives.

---

## 14. Plugin lifecycle

![Plugin lifecycle](/assets/img/talks/plugin_lifecycle.svg)

> A plugin is described by a **manifest** (like `package.json`), uses
> **migrations** with UP/DOWN for schema changes (distributed transactions,
> auto-rollback), and is managed entirely via **SQL** (`ALTER PLUGIN`,
> `ALTER SERVICE`). At most 2 versions can coexist in a cluster for
> blue/green upgrades. Configuration is strictly consistent across all nodes.

---

## 15. Use cases

![Use cases](/assets/img/talks/use_cases.svg)

High-throughput OLTP with microsecond latency, ACID, and horizontal scaling.

> **Banking & Finance**: real-time tarification, mobile banking statements,
> fraud detection — top-10 banks in production.
> **Telecom**: unified customer profiles, real-time session management.
> **Government**: visual network analysis for federal authorities,
> document processing pipelines.
> **Manufacturing & IoT**: sensor data ingestion, real-time cost calculation.
> **E-commerce**: inventory and pricing engines, recommendation systems.
> **Gaming & AdTech**: leaderboards, real-time bidding.
> Common thread: high-throughput OLTP that needs microsecond latency,
> ACID guarantees, and horizontal scaling — all in one product.

---

## 16. Thank you & reach out

![Picodata](/assets/img/talks/picodata_logo.png)

![QR code — Telegram channel](/assets/img/talks/qr_telegram.png)

- [@picodataru](https://t.me/picodataru)
- [@kostja_osipov](https://t.me/kostja_osipov)
