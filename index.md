---
layout: default
title: Duraphilms
---

<link rel="stylesheet" href="assets/css/indexStyle.css">

<div id="DarkModeButton"><svg width="100%" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 496"><path fill="currentColor" d="M8,256C8,393,119,504,256,504S504,393,504,256,393,8,256,8,8,119,8,256ZM256,440V72a184,184,0,0,1,0,368Z" transform="translate(-8 -8)"/></svg></div>

<div id="StickyHeadline" style="position: sticky; top: 0; z-index: 1; height: 4em; padding-top: 0.4em; margin-bottom: 1em; background-color: white; border-bottom: 1px solid #159957">
<h1 style="text-align: center;">
Duraphilms Synchros
</h1>
</div>

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

# Jetzt NEU unser Discord-Server: [chat.duraphilms.tk](https://chat.duraphilms.tk)!

<iframe src="https://discordapp.com/widget?id=760488636382445590&theme=dark" width="100%" height="300" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>

{% for playlist in site.data.videos %}
<div class="w3-margin-top">
    <a href="/{{ playlist.short }}/">
        <h1>{{ playlist.title }}</h1>
    </a>
</div>

<div style="position: relative; width: 100%;">
<div id="Carusell{{ playlist.short }}" style="scroll-behavior: smooth; height: 19em; display: grid; grid-auto-flow: column; overflow: hidden;">
{% for video in playlist.videos %}
    <div class="w3-padding w3-animate-opacity">
        <div onmouseover="mOver(this.id)" onmouseout="mOut(this.id)" id="{{ playlist.short }}{{ video.id }}" class="w3-card">
{% unless video.available_soon %}
            <a href="/{{ playlist.short }}/{{ video.id }}">
{% endunless %}
                <div class="w3-display-container" style="width: 100%; height: 11.3em; background: #000000; border-radius: 0.5rem">
                    <img class="w3-display-middle" style="width: 100%;" alt="Thumbnail" src="/thumbs/{{ playlist.name }}_{{ video.id }}.small.jpg">
                </div>
{% unless video.available_soon %}
            </a>
{% endunless %}
            <div style="position: absolute; top: 0; text-shadow: 0px 0px 3px black;" class="w3-margin">
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
</div>

            <div class="w3-margin">
{% if video.available_soon %}
                <i><h5>Demnächst™ verfügbar</h5></i>
{% endif %}
                <p class="Wo" id="Wo{{ playlist.short }}{{ video.id }}" style="display: none;">
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
<div id="{{ playlist.short }}" onclick="leftScroll(this.id)">
    <div style="
    position: absolute;
    top: 0px;
    height: 100%; 
    width: 5rem;
    background-image: 
    linear-gradient(to right, rgb(255, 255, 255), rgba(255, 255, 255, 0));
    " class="left ScrollButtons"><img style="transform: translateY(4em) rotate(180deg);" src="assets/images/arrow.svg"></div>
</div>
<div id="{{ playlist.short }}" onclick="rightScroll(this.id)">
    <div style="
    position: absolute;
    top: 0px;
    height: 100%; 
    width: 5rem;
    background-image: linear-gradient(to left, rgb(255, 255, 255), rgba(255, 255, 255, 0)); right: 0;
    " class="right ScrollButtons"><img style="transform: translateY(4em);" src="assets/images/arrow.svg"></div>
</div>
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

<script src="assets/js/DarkmodeIndex.js"></script>
<script src="assets/js/IndexScrollButtons.js"></script>
