---
layout: post
date:      2006-03-06 22:44
title:   "Encapsulation in C++: public members vs. getters"
categories: "c++"
---

Reading yet another book which advocates

```B& a.get_b()```

versus simple

```a.b```

and getting really sick of it. Let's state that: both are equally evil. The
main advantage that is usually named when promoting get\_b() is that one day
you can change the implementation to do a little more without having to
update the clients.

**Wrong**.

Once you change the semantics, you also must change the name -- if your
method suddenly starts doing a little extra, to be on the safe side you need
to ensure that all users are fine with the new logic.

Of course one never can check all clients of a shipped library, but this
only means that in a shipped library you're better off not having public
members (or getters) at all.
