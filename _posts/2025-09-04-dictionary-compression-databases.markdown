---
layout: post
comments: true
title:  "Dictionary-based compression в СУБД"
date:   2025-09-04 16:21:00 +0000
categories: rabid-transit databases compression
---

Интересный тренд использовать dictionary-based compression в СУБД. Сейчас [это обсуждают в Cassandra mailing list](https://lists.apache.org/thread/pd43rfws7tbgj5zp3wxvsg7lc0y52otv), ранее такую возможность [добавила ScyllaDB](https://docs.scylladb.com/manual/stable/operating-scylla/procedures/config-change/sstable-dictionary-compression.html) в свою коммерческую версию. Наилучший эффект достигается, конечно же, на LSM дереве, т.к. только там мы имеем дело с достаточно большими объёмами в одном sstable и append-only работой с диском, но в целом ничего, кажется, не мешает применять и в B-деревьях. Основная проблема в реализации это создание и поддержка актуальных словарей - это бэкграунд работа, которая не должна влиять на производительность системы в целом. В shared-memory парадигме обеспечить конкурентный быстрый доступ к релевантному словарю может быть непросто. Если словарь утерян, расшифровать файл невозможно, поэтому необходимо обеспечить надёжное хранение словаря. В [ScyllaDB](https://www.scylladb.com/) для этого используется group0 - глобальная Raft группа объединяющая все узлы в кластере. Похожий принцип управления метаданными [реализован и в Picodata](https://docs.picodata.io/picodata/devel/architecture/raft_failover/).
