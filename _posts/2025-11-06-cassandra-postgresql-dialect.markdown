---
layout: post
comments: true
title:  "Диалект PostgreSQL в Cassandra?"
date:   2025-11-06 17:33:00 +0000
categories: rabid-transit databases cassandra postgresql
---

Крайне любопытный [тред в Cassandra mailing list](https://lists.apache.org/thread/f1q2pfpglp6d49ysoy2bvq1f5vh9bod5) о том, не реализовать ли в [Cassandra](https://cassandra.apache.org/) поддержку диалекта [PostgreSQL](https://www.postgresql.org/). Диалект PostgreSQL пожирает мир баз данных с невероятной скоростью: если только вы не делаете что-то совсем своё, как [TigerGraph](https://www.tigergraph.com/) или [Memgraph](https://memgraph.com/), то вы выбираете диалект PostgreSQL. Для сообщества Cassandra это вдвойне любопытно, т.к. Cassandra, по моему мнению, реализует один из самых чудовищных диалектов SQL, и тема поднимается не первый раз. В предыдущие разы ответ был неизменно - для AP базы данных нужен AP синтаксис. Видимо поддержка транзакций многое в сообществе Cassandra, которое в целом в последние пару лет переживает ренессанс, поменяла.
