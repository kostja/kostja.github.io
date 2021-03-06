---
layout: post
date:      2010-04-28 02:06
title:   RDBMS software is difficult
---

I spent the day today reviewing Dmitry's patch for <a
href="http://bugs.mysql.com/46947">Bug#46947</a>. When looking at the quick
fix, we discovered that MySQL <-> storage engine locking protocol is very
weakly defined when it comes to more advanced features, such as subqueries,
stored functions, views.

It's badly defined, it's not documented, it's not tested. As a result, some
bits of server behaviour flipped back and forth between 4.1, 5.1 and 5.5. 


The problem is that when a statement accesses the table via a subquery, view
or a function, the lock that the server needs to take on that table is not a
function of the SQL in the subquery/view itself, but depends on the context
where this view or function is used.

If we use the view in an UPDATE statement, and don't take sufficiently
strong locks on its tables or rows, replication may break, or, in some
engines, repeatable read consistency get violated.

This problem does not depend on how effectively we optimize subqueries. It
does not matter how fast the storage engine underneath is. It's a bug in the
infrastructure that MySQL server provides to its engines, and one that is
not easy to get right.

This reminded me of my conversation with David, one of MySQL founders, on
Drizzle, at the recent O'Reilly MySQL Conference.

Obviously, there is no such bug in Drizzle, which has no subqueries,
functions or views. And when they add any of those, the bug is very likely
to resurface.

That's why back then I said that it's impossible to rethink everything. At
least, it takes ages to do. I mentioned that no one was able to "rethink"
InnoDB, or throw away and replace the obscure code of MySQL optimiser. I
mentioned that there is a lot more to it, than just killing badly designed
and non-standard MySQL behaviour, or rewriting all the bits to use STL and
boost. I said that when it comes to good stuff, there is no reason why MySQL
can't or won't do it. The main reason it is harder to do changes with MySQL
is a larger legacy, including political and managerial, but you get into
exact same situation in any project after your first release. I said that
all things considered, the current MySQL trunk is perhaps as good starting
point for rethinking as the current Drizzle.

Recent years there's been a serious fragmentation of technical thought in
MySQL ecosystem. Drizzle, MariaDB, Percona are excellent for community, but
are not at all good for our ability to make MySQL a universal database
platform. I mean, ability to make MySQL a database platform comparable to
what Linux/Unix is nowadays to operating systems. Truth be said, I am not at
all sure that my current employer, Oracle, is a good host to seek this holy
grail either. Perhaps we'll never get there, not with this project.

I would not want to actually diminish importance of Drizzle (initially, I
was fond of it and rather wanted to join; the reason I didn't, I've just
spelled out). I'd love to be proven wrong, but I don't see it becoming such
a universal piece of software that I personally would like to be
contributing to. And I've never blogged about it before since, I thought,
the more forks, the better.

The reason for this blog post is  <a
href="http://www.youtube.com/watch?v=ra9K7CoVMD8">the recent interview on
Drizzle with our beloved community leader</a>. Watching the interview, I
thought that some properties of Drizzle or all forks, for that matter, are
not clearly understood.

