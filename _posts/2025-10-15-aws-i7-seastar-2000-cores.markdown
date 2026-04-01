---
layout: post
comments: true
title:  "AWS i7 и seastar на 2000 ядер"
date:   2025-10-15 10:55:00 +0000
categories: rabid-transit seastar cloud
---

Амазон [выпустила линейку машин i7\*](https://aws.amazon.com/ec2/instance-types/i7i/) (из России ссылку не открыть) в которой (в облаке) доступно до 192 ядер, 1.5ТБ оперативной памяти и 100Gbps сеть. Это уже привело [к серии патчей](https://github.com/scylladb/seastar/pull/3053) в [seastar](http://seastar.io/) которая до этого не умела работать с CPU c более чем 256 ядрами. Теперь seastar поддерживает до 2000 ядер. И совсем непонятно как классические СУБД к этому будут адаптироваться.
