---
layout: post
date:      2010-02-18 16:05
title:   Bug#989 is in. Again.
--- 

<a href="http://blogs.mysql.com/peterg/2009/04/01/progress-report-march-2009/">The infamous Bug#989</a> was pushed into the trunk.

This marks an end of an important project that I personally and the runtime team spent eons of time on.

Why do I say we pushed it "again"? The fix, which is comprised by three worklogs, was initially pushed into 6.0 tree.
Yeah, an intended basis for the next GA.
But 6.0 received a bunch of alpha code, which, worse yet, was since then abandoned by its authors.

Just taking 200 changesets out, stabilizing them in a 5.1 based clone, and re-merging/integrating with the remaining stable features that were added to the trunk took 2 months. Thanks to brilliant 6.0 planning and the turbulent times...

But we didn't just do that. Thanks to MySQL's internal QA, and the time that the patch sat in a public tree, we were able to identify a lot of collateral problems, regressions, nice-to-haves,
and get them solved.

I'm sure such a significant change will not affect everyone positively. But at the same time, I'm looking forward to what it enables us to do in the future: higher scalability,
a more transparent architecture, flexibility to extend the system.

Today I'm cautiously proud to list all the tasks that have been completed:

<a href="http://forge.mysql.com/worklog/task.php?id=3726">WL#3726 "DDL locking for all metadata objects"</a>
<a href="http://forge.mysql.com/worklog/task.php?id=4284">WL#4284 "Transactional DDL locking"</a>
<a href="http://forge.mysql.com/worklog/task.php?id=4144">WL#4144 "Lock MERGE engine children"</a>

<a href="http://bugs.mysql.com/989">Bug#989 "If DROP TABLE while there's an active transaction, wrong binlog order"</a>
<a href="http://bugs.mysql.com/25144">Bug#25144 "replication / binlog with view breaks"</a>
<a href="http://bugs.mysql.com/39675">Bug#39675 rename tables on innodb tables with pending transactions causes slave data issue"

<a href="http://bugs.mysql.com/30977">Bug#30977 "Concurrent statement using stored function and DROP FUNCTION breaks SBR"</a>
<a href="http://bugs.mysql.com/37346">Bug#37346 "innodb does not detect deadlock between update and alter table"</a>
<a href="http://bugs.mysql.com/45225">Bug#45225 "Locking: hang if drop table with no timeout"</a>
<a href="http://bugs.mysql.com/46224">Bug#46224 "HANDLER statements within a transaction might lead to deadlocks"</a>
<a href="http://bugs.mysql.com/41804">Bug#41804 "purge stored procedure cache causes mysterious hang for many minutes"</a>
<a href="http://bugs.mysql.com/26141">Bug#26141 "mixing table types in trigger causes full table lock on innodb table"</a>
<a href="http://bugs.mysql.com/43685">Bug#43685 "Lock table affects other non-related tables"</a>
<a href="http://bugs.mysql.com/22876">Bug#22876 "Four-way deadlock"</a>
<a href="http://bugs.mysql.com/44613">Bug#44613 "SELECT statement inside FUNCTION takes a shared lock"</a>
<a href="http://bugs.mysql.com/33948">Bug#33948 "performance issue when using sysbench benchmark on a multiple-core system."

<lj-cut text="A long list of bugs found by our remarkable QA enginers">
These are bugs that our QA engineers found and we fixed before the push:

<a href="http://bugs.mysql.com/40181">Bug#40181 "Partitions: hang if create index</a>
<a href="http://bugs.mysql.com/43867">Bug#43867 "ALTER TABLE on a partitioned table causes unnecessary deadlocks</a>

<a href="http://bugs.mysql.com/43272">Bug#43272 "HANDLER SQL command does not work under LOCK TABLES"</a>

<a href="http://bugs.mysql.com/46272">Bug#46272 "New MDL: unnecessary deadlock"</a>
<a href="http://bugs.mysql.com/46654">Bug#46654 "False deadlock on concurrent DML/DDL with partitions, inconsistent behavior"</a>
<a href="http://bugs.mysql.com/48541">Bug#48541 "Deadlock between LOCK_open and LOCK_mdl (was deadlock with LOCK_thread_count)"</a>
<a href="http://bugs.mysql.com/42862">Bug#42862 "Crash on failed attempt to open a children of a merge table"</a>
<a href="http://bugs.mysql.com/46273">Bug#46273 "New MDL: Bug#989 is not fully fixed in case of ALTER"</a>
<a href="http://bugs.mysql.com/50913">Bug#50913 "Deadlock between open_and_lock_tables_derived and MDL"</a>
<a href="http://bugs.mysql.com/45949">Bug#45949 "Assertion `!tables->table' in open_tables() on ALTER + INSERT DELAYED"</a>
<a href="http://bugs.mysql.com/47635">Bug#47635 "assert in start_waiting_global_read_lock during CREATE VIEW"</a>
<a href="http://bugs.mysql.com/46452">Bug#46452 "Crash in MDL, HANDLER OPEN + TRUNCATE TABLE"</a>
<a href="http://bugs.mysql.com/46495">Bug#46495 "Crash in reload_acl_and_cache on SIGHUP"</a>
<a href="http://bugs.mysql.com/50821">Bug#50821 "Deadlock between LOCK TABLES and ALTER TABLE"</a>
<a href="http://bugs.mysql.com/51136">Bug#51136 "Crash in pthread_rwlock_rdlock on TEMPORARY + HANDLER + LOCK + SP"</a>
<a href="http://bugs.mysql.com/50907">Bug#50907 "Assertion `hash_tables->table->next == __null' on HANDLER OPEN"</a>
<a href="http://bugs.mysql.com/50908">Bug#50908 "Assertion `handler_tables_hash.records == 0' failed in enter_locked_tables_mode"</a>
<a href="http://bugs.mysql.com/51134">Bug#51134 "Crash in MDL_lock::destroy on a concurrent DDL workload"</a>
<a href="http://bugs.mysql.com/50412">Bug#50412 "Assertion `! is_set()' failed in Diagnostics_area::set_ok_status at PREPARE"</a>
<a href="http://bugs.mysql.com/42074">Bug#42074 "concurrent optimize table and alter table = Assertion failed: thd->is_error()"</a>
<a href="http://bugs.mysql.com/47335">Bug#47335 "assert in get_table_share"</a>
<a href="http://bugs.mysql.com/48246">Bug#48246 "assert in close_thread_table"</a>
<a href="http://bugs.mysql.com/47313">Bug#47313 "assert in check_key_in_view during CALL procedure"</a>
<a href="http://bugs.mysql.com/45035">Bug#45035 "Altering table under LOCK TABLES results in "Error 1213 Deadlock found..."</a>
<a href="http://bugs.mysql.com/39897">Bug#39897 "lock_multi fails in pushbuild: timeout waiting for processlist"</a>
<a href="http://bugs.mysql.com/48248">Bug#48248 "assert in MDL_ticket::upgrade_shared_lock_to_exclusive"</a>
<a href="http://bugs.mysql.com/41425">Bug#41425 "Assertion in Protocol::end_statement() (pushbuild2) (diagnostics_area)"</a>
<a href="http://bugs.mysql.com/42147">Bug#42147 "Concurrent DML and LOCK TABLE ... READ for InnoDB table cause warnings in errlog"</a>
<a href="http://bugs.mysql.com/42546">Bug#42546 "Backup: RESTORE fails, thinking it finds an existing table"</a>
<a href="http://bugs.mysql.com/46747">Bug#46747 "Crash in MDL_ticket::upgrade_shared_lock_to_exclusive on TRIGGER + TEMP table"</a>
<a href="http://bugs.mysql.com/45781">Bug#45781 "infinite hang/crash in "opening tables" after handler tries to open merge table"</a>
<a href="http://bugs.mysql.com/46673">Bug#46673 "Deadlock between FLUSH TABLES WITH READ LOCK and DML"</a>
<a href="http://bugs.mysql.com/47107">Bug#47107 "assert in notify_shared_lock on incorrect CREATE TABLE, HANDLER"</a>
<a href="http://bugs.mysql.com/38661">Bug#38661 "all threads hang in "opening tables" or "waiting for table" and cpu is at 100%"</a>
<a href="http://bugs.mysql.com/50912">Bug#50912 "Assertion `ticket->m_type >= mdl_request->type' failed on HANDLER + I_S"</a>
<a href="http://bugs.mysql.com/50786">Bug#50786 "Assertion `thd->mdl_context.trans_sentinel() == __null' failed in open_ltable()"</a>
<a href="http://bugs.mysql.com/51093">Bug#51093 "Crash (possibly stack overflow) in MDL_lock::find_deadlock"</a>
<a href="http://bugs.mysql.com/48210">Bug#48210 "FLUSH TABLES WITH READ LOCK deadlocks against concurrent CREATE PROCEDURE"</a>
<a href="http://bugs.mysql.com/45066">Bug#45066 "FLUSH TABLES WITH READ LOCK deadlocks against LOCK TABLE"</a>
<a href="http://bugs.mysql.com/45067">Bug#45067 "Assertion `stmt_da->is_error()' in Delayed_insert::open_and_lock_table"</a>
<a href="http://bugs.mysql.com/46610">Bug#46610 "MySQL 5.4.4: MyISAM MRG engine crash on auto-repair of child"</a>
<a href="http://bugs.mysql.com/47249">Bug#47249 "assert in MDL_global_lock::is_lock_type_compatible"</a>
<a href="http://bugs.mysql.com/46374">Bug#46374 "crash, INSERT INTO t1 uses function, function modifies t1"</a>
<a href="http://bugs.mysql.com/48724">Bug#48724 "Deadlock between INSERT DELAYED and FLUSH TABLES"</a>
<a href="http://bugs.mysql.com/50998">Bug#50998 "Deadlock in MDL code during test rqg_mdl_stability"</a>
<a href="http://bugs.mysql.com/47648">Bug#47648 "main.merge fails sporadically"</a>
<a href="http://bugs.mysql.com/49988">Bug#49988 "MDL deadlocks with mysql_create_db, reload_acl_and_cache"</a>
<a href="http://bugs.mysql.com/48940">Bug#48940 "MDL deadlocks against mysql_rm_db"</a>
<a href="http://bugs.mysql.com/48538">Bug#48538 "Assertion in thr_lock() on LOAD DATA CONCURRENT INFILE"</a>
<a href="http://bugs.mysql.com/44040">Bug#44040 "MySQL allows creating a MERGE table upon VIEWs but crashes when using it"</a>
<a href="http://bugs.mysql.com/39674">Bug#39674 "On shutdown mdl_destroy() called before plugin_shutdown()"</a>
<a href="http://bugs.mysql.com/46044">Bug#46044 "MDL deadlock on LOCK TABLE + CREATE TABLE HIGH_PRIORITY FOR UPDATE".</a>
</lj-cut>

Finally, some fixes are not yet in, but were "enabled" by the new design and have patches:

<a href="http://bugs.mysql.com/33669">Bug#33669 "Transactional temporary tables do not work under --read-only"</a>
<a href="http://bugs.mysql.com/36171">Bug#36171 "CREATE TEMPORARY TABLE and MERGE engine"</a>
<a href="http://bugs.mysql.com/42643">Bug#42643: InnoDB does not support replication of TRUNCATE TABLE</a>

Wooh.
