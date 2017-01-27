---
layout: post
date:      2013-10-02 11:34
title:   Performance of stdarg.h
---

Most discussions I was able to find online about functions with variable
number of arguments in C and C++ focus on syntax and type safety. Perhaps it
has to do with C++11 support of such functions. But how much are they
actually slower? 

I wrote a small test to find out:

<a href="https://github.com/kostja/snippets/blob/master/stdarg.c"
target="_blank">https://github.com/kostja/snippets/blob/master/stdarg.c</a>

    kostja@olah ~/snippets % gcc -std=c99 -O3 stdarg.c; time ./a.out 
    ./a.out  0.18s user 0.00s system 99% cpu 0.181 total
    kostja@olah ~/snippets % vim stdarg.c 
    kostja@olah ~/snippets % gcc -std=c99 -O3 stdarg.c; time ./a.out
    ./a.out  0.31s user 0.00s system 98% cpu 0.320 total

64-bit ABI allows passing some function arguments in C via registers.
Apparently this is not the case for functions with variable number of
arguments. I don't know for sure how many registers can be used, but the
speed difference between standard and variadic function call increases when
increasing the number of arguments.
