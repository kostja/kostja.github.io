---
layout: post
date:      2006-03-24 16:14
title:   Counting prepared statements in MySQL 4.1
categories:      planetmysql, mysql
---

Finally found time to fix <a href="http://bugs.mysql.com/16365">Bug#16365</a>, which is a request to add a limit for the total number of prepared statements in the server. It turns out to be a pretty useful feature, at least I was able to find 4 statement leaks in the test suite with it. The patch adds server variables to limit and monitor the count of prepared statements:

<pre>
mysql> show variables like '%stmt%';
 ------------------------- ------- 
| Variable_name           | Value |
 ------------------------- ------- 
| max_prepared_stmt_count | 16382 |
| prepared_stmt_count     | 0     |
 ------------------------- ------- 
2 rows in set (0.00 sec)
</pre>

Notice that this is slightly different from the status information, as in the status we account for all prepares and executes, including unsuccessful ones:<br />
<lj-cut />
<pre>
mysql> prepare stmt from "select 1"; prepare stmt1 from "select 2";
mysql> prepare stmt2 from "select bla";
ERROR 1054 (42S22): Unknown column 'bla' in 'field list'
mysql> show variables like '%stmt%';
 ------------------------- ------- 
| Variable_name           | Value |
 ------------------------- ------- 
| max_prepared_stmt_count | 16382 |
| prepared_stmt_count     | 2     |
 ------------------------- ------- 
mysql> show status like '%stmt%';
 ------------------------- ------- 
| Variable_name           | Value |
 ------------------------- ------- 
| Com_stmt_close          | 0     |
| Com_stmt_prepare        | 3     |
 ------------------------- ------- 
</pre>

So now 4.1 has a protection against statement leaks in the application, a way to see the total number of prepared statements, and the current prepare/execute ratio. <br />
And I got <lj user="peter_zaitsev" /> off my back :)
