---
layout: post
comments: true
title:  "Патч, позволяющий каждому коннекту иметь много user lock объектов"
date:   2012-12-05 12:00:00 +0400
categories: mysql
---

*Originally published on [Habr](https://habr.com/ru/articles/161511/)*

Привет,

Пока был в отпуске, написал патч для MySQL, позволяющий каждому коннекту владеть несколькими user lock объектами.

Патч доступен здесь:

[https://code.launchpad.net/~kostja/percona-server/userlock](https://code.launchpad.net/~kostja/percona-server/userlock)

Это последний percona-server (5.5) + новые пользовательские локи.

Подробнее про патч написал [в своём блоге](http://kostja-osipov.livejournal.com/46410.html).

Надеюсь, кому-то окажется полезен. Буду рад комментариям по этой фиче.
