---
layout: post
date:      2005-12-24 12:48
title:   MySQL Users Conference 2006
categories:      mysql
---

I've just got an email that I was <a href="http://www.mysqluc.com/cs/mysqluc2006/view/e_sess/8160">accepted</a> as a presenter for the <a href="http://www.mysqluc.com/">MySQL Users Conference 2006</a>. My 45 minute session is devoted to "Dynamic SQL in Stored Procedures", which I honestly know little about, except that I implemented the feature. 
<lj-cut>
I'm glad I'm coming again this year, although I'm a bit nervous as the talk is dedicated to DBAs, and my DBA experience is quite modest. The idea of the session is to show how to move DBA's existing scripts into a database and use DSQL for some routine administration tasks, such as optimizing tables, truncating logs, etc. Dynamic SQL is the key component here because it allows DBAs to first query their database metadata, and then construct administrative commands in accordance with it. That can't be done with basic stored procedures functionality.
5.1 delivers even more neat stuff to help in this field: it has temporal triggers (you'll be able to activate a stored procedure in a cron-like fashion) and selectable database tables to keep DBMS logs.
