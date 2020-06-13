---
layout: default
title: Duraphilms
---

Duraphilms Synchros
===================

### Fack, aehhm... *FAQ*

Diese Seite ist *nicht* von Duraphilms selbst, sondern wird von den
Duraphilms-Fans LNJ und JBB verwaltet. Wenn ihr weitere Links habt, geben wir
euch gerne Zugriff auf [GitHub][gh].

Hier gibt es eine Auflistung aller Synchroteile bei allen verschiedenen Hostern.
Ein paar Teile von PvA gibt es hier auch exklusiv als Full-HD Remake von LNJ.

Alle Teile können von den verschiedenen Seiten mittels [youtube-dl][ytdl]
heruntergeladen werden. Dropbox und archive.org verfügen allerdings auch über
direkte Links, die Ihr einfach mit dem Browser herunterladen könnt.

Mehr Infos zum Videomaterial [hier](/faq).

### Duraphilms-Downloadpakete auf Mega

*PvA Teil 1-14 inkl. Outtakes*: [mega.co.nz](https://mega.co.nz/#!L1IXDRCQ!5U3K8SA_Y4NgC_tTJtFTs3j3ZI-c5RZUobE1wniL3xo)

*OdP Teil 1-13 inkl. Specials*: [mega.nz](https://mega.nz/#!25JzRApD!4bZ9Y-pYSIcxubxGR0HXQoqEvv6Nv7LdJ9sgNpT39Y4)

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


[gh]: https://github.com/duraphilms/duraphilms.github.io
[ytdl]: https://ytdl-org.github.io/youtube-dl/index.html
