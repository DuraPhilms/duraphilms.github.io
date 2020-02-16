import os
import random
import time

HOSTER_NAME = "youtube"
HOSTER_HAS_DIRECT_LINKS = False
HOSTER_KEEP_UNAVAILABLE_UPLOADS = True

def linkFromId(videoId):
    return "https://youtube.com/watch?v=" + videoId

