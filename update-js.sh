#!/bin/bash

# videojs quality-selector: https://github.com/silvermine/videojs-quality-selector
curl -L https://unpkg.com/silvermine-videojs-quality-selector/dist/js/silvermine-videojs-quality-selector.min.js > assets/js/videojs.quality-selector.min.js
curl -L https://unpkg.com/silvermine-videojs-quality-selector/dist/css/quality-selector.css > assets/css/videojs.quality-selector.css

# videojs webvtt thumbs: https://github.com/chrisboustead/videojs-vtt-thumbnails
# currently contains local patches (see https://github.com/omarroth/videojs-vtt-thumbnails)
#curl -L https://unpkg.com/videojs-vtt-thumbnails/dist/videojs-vtt-thumbnails.min.js > assets/js/videojs.vtt-thumbnails.min.js
#curl -L https://unpkg.com/videojs-vtt-thumbnails/dist/videojs-vtt-thumbnails.css > assets/css/videojs.vtt-thumbnails.css

