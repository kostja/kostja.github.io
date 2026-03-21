---
layout: post
comments: true
title:  "Генерация тестовых данных"
date:   2025-05-14 20:03:00 +0000
categories: rabid-transit databases testing
---

Генерация правдоподобных тестовых данных - ключевой аспект нагрузочного тестирования, результатам которого можно доверять. Стартап [shadowtraffic.io](https://shadowtraffic.io/) делает это для Kafka, PostgreSQL, и других популярных СУБД. В [cassandra-stress](https://cassandra.apache.org/doc/4.0.0/cassandra/tools/cassandra_stress.html), например, вы можете задать тип, размер и распределение тестовых данных, вот так:

```yaml
columnspec:
  - name: username
    size: uniform(10..30)
  - name: first_name
    size: fixed(16)
  - name: last_name
    size: uniform(1..32)
  - name: password
    size: fixed(80) # sha-512
  - name: email
    size: uniform(16..50)
  - name: startdate
    cluster: uniform(20...40)
  - name: description
    size: gaussian(100...500)
```

Это удобно для целого ряда тестов, но не эмулирует продакшн данных, например в тестах на качество компрессии. В shadowtraffic вы в конфиге можете указать сущность предметной области, например вот так:

```json
"name": {
    "_gen": "string",
    "expr": "#{Name.full_name}"
}
```

Подход требует потенциально тяжёлых доменных словарей (имена, фамилии, адреса и т.д.) и реализован как сервис. Но сэмпл данных предостаточно в открытых дата сетах, только вот большинство инструментов нагрузочного тестирования их не используют.
