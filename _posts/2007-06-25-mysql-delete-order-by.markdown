---
layout: post
date:      2007-06-25 14:49
title:   On infninite usefulness of DELETE FROM t1 ORDER BY 1
---

Did you know that MySQL supports:

    DELETE FROM t1 ORDER BY a;

?

MySQL manual says:

> If the ORDER BY clause is specified, the rows are deleted in the order that is specified.

You can use stored functions and subselects there too if you like.

I should start using this feature immediately.
