---
layout: post
date:      2004-12-23 21:09
title:   Setting up vim to work with exuberant ctags
categories:      make, vim
---

Today it was the time for me to stop bearing with the way vim searches for tags by default, and give the problem another look.
<lj-cut>
 First of all, any project which is managed by automake has built-in 
'make tags'
 goal. This goal will create emacs-like TAGS file in every directory of the project, and additionally link all the files with etags-specific include directive, like:
<pre>
kostja@dragonfly:~/personal/bkprojects/search/src/common> cat ../TAGS 

/home/kostja/personal/bkprojects/search/src/common/TAGS,include

/home/kostja/personal/bkprojects/search/src/translation/TAGS,include
</pre>
One thing that confused me at first was that for some files there were no tags. It turned out that automake would parse only those
sources which are in one of _HEADERS or _SOURCES goals of the project. OK, that I fixed in a minute. After that all I needed was to make sure that the top-level `TAGS' file is visible to vim by saying:
<pre>
kostja@dragonfly:~> tail -3 ~/.vimrc
" for etags automake will generate'include' directives, so we only need to list
" those TAGS files which are on the upper level
set tags+=./../TAGS,../TAGS,./../../TAGS,../../TAGS
</pre>
Good, but it appeared that etags are not really that useful for C++: they were easily confused by namespaces and classes. So I started looking for a way to use <a href="http://ctags.sourceforge.net/">exuberant ctags</a>: dug into a Makefile, tried 'make ctags' and it worked :) In addition to 'TAGS' 'make ctags' will create 'tags' file in each directory of the project.
Now, these 'tags' don't have include lines :(, which makes it difficult to use them for the entire project:
I had to ask vim to search for tags recursively:
<pre>
set tags+=./../*/tags,./../*/*/tags
</pre>
This can be quite slow, but I had to stick to it for now.
