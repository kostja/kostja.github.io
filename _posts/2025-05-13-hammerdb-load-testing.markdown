---
layout: post
comments: true
title:  "HammerDB и инструменты нагрузочного тестирования"
date:   2025-05-13 19:42:00 +0000
categories: rabid-transit databases benchmarking
---

[HammerDB](https://www.hammerdb.com/document.html) - это не СУБД, а инструмент по нагрузочному тестированию СУБД. Из интересного, он оформлен в готовый продукт, то есть есть даже сборки под MS Windows. Спонсируется это всё, судя по всему, [MariaDB](https://mariadb.org/), а разрабатывает тест бывший performance engineer Intel. Занятная штука с этими инструментами нагрузочного тестирования: каждый performance engineer делает инструмент под себя, потом инженер меняет работу и инструмент уходит в небытие. [sysbench](https://github.com/akopytov/sysbench), [YCSB](https://github.com/brianfrankcooper/YCSB), [cassandra-stress](https://cassandra.apache.org/doc/4.0.0/cassandra/tools/cassandra_stress.html) - сообщество повторяет раз за разом одно и то же. Есть какой-то непостигнутый дзен во всём этом, но как минимум понятно что фаза развёртывания, вид нагрузки и сбор метрик должны быть легко подключаемыми. Мы в Picodata пошли [по пути создания расширения для k6](https://habr.com/ru/companies/arenadata/articles/864974/) и это, похоже, наиболее понятный с точки зрения сопровождения путь.
