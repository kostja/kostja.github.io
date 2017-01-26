---
layout: post
date:      2005-08-22 23:50
title:   Adding plugins to the server
---

We're adding plugin support to MySQL 5.1. While reviewing the task
description and the patch today, I realized that this must be one of the
coolest features of a database server, and noone else to my knowledge did
something like that.  We of course have had support for user defined
functions for ages and other databases have similar functionality, but the
thing I was looking at today can let one load and use much much bigger and
more useful things.

A storage engine, PAM, fulltext search extensions, a custom query parser --
a few of the examples given in the task. Of course for storage engines we
were able to add a custom one as early as in 3.22, but to do that now one
has to visit a Users Converence and listen to <a
href="http://krow.net">Brian's</a> talk. 

But the main difference is that "plugin" is such a sticky and well-known
word that you don't need to explain the concept any more: anyone who once
used WinAmp knows what "plugin" is.
