---
layout: post
date:      2006-10-27 10:42
title:   utf8 support in MySQL rocks ;)
---

Joke of the day from our character sets ubergod:
<pre>
10:59 < bar> mysql> set names utf8;
10:59 < bar> Query OK, 0 rows affected (0.00 sec)
10:59 < bar> mysql> create table t1 (a text,
10:59 < bar>     -> fulltext index `бесовский` (a))
10:59 < bar>     -> character set utf8;
10:59 < bar> Query OK, 0 rows affected (0.00 sec)
10:59 < bar> mysql> insert into t1 values ('слово божие');
10:59 < bar> Query OK, 1 row affected (0.00 sec)
</pre>
And it just works :)
