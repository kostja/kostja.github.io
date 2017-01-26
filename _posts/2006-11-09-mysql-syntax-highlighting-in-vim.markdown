---
layout: post
date:      2006-11-09 02:00
title:   MySQL syntax highlighting in Vim
categories:      mysql, vim
---

I didn't know such a thing exists.
<pre>
kostja@bodhi:/usr/share/vim/vim70/syntax> ls -al mysql.vim 
-rw-r--r-- 1 root root 16078 2006-05-24 20:16 mysql.vim
<lj-cut />
kostja@bodhi:/usr/share/vim/vim70/syntax> head -7 mysql.vim 
" Vim syntax file
" Language:     mysql
" Maintainer:   Kenneth J. Pronovici <pronovic@ieee.org>
" Last Change:  $date: 2004/06/13 20:12:39 $
" Filenames:    *.mysql
" URL:		ftp://cedar-solutions.com/software/mysql.vim
" Note:		The definitions below are taken from the mysql user manual as of April 2002, for version 3.23
</pre><b>To enable it in the editor:</b>
<pre>
:set filetype=mysql
</pre>
Or, in your .vimrc to highlight all .sql and .test files:
<pre>
if has("autocmd")
        autocmd BufRead *.sql set filetype=mysql      
        autocmd BufRead *.test set filetype=mysql
endif
</pre>
