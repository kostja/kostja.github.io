---
layout: post
date:      2007-06-29 17:54
title:   My top 5 MySQL wishes
categories:      mysql
---

There has been a trend in the blogs for top5 MySQL wishes.

Many people, including <a href="http://blog.arabx.com.au/?p=739">Ronald
Bradford</a>, <a href="http://dormando.livejournal.com/469685.html">Alan
Kasindorf</a>, <a href="http://trainedmonkey.com/2007/6/23/my_five_mysql_wishes">Jim
Winstead</a>, <a href="http://www.cybersite.com.au/blog/mysql_five_wishes">Jonathon
Coombes</a>, <a href="http://jcole.us/blog/archives/2007/06/20/my-top-5-wishes-for-mysql/">Jeremy
Cole</a>, <a href="http://www.jpipes.com/index.php?/archives/172-My-Top-5-Wishlist-for-MySQL.html">Jay
Pipes</a>, <a href="http://antbits.blogspot.com/2007/06/wish-lists.html">Antony
Curtis</a>, <a href="http://www.flamingspork.com/blog/2007/06/19/my-top-5-wishlist-for-mysql/">Stewart
Smith</a> coined in.

Here're my 5:

1. Remove excessive fuss. OK, we know what needs to be done, just give us
   time to get things in order. Anything related to MySQL gets huge
   visibility, and we tend to overestimate the importance of "opinion of
   community". If you have a cool new feature for the server or a cool new
   wish, let it cook for a while. If you have or want to write a patch,
   first get in touch with developers, discuss things on internals@ or
   commits@, then post your patch on the Forge and see if it takes off. Be
   sure it'll get in if it's a really good idea. But not next week. Perhaps
   in a year or two. Want your code to be accepted faster? Write a good fix
   for a bug. We have 1100 of them. Still want it in faster? Fix a crash.

2. Open the development process. This is the other side of the previous
   wish. It takes a year or two to introduce a new engineer into all the
   existing conventions. So an external engineer just can't write a good
   patch for the server. Besides, we  mostly in need of contributions that
   improve and simplify the existing code base, not add new code. But it is
   increasingly hard to change the existing code -- implicit dependencies,
   no good tests, almost  non-existent unit test coverage. This is a barrier
   for penetration, and it's a catch, catch-22.

3. Get to a normal release schedule. Have XXX.1, XXX.2, XXX.3 releases once
   or twice a year. There is a lot in this wish that makes it very hard to
   satisfy -- planning, compatibility, healthy life cycle, high quality
   support. But we do need to shift the load of patches pushed to the period
   when a version is in alpha, not when it's in GA, and we do need to
   release more often.

4. Establish productive relationship with the majority of users. Something
   tells me that visibility does not equate to quality of input, and we get
   most of our input from early adopters, not from the large majority. We
   need this for the next wish:

5. Find a way to do incompatible changes with minimal pain for users. If we
   don't deprecate the 'cool non-standard features most needed now' that
   were added during brave times of 3.23 and 4.0, the software is a dead
   fish.
