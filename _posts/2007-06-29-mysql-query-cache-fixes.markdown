---
layout: post
date:      2007-06-29 19:17
title:   MySQL Query cache is slow to the point of being unusable
categories:      mysql
---

We spent a lot of time this month trying to fix Bug#21074 "Large query_cache
freezes mysql server sporadically under heavy load".

In a nutshell, invalidation of a table can be dead slow (seconds) when there
are tens of thousands of cached queries associated with this table, and,
moreover, invalidation freezes the entire server when it happens.

It's so funny, this thing happens under two singleton mutexes (one instance
of the mutex exists in the entire server) both of which are required for
every single query that the server gets.

Invalidation is indeed somewhat slow, but making it a bit faster will only
shift the threshold when the query cache becomes unusable from tens of
thousands of cached results, to, say, hundreds of thousands. So we thought
it'll only change the depth of the hole in which people will discover
they've shoot themselves in the foot.

Besides, any change of that sort requires quite an overhaul of internal data
structures in the cache - not something one would do at a beta stage (the
work is being done for 5.1).

So, instead, we're trying to make the whole thing more concurrent. Eek,
perhaps these two singleton mutexes are not needed after all?

LOCK_open was taken in mysql_rm_table_part2. This thing does the actual job of DROP TABLE. 

That place we fixed to take an exclusive name lock on the table instead of
keeping the entire system frozen (good for other things as well). Thanks to
some prior patch that was done by Dmitri earlier this year in 5.1, exclusive
name locks on table metadata are now possible.

The problem with structure_guard_mutex was harder to crack. The thing is,
invalidation of one table may potentially trigger invalidation of every
single result in the query cache, and that's not known in advance, and there
is no way to lock a sub-part of the cache and then shift the lock to some
other part.

And implementing this would, again, mean, changing the whole thing quite a bit.

So we now simply disable the cache during invalidation.

Now, I'm writing this to get beaten. If it's wrong and will break your
application, please tell. If, on the contrary, you like the idea and want to
test it, stay tuned. The patch is not yet in, but soon will be.
