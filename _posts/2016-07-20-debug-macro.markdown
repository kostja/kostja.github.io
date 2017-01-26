---
layout: post
comments: true
title:  "How to debug a segmentation fault inside a large C #define?"
date:   2016-07-20 00:09:02 +0300
categories: misc
---

Here's how you can debug a lengthy #define. You will need to know a full
object build string in your build tool (VERBOSE=1 make if you're using
cmake), and install GNU indent.

Then:

<span style="font-size:1.4em;">cc -E file.c | grep -v &#39;^#&#39; | indent &gt; out
mv out file.c
make # rebuild your project with the new file</span>

Now it's easy to see what part of a macro is causing the problem.

{% if page.comments %}

{% include disqus.html %}

{% endif %}
