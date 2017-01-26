---
layout: post
date:      2006-06-11 03:26
title:   Ubuntu Dapper Drake is up and running
categories:      ubuntu, linux, suse, vim
---

I've managed to get almost everything to work on the new Lenovo T60p laptop, which is my new home since recently. And I like the distribution too, it's a good product despite some glitches that I found on the way.<br />
<div><br />To name a few reasons why I liked Ubuntu: <br /></div>
<div class="ljcut">
<ul>
    <li>
    <div>Debian-based distribution. Inherits huge package base from it. And unlike RPM-based distributions, Debian world seems to be less fragmented - if you were able to find a .deb package for the piece of software you need, it's much more likely that this package will be accepted by your installer.</div>
    </li>
    <li>apt-get is cute! Installing software made easy (c). Say, I need ctags - I just type "apt-get install ctags" and that's it! Compare with SuSE: <br /></li>
    <ol>
        <li>Start Yast2 <br /></li>
        <li>Start Software Management application <br /></li>
        <li>Wait till it updates its sources, or whatever it does that takes precious time <br /></li>
        <li>Find the package <br /></li>
        <li>Hit OK a few times and</li>
        <li>Wait for SuSEconfig.&nbsp;</li>
    </ol>
</ul>
<blockquote>And the exact reason why I decided to go through the hassle of switching Linux distributions is that the last step, "wait for SuSEconfig", didn't improve a tiny bit throughout the last years that I've been using SuSE. For me it looked like Novell is just exploiting past achievements of the SuSE team and not adding any new value, at least in the community release. I heard there is yum in SuSE, but I've never been forced to use it - in that case perhaps I'm kind of the guy who needs to switch distributions to learn something new ;)<br /></blockquote>
<ul>
    <li>They got it right with providing community with only an ISO image of the installation CD and making the rest available online. Kind of switches the way you think of the distribution, forces you to forget about installation CDs and always rely on the apt source for new packages and updates. The installation is straightforward.<br /></li>
</ul>
<blockquote>And by the way, system upgrade is just one command: apt-get upgrade. Still have to see how it works in reality though. I decided to not use Synaptics or any other GUI for software management for why would you need a GUI if the CLI counterpart is made well?<br /></blockquote>
<div><strong>A few differences with SuSE:<br /></strong></div>
<ul>
    <li>
    <div>It's not possible to log in as root. Instead, the main user gets sudo for everything. I don't care, not an expert in Linux security, just was a bit surprised at first</div>
    </li>
    <li>zsh doesn't have a decent system-wide config file. E.g. ls coloring works in bash, but doesn't work in zsh (fixed, of course).</li>
    <li>similarly, the default postfix configuration was empty. Truth must be said that I chose no configuration at install, but they could have installed empty files to relieve me of the burden of touch $name; postmap $name. In SuSE, Postfix configuration files contain corresponding man pages, commented, which is very handy.</li>
    <li>/etc/rc.d -&gt; /etc/init.d</li>
    <li>no /etc/sysconfig found. It seems that there is no meta-config that is used to build system configuration, which is also nice</li>
    <li>because of the above it's not clear where to set up certain things. But I managed to get wireless working without much hassle (by patching /etc/network/interfaces).</li>
    <li>/etc/alternatives system - somehow I have "view" aliased to "mcview", not to "vim -R"</li>
    <li>default filesystem proposed in the installer is ext3 (SuSE uses Reiser, and I believe it's faster for my tasks)</li>
    <li>.xinitrc is not read by gdm. Moved out the things I need to .xprofile</li>
</ul>
<div><strong>A few things that didn't impress me at all :), in no particular order:<br /></strong></div>
<ul>
    <li>
    <div>I had to hack a bit to get mplayer to work - for some reason I wasn't able to find it in the repositories (even in the multiverse one) that I had on hand. Instead, I found a Debian package, fixed some dependencies in it and installed it (too bad, I know ;). <br /></div>
    </li>
    <li>
    <div>Some GUI applications still seem to be raw and not ready to be included into a mature distribution - especially it is relevant to [X|K]ubuntu desktops, which I decided to not use. <br /></div>
    </li>
    <li>
    <div>Some things still don't work, suspend and resume being the main two - but I'll get to them, there is no reason why they wouldn't.</div>
    </li>
    <li>
    <div>I found that the minimal system is shipped in somewhat broken state: the default locale is set to en_US.UTF-8, whereas locale packages are not included into the list of dependencies of the base system. When I installed the locale packages (language-support-en is the entry point I believe), I discovered that the name of the English utf8  locale is en_US.utf8, not en_US.UTF-8, as was set in /etc/environment. I wonder, why? By the way, ru_RU.KOI8-R I had to compile manually. Moreover, when I installed X I discovered that xkb doesn't work (switch to Russian does nothing) because of missing xkeyboard-config package. In short, I had to track down a few implicit dependencies and manually resolve them.</div>
    </li>
    <li>xdm turned out to be broken too. I even found a post in a forum that confirmed my guess: xdm just wouldn't start Xsesion, for no apparent reason. Spent 3 hours to realize that I need to install gdm and forget about the problem.</li>
    <li>in Xubuntu or Kubuntu you can't drop a package without dropping the entire desktop - one of the reason why I decided to not use them</li>
</ul>
<div><strong>Quick impressions from the new system:</strong></div>
<ul>
    <li>
    <div>Firefox has impressive rendering speed. "Back" button is now instant -- it seems it doesn't even require a page reload, which is neat.</div>
    </li>
    <li>
    <div>
    <div>built-in spell checking in vim7, which is not a part of Dapper Drake distribution but which I was able to easily find at <a href="http://packages.debian.org">http://packages.debian.org</a> and use for upgrade, rocks.</div>
    </div>
    </li>
</ul>
<font size="3"><font size="2">PS Installed packages:mpg321, xmms, zsh, language-support-en, mutt, icewm, xserver-xorg, xfonts-*, xfonts-efont in particular, ttf-*, xkeyboard-config, gdm, gdb, g++, valgrind, libssl-dev, zlibc, libncurses5-dev, automake1.9, autoconf, libtool, ccache, make, gdb, g++, flex, bison, ctags, irssi, thinkpad-base, tpb, tpctl, fetchmail, procmail libvorbis, libvorbisfile, libmikmod, acpi-support, laptop-mode-tools, cdrecord, xcdroast, cdparanoia, mplayer, bc, lynx, urlview, pinfo</font></font>, firefox, openoffice.org, gimp, gqview, licq<br /></div>
