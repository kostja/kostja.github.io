---
layout: post
date:      2007-05-24 13:02
title: Frustration over MySQL use of C++
---

Today I tried to add this little function to our impekkable List template:

    template <typename t="T">
    inline
    List<t>::List(const List<t> &rhs, MEM_ROOT *mem_root)
      :base_list(rhs, mem_root)
    {
      /* Make a deep copy of each element */
      List_iterator<t> it(*this);
      T *el;
      while ((el= it++))
        it.replace(new (mem_root) T(*el));
    }

That is, for the referecne, the default copy constructor for List template
is shallow.  So, I needed a _normal_ copy constructor. I don't want to
rewrite the existing one -- it is used eveywhere (and don't ask me how one
can make any sane use of a shallow copy constructor of a container - because
all the usages are insane).  And here we go - this won't compile:

    sql_list.h: In constructor ‘List<t>::List(const List<t>&, MEM_ROOT*) [with T = Item]’:
    item.cc:6917:   instantiated from here
    sql_list.h:581: error: cannot allocate an object of abstract type ‘Item’
    item.h:446: note:   because the following virtual functions are pure within ‘Item’:
    item.h:541: note: 	virtual Item::Type Item::type() const

item.cc:6917 is gorgeous:

    #ifdef HAVE_EXPLICIT_TEMPLATE_INSTANTIATION
    template class List<item>;
    template class List_iterator<item>;
    template class List_iterator_fast<item>;
    template class List_iterator_fast<item_field>;
    template class List<list_item>;
    #endif

And explicit instantiation is the default. And class Item is of course an
abstract base.  So, boy, have you had fun with meta-programming? Alright,
now do some real stuff - write 

    mysql_copy_list(void *from, void *to);

