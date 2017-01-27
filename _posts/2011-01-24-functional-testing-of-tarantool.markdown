---
layout: post
date: 2011-01-24 21:10
title:   Automation of functional testing of a key/value storage
categories: python, tarantool, testing
---

<a href="http://kostja-osipov.livejournal.com/33310.html">In my previous
post</a> I described what it took to add SQL support and a simple command
line client to a NoSQL storage.  However, I needed not just ad-hoc testing
with a client, but a framework to automatically run and manage many
tests.

I expect that automated tests are easy to understand, extend, and maintain.
When a test breaks, finding and debugging what broke should be easy. Such
qualities can not be met in a heterogeneous test environment. Rather, it
would be best if some common language and toolkit was used. It's easiest for
all when a failing test can be run directly under a debugger.

In MySQL, this task is solved with a combination of 'mysqltest' client-side testing tool and 'mysql-test-run', an automation environment for functional tests.  

<a
href="http://dev.mysql.com/doc/mysqltest/2.0/en/mysqltest-reference.html">'mysqltest'</a>
is a C program that simply reads lines from its standard input, sends them
to the server, formats received results, and sends them to the standard
output. It also has <a
href="http://dev.mysql.com/doc/mysqltest/2.0/en/mysqltest-commands.html">&quot;control
statements&quot;</a>, encrypted in SQL comments.

These control statements, for example, allow to create a loop, open a new
connection to the server, change the current connection, move or delete a
file, rewrite server output.  

The test runner, <a href="http://dev.mysql.com/doc/mysqltest/2.0/en/running-tests.html">'mysql-test-run'</a>, prepares server environment, such as data directory and default configuration, starts and stops the server, collects test scripts, feeds them to mysqltest, records mysqltest ouptut.  

When a new .test file with SQL statements is created, a developer can grab
mysqltest output and put it into a .result file. When mysql-test-run later
runs the .test script through mysqltest, it compares the new output with the
old one.  

A set of .test and corresponding .result files, which needed to be run in a
certain server configuration, comprise a test collection.  

'make test', in turn, is aliased to mysql-test-run running several mandatory
collections, containing regression tests.  

I liked mysql-test-run approach so much I almost  forked the script.
Unfortunately, while having a pretty lean design when it comes to test
management, all parts related to working with MySQL were hard to
encapsulate. Support for non-default storage engines, replication,
MySQL-specific installation procedure were hard to remove -- it was easier
to duplicate important features in a new tool. 

But even with the new tool I re-used mysql-test-run layout and options. This
way, the first version of test automation was built very soon.  It used
'tarantool' command line client and a simple Python script (./test-run.py),
copying the most basic functions of mysql-test-run. Such approach, however,
worked only thus far.  

If one comes back to mysqltest and the testing language it supports, a big
advantage of it lays in SQL language extensions that allow a test writer to
manipulate with execution environment. 

For example, one of important recurring bugs in <a
href="http://launchpad.net/tarantool">Tarantool</a> was that it would fail
to start from an existing snapshot. A possible test for such bug is to
create a snapshot, restart the server, and then SELECT all keys to verify
that the snapshot is correct.  

In other words, almost immediately the implemented automation functionality
wasn't sufficient: in the course of test execution, I needed to manipulate
with the execution environment, i.e. start and stop the server.  

Since I spent so much time working with mysqltest, I almost added support
for the required commands to my SQL dialect. But then the need for some type
    of remote procedure calls arose, since it was necessary to pass requests
    from the command line client to the test runner. The whole thing started
    to look too complicated :-(  

Thankfully, after a discussion with <a
href="http://www.github.com/delamonpansie">delamonpansie</a> a simpler and
more flexible solution emerged.  Indeed, instead of trying to extend the SQL
client with  control flow and environment management statements, it was
easier to extend the test-runner interpreter (Python) to be able to
understand SQL. 

In other words, it was decided to:

* move from SQL to Python as the base language for testing
* find a way to execute a Python script in the runtime environment of the
  test framework. E.g. imagine a test script which contains:  

    server.start()
    server.stop() 

Executing this script in the runtime environment of the test runner would
execute methods start() and stop() of local variable 'server'.  This
approach automatically provides a test writer with operating system and
hardware independent access to test environment, file manipulation, logging,
control flow, basically everything a modern portable scripting language
provides you with!  Fortunately, Python came in very handy with its
execfile() function. 


* find a way to nicely embed SQL statements into Python. Ideally, I needed
  to be able to write:  

    server.start()
    select * from t0 where k0 = 1
    sever.stop()
     ...

This goal was harder to reach. Ideally, I wanted to have a dialect of
Python, which would allow me to embed SQL constructs into it. That would
make my old pure-SQL tests directly usable with the new tool.
Unfortunately (for me, but good for Python, according to #python freenode
community :)) the language grammar could not be extended.  Best I could do
was modifying Python's preprocessor and/or tokenizer (these objects of the
interpreter runtime are available to the script via an API). This is what I
indeed  have done, by providing a custom &quot;codec&quot; to the
interpreter.


In the end, my testing language looks like this:  

    # encoding "tarantool"
    server.start()
    exec sql &quot;select * from t0 where k0 = 1&quot;
    sever.stop()
    ...
  
Not ideal (I would love to make SQL a complex part of the language grammar,
and not use the pre-processor), but having  its strenghts too:   

    for i in range(0,10):
      exec sql "select * from t0 where k0 = {0}".format(i)

I'm very pleased with the end result: it turned out to  be way more flexible
than the limited SQL extensions I had with mysqltest!

