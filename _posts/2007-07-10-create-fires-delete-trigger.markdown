---
layout: post
date:      2007-07-10 11:34
title:   CREATE TABLE t1 may fire an AFTER DELETE trigger on table t2
---

Nothing is impossible.
Here is the trick:

    drop table if exists t1, t1_op_log;

    create table t1 (id int primary key auto_increment, operation varchar(255));
    -- not that one

    create table t1_op_log(operation varchar(255));

    create trigger trg_t1_ad after delete on t1
    for each row 
      insert into t1_op_log (operation)  values (concat("After DELETE, old=", old.operation));

    insert into t1 (operation) values ("INSERT");

    set @id=last_insert_id();

    create table if not exists t1 replace
    select @id, "CREATE TABLE ... REPLACE SELECT, deleting a duplicate key";

-- voila

    select * from t1_op_log;

Update: this works even if t1 is a view.
