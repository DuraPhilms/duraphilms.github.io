---
layout: default
title: Duraphilms
---

<h1 style="text-align: center">
Durpahilms HP-Synchro-Multiversum
</h1>

<div style="width: 33.33%; float: left;">
<center>
<h2>
<b>ALLE</b> Synchroteile
</h2>
</center>
</div>

<div style="width: 33.33%; float: left;">
<center>
<h2>
<b>IMMER</b> verfügbar
</h2>
</center>
</div>

<div style="width: 33.33%; float: left;">
<center>
<h2>
<b>EXKLUSIV</b> Full-HD Remaster
</h2>
<br/>
</center>
</div>

Hier gibt es eine Auflistung **aller Synchroteile** und die Verfügbarkeit bei
verschiedenen Hostern. PvA gibt es hier zum Teil auch als **Full-HD** bzw.
**4K Remaster** von LNJ.

## Community-Gruppe

<iframe src="https://www.strawpoll.me/embed_1/21011398" style="width:680px;height:480px;border:0;">Loading poll...</iframe>

Die Community-Gruppe und andere Projekte werden in Zukunft in Kooperation mit
[Unknown6656][u6656] entstehen!

{% for playlist in site.data.videos %}
<div class="w3-margin-top">
    <a href="/{{ playlist.short }}/">
        <h1>{{ playlist.title }}</h1>
    </a>
</div>

<div style="display: grid; grid-auto-flow: column; overflow-x: scroll;">
{% for video in playlist.videos %}
    <div class="w3-padding w3-animate-opacity">
        <div class="w3-card" style="height: 100%; width: 20em;">
{% unless video.available_soon %}
            <a href="/{{ playlist.short }}/{{ video.id }}">
{% endunless %}
                <div class="w3-display-container" style="width: 100%; height: 11.3em; background: #000000;">
                    <img class="w3-display-middle" style="width: 100%;" alt="Thumbnail" src="/thumbs/{{ playlist.name }}_{{ video.id }}.small.jpg">
                </div>
{% unless video.available_soon %}
            </a>
{% endunless %}
            <div class="w3-margin">

{% unless video.available_soon %}
                <a href="/{{ playlist.short }}/{{ video.id }}">
{% endunless %}

{% if video.title %}
                    <h3>{{ video.title }}</h3>
{% else %}
                    <h3>Teil {{ video.id }}</h3>
{% endif %}

{% unless video.available_soon %}
                </a>
{% endunless %}

{% if video.available_soon %}
                <i><h5>Demnächst™ verfügbar</h5></i>
{% endif %}

                <p>
{% for upload in video.uploads %}
{% if upload.enabled %}
{% if upload.hoster == "youtube" %}
                    <a target="_blank" href="https://youtube.com/watch?v={{ upload.id }}">YouTube</a>
{% elsif upload.hoster == "twitch" %}
                    <a target="_blank" href="https://www.twitch.tv/videos/{{ upload.id }}">Twitch</a>
{% elsif upload.hoster == "vimeo" %}
                    <a target="_blank" href="https://vimeo.com/{{ upload.id }}">Vimeo</a>
{% elsif upload.hoster == "archive" %}
                    <a target="_blank" href="https://archive.org/download/{{ upload.id }}">archive.org</a>
{% elsif upload.hoster == "dropbox" %}
                    <a target="_blank" href="https://dl.dropboxusercontent.com/s/{{ upload.id }}">Dropbox</a>
{% elsif upload.hoster == "openload" %}
                    <a target="_blank" href="https://openload.co/embed/{{ upload.id }}">openload</a>
{% elsif upload.hoster == "dailymotion" %}
                    <a target="_blank" href="https://www.dailymotion.com/embed/video/{{ upload.id }}">dailymotion</a>
{% elsif upload.hoster == "u6656" %}
                    <a target="_blank" href="https://unknown6656.com/harrypotter/videos/{{ upload.id }}">Unknown6656</a>
{% endif %}

{% unless forloop.last %}
                    •
{% endunless %}

{% endif %}
{% endfor %}
                </p>
            </div>
        </div>
    </div>
{% endfor %}
</div>

{% endfor %}

## Herunterladen: *Die Synchro Offline*

Wenn ihr die Teile herunterladen möchtet könnt ihr dies am einfachsten über die
**direkten Links** von *Dropbox* und *archive.org* machen. Aktuell müsst ihr
dazu allerdings jeden Teil einzeln herunterladen.

#### Alternativ: Duraphilms-Downloadpakete auf Mega

 * *__Penner von Alcatraz__ Teil 1-14 inkl. Outtakes*: [mega.co.nz](https://mega.co.nz/#!L1IXDRCQ!5U3K8SA_Y4NgC_tTJtFTs3j3ZI-c5RZUobE1wniL3xo)
 * *__Orden des Penners__ Teil 1-13 inkl. Specials*: [mega.nz](https://mega.nz/#!25JzRApD!4bZ9Y-pYSIcxubxGR0HXQoqEvv6Nv7LdJ9sgNpT39Y4)

## Über Duraphilms.tk

Diese Seite wird von der Duraphilms-Fanorganisation _„Duraphilms.tk“_ (kreativer
Name) betreut. Wenn ihr Feedback oder anderen Input habt, könnt ihr uns gerne
auf [GitHub][gh] kontaktieren. Wenn ihr Interesse habt mitzumachen, laden wir
euch gerne in die Organisation ein.

Mehr Infos zum Videomaterial gibt es [hier](/faq).

[gh]: https://github.com/duraphilms/duraphilms.github.io
[ytdl]: https://ytdl-org.github.io/youtube-dl/index.html
[u6656]: https://unknown6656.com/harrypotter/
