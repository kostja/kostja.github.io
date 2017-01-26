---
layout: post
date:      2007-07-11 02:38
title:   SHOW CREATE TRIGGGER, Bug#26141, Bug#24989
---

<a href="https://dev.mysql.com/doc/refman/5.7/en/show-create-trigger.html">SHOW
CREATE TRIGGER</a> was added two weeks ago into 5.1 branch - it turned out
there is no way to do mysqlbackup without this statement when the trigger is
defined in a character set that is not UTF-8.

And while we are on triggers, some most painful locking bugs with triggers
are being fixed too (in 5.0) - <a href="http://bugs.mysql.com/26141/">Bug#26141 mixing table types in trigger
causes full table lock on innodb table</a> and <a href="http://bugs.mysql.com/24989">Bug#24989 'Explicit or implicit commit'
error/server crash with concurrent transactions</a>. With these two fixes
in, triggers should actually become usable with InnoDB.
