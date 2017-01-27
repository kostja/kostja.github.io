---
layout: post
date:      2015-01-14 21:41
title:   inotify_add_watch()/inotify_rm_watch() perofrmance
---

Turns out, inotify performance depends on the path.

Why is <b>/tmp</b> so much slower? The filesystem is the same (ext4). My
only guess is that it has so many events that inotify_rm_watch has to do a
lot of work to clear them.

<div class="gh-gist" data-gist-id="kostja/3990427faa32d9d5befd"><a href="https://gist.github.com/kostja/3990427faa32d9d5befd">gist.github.com/kostja/3990427faa32d9d5befd</a></div>
