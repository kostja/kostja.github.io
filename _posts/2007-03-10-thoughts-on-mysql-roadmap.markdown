---
layout: post
date: 2007-03-10 00:51
title:  Thoughts on MySQL roadmap 
---

While reading "Crossing the Chasm" by Jeffrey Moore, I discovered that I
never actually questioned the features we added in the recent releases.

I came to MySQL with a background similar to Peter Zaitsev's, we worked
together in Spylog. MySQL was used there as storage for an in-house
scale-out application that served TBytes of data per month and hundreds of
thousands of requests per day.

The thing is, almost none of the features implemented in the recent years I
would use for that sort of appliance.

Top things on my list would be:

* integrated inverse indexes/full-text search, both InnoDB and MyISAM. And these indexes would need to scale well to give low response times for at least 500 MB tables.
* scaling to multi-core CPUs and high amount of memory (64GB and more)
* better and faster networking that would not spawn off a thread for every connection, so that the server can actually handle a connection per user.

So what would I use? Prepared statements, maybe, only if they were
noticeably faster. Mixed mode replication, that's for sure. Extended
character set support? Hardly, I'd probably run the system in pure Unicode.

It seems we were trying to add all these stored procedures and triggers to
appeal to some ERP systems and to become a viable replacement for some
extinguishing behemoths like Sybase/whatever.

The thing is, we're not there yet, and I don't know when we will be.  I
wonder if any of the modern Web 2.0 system is using this stuff.

Huh.
