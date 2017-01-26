---
layout: post
date:      2012-08-13 16:05
title:   Ropes and AVL trees
---

<p>
Last week I've been working on a new 
<a href="http://www.tarantool.org/tarantool_user_guide.html#language-reference">UPDATE
command</a>
implementation in Tarantool.
</p>

<p>
Tarantool UPDATE can modify, add and remove individual
fields in a tuple.
</p>

<p>
A typical UPDATE looks like a sequence of operations,
e.g. <b>'set field 1 to "abc", insert value "foo" after field 5, delete
field 10, push value "tail" at the end of the tuple'</b>.
</p>

<p>
The difficulty of an efficient implementation 
is caused by the tuple format:  essentially, it's a blob storing
a sequence of length-prefixed strings.
</p>

<p>
Due to this format, accessing an invividual field in a tuple has
linear cost (<b>O(tuple size)</b>). In consequence of this, tuples are never modified in
place.
</p><lj-cut />
<p>
When UPDATE contains many operations, they are all first
"compiled", and then a new tuple is created based on the old tuple
data and "modification instructions", produced from
the operation list.
</p>

<p>
This all works fine, with one exception: the algorithm
is written in such way that all indexes of fields in a tuple are
"frozen" at start of UPDATE. 
E.g. if an UPDATE deletes field 5, and then inserts a new field after
field 5, the new field is inserted in place of the deleted one,
not at the relative position in the "intermediate" tuple.
</p>

<p>
At first I personally didn't consider this a serious defect, but
then <lj user="avdicius" /> pointed out that this semantics makes
it impossible to batch multiple UPDATEs into a single one.
</p>
<p>
The other flaw of the existing implementation was that, even though 
it was efficient enough (it took <b>O(K * log(K) ) + O(N)</b> time to do an update,
where K is the number of operations, and N is the size of the tuple), 
it was rather complicated - 300 lines of difficult to read C code.
</p>

<p>
UPDATE operations were ordered by field number, then
put into an intrusive linked list, etc. 
We needed an axuiliary container to store UPDATE ops, to delegate 
the semantics of operation ordering.
</p>

<p>
A <a href="http://en.wikipedia.org/wiki/Rope_(computer_science)">rope</a> looked like a viable solution.
</p>

<p>
Unfortunately, after quite a bit of digging, it turned out that there is no
good standalone implementation of ropes. It seems ropes did
not go mainstream, are still only employed in a few specific cases or 
as an advanced topic in a technical interview.
</p>

<p>
We found that
<a href="http://www.hpl.hp.com/personal/Hans_Boehm/gc/">Hans Boehm's
cords</a> are tightly coupled with his
garbage collector, <a href="http://www.sgi.com/tech/stl/Rope.html">STL ropes</a>, again,
are quite bloated and integrated with STL allocators too tightly.
Besides, both implementations use a very simple tree balancing
procedure, which doesn't produce well balanced trees and doesn't
care about memory consumption very much.
</p>

<p>
Popular edge cases are not optimized either: for example, deletion of a
substring from a rope is typically done by means of two tree splits and one
merge (cut the tail, cut the tail of the tail, throw away the
middle, merge the beginning and the end), whereas in Tarantool one
doesn't delete ranges of fields, and deletion of an individual
field can easily be done by a usual <a href="http://en.wikipedia.org/wiki/Binary_search_tree#Deletion">binary
tree deletion</a>.
</p>

<p>
Tree balancing was not perfect either: implemented the same way as in Fibonacci heap,
which doesn't produce a very balanced tree. 
</p>

<p>
Tarantool needed something with low enough overhead to justify use of a complex
data structure even when the number of operations in an UPDATE is
small (typically an UPDATE in Tarantool contains less than half a
dozen of ops), but scalable to large commands.
</p>

<p>
Thus, an idea to use AVL tree balancing algorithm emerged, and all the time I had
for coding last week I devoted to writing a rope 
with AVL balancing procedures.
I chose AVL, as opposed to, say, RB or Andersson trees since I
knew it from the University.
</p>

<p>
An intermediate result you can see <a href="http://codeviewer.org/view/code:28d9">here</a>. I borrowed a lot of
ideas from an excellent AVL tree tutorial at
<a href="http://eternallyconfuzzled.com">http://eternallyconfuzzled.com</a>.
</p>
<p>
The main idea is that all nodes are used to store substrings, not
just leaf nodes, and typical operations, such as tree insert or
delete, are done not by means of tree split and merge, typical
for ropes, but by means of insertion and deletion from AVL
tree.
</p>
<p>
AVL balance algorithm had to be modified, since insertion,
when dealing with a rope, can insert not one node but
two.
</p>
<p>
I'm still not sure if writing such a basic data structure almost
from scratch was a good idea, or if it was worth the time spent.
The good news is that
the random tree generator I wrote at the dawn of Friday found
no tree consistency bugs yet.
</p>
<p>
If someone, who knows binary
trees and computer science better than me (I'm a nub,
being in database technology means being a jack of all trades),
is reading this blog post, I'd be grateful to all comments
pointing out anything I might have missed.
</p>
