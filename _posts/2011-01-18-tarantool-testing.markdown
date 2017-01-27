---
layout: post
date:      2011-01-18 15:13
title:   Bringing RDBMS testing methods to a key/value storage project
categories:      tarantool, testing
---

What I'd like to describe is how I tried to bring things that are good about <a
href="http://dev.mysql.com/doc/refman/5.5/en/mysql-test-suite.html">mysql-test-run,
mysqltest</a> and <a href="http://labs.mysql.com">pushbuild</a>, to the open
source project I'm currently working on, <a
href="http://launchpad.net/tarantool">Tarantool</a>.


Since names such as mysql-test-run, mysqltest, or pushbuild tell little to
those who don't know <a
href="http://blogs.sun.com/datacharmer/entry/how_mysql_tests_servers_before">how
testing is done at MySQL</a>, I'll make a series of blog posts and try
explaining the elephant one piece at a time.

In a nutshell, there is a collection of tools that enable [open source]
projects to do development in a &quot;civilized&quot; form. Some projects
only use select pieces of the puzzle, but the best effects are, in my view,
achieved when all pieces are made to work together.

These pieces include:

* automated regression testing
* a framework for functional tests
* a framework for unit tests
* automated continuous integration
* automated software packaging

Together these tools form a habitat for a feature or bug in the course
of its whole life, and help engineers write high quality software, remove
routine work, while providing managers with more accountability, and the
whole project with room to grow.

I have to admit that when I started, I didn't know what I'm up to: <a
href="http://github.com/tarantool/tarantool">Tarantool</a>is a key/value
storage, which is often sharded, whereas I approached my task with putting
the heaviest emphasis on functional regression tests, like we had with
MySQL, and thinking that a key/value storage simply provides a subset of SQL
database functionality. It turned out, I was not quite right :-)
