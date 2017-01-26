---
layout: post
date:      2006-01-02 17:12
title:   The case of a color-blind painter.
categories:      design patterns, mysql, c
---

I'm happy it turned out to be that simple, but the amount of such bugs and devastating consequences are humiliating.
<a href="http://bugs.mysql.com/7209">Bug#7209</a> is a case of an intermittent failure when the best brain of Support department and dozens of man hours had to be spent to track the issue down to a repeatable test case. And the cause is such a trivial design mistake:
<lj-cut><pre>
<strong>typedef</strong> <strong>struct</strong> <font color="#2040a0">st_hash</font> <font color="4444FF"><strong>{</strong></font>
  <font color="#2040a0">uint</font> <font color="#2040a0">key_offset</font>,<font color="#2040a0">key_length</font><font color="4444FF">;</font>           <font color="#444444">/* Length of key if const length */</font>

  <font color="#2040a0">uint</font> <font color="#2040a0">records</font>,<font color="#2040a0">blength</font>,<font color="#2040a0">current_record</font><font color="4444FF">;</font>
  <font color="#2040a0">DYNAMIC_ARRAY</font> <font color="#2040a0">array</font><font color="4444FF">;</font>                          <font color="#444444">/* Place for hash_keys */</font>

  <font color="#444444">/* cut */</font>
<font color="4444FF"><strong>}</strong></font> <font color="#2040a0">HASH</font><font color="4444FF">;</font>

<font color="#2040a0">gptr</font> <font color="#2040a0">hash_search</font><font color="4444FF">(</font><font color="#2040a0">HASH</font> <font color="4444FF">*</font><font color="#2040a0">info</font>,<strong>const</strong> <font color="#2040a0">byte</font> <font color="4444FF">*</font><font color="#2040a0">key</font>,<font color="#2040a0">uint</font> <font color="#2040a0">length</font><font color="4444FF">)</font><font color="4444FF">;</font>

<font color="#2040a0">gptr</font> <font color="#2040a0">hash_next</font><font color="4444FF">(</font><font color="#2040a0">HASH</font> <font color="4444FF">*</font><font color="#2040a0">info</font>,<strong>const</strong> <font color="#2040a0">byte</font> <font color="4444FF">*</font><font color="#2040a0">key</font>,<font color="#2040a0">uint</font> <font color="#2040a0">length</font><font color="4444FF">)</font><font color="4444FF">;</font>
</pre>
Now, where does hash_next get the current position of the search? In st_hash::current_record, and it, obviously, makes the search non concurrent-safe.
