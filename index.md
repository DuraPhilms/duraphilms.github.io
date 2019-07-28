---
layout: default
title: Duraphilms
---

DuraPhilms Fan Productions
==========================

Diese Seite ist *nicht* von DuraPhilms selbst, sondern von den ultra krassen
DuraPhilms-Fans LNJ und JBB. Wenn ihr weitere Links habt, geben wir euch gerne
Zugriff auf [GitHub](https://github.com/duraphilms/duraphilms.github.io).

Hier gibt es eine Auflistung aller Synchro Teile bei allen verschiedenen Hostern.
Hierbei entspricht 1080Rmk, einem 1080p Full-HD Remaster (von LNJ).

Alle Teile können von den verschiedenen Seiten mittels
[youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html) heruntergeladen werden.


{% for playlist in site.data.videos %}
# {{ playlist.title }}

<div style="display: grid; grid-auto-flow: column; overflow-x: scroll;">
{% for video in playlist.videos %}
    <div class="w3-padding">
        <div class="w3-card" style="height: 100%; width: 20em;">
            <div class="w3-display-container" style="width: 100%; height: 11.3em; background: #000000;">
                <img class="w3-display-middle" style="width: 100%;" alt="Thumbnail" src="/thumbs/{{ playlist.name }}_{{ video[0] }}.jpg">
            </div>

            <div class="w3-margin">
{% if video[1].title %}
                <h3>{{ video[1].title }}</h3>
{% else %}
                <h3>Teil {{ video[0] }}</h3>
{% endif %}

{% if video[1].available_soon %}
                <i><h5>Demnächst™ verfügbar</h5></i>
{% endif %}

                <p>
{% for hoster in video[1].hosters %}
{% if hoster[1].id != "" %}
{% if hoster[0] == "youtube" %}
                    <a target="_blank" href="https://youtube.com/watch?v={{ hoster[1].id }}">YouTube</a>
{% elsif hoster[0] == "twitch" %}
                    <a target="_blank" href="https://www.twitch.tv/videos/{{ hoster[1].id }}">Twitch</a>
{% elsif hoster[0] == "vimeo" %}
                    <a target="_blank" href="https://vimeo.com/{{ hoster[1].id }}">Vimeo</a>
{% elsif hoster[0] == "archive" %}
                    <a target="_blank" href="https://archive.org/download/{{ hoster[1].id }}">archive.org</a>
{% elsif hoster[0] == "dropbox" %}
                    <a target="_blank" href="https://dl.dropboxusercontent.com/s/{{ hoster[1].id }}">Dropbox</a>
{% elsif hoster[0] == "openload" %}
                    <a target="_blank" href="https://openload.co/embed/{{ hoster[1].id }}">openload</a>
{% endif %}

{% if forloop.rindex != 1 %}
                    •
{% endif %}

{% endif %}
{% endfor %}
                </p>
            </div>
        </div>
    </div>
{% endfor %}
</div>
{% endfor %}

