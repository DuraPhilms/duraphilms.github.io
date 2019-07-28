import json

DATA_LOCATION = "_data/videos.json"

with open(DATA_LOCATION) as f:
    DB = json.load(f)

def saveDatabase():
    with open(DATA_LOCATION, 'w') as f:
        json.dump(DB, f, indent=4)

def getPlaylistIds():
    return range(len(DB))

def getPlaylistsNames():
    names = []

    for p in DB:
        names.append(p["name"])

    return names

def getPlaylistsTitles():
    names = []

    for p in DB:
        names.append(p["title"])

    return names

def getPlaylistName(id):
    return DB[id]["name"]

def getPlaylistId(name):
    for i in range(len(DB)):
        if DB[i]["short"] == name or DB[i]["name"] == name:
            return i
    return -1

def getVideos(playlist = -1):
    videos = []
    if playlist == -1:
        for playlist in DB:
            for video in playlist["videos"]:
                videos.append(video)
    else:
        for video in DB[playlist]["videos"]:
            videos.append(video)

    return videos

def getVideo(playlistId, part):
    return DB[playlistId]["videos"][str(part)]

def addVideo(playlist, newVideo):
    if not newVideo in DB[playlist]["videos"]:
        DB[playlist]["videos"].append(newVideo)

def setVideoId(playlistId, part, hoster, videoId, version = "Original"):
    DB[playlistId]["videos"][str(part - 1)]["hosters"][hoster] = {"id": videoId, "version": version}
    
def removeVideoHoster(playlist, part, hoster):
    DB[playlist]["videos"][str(part)]["hosters"].pop(hoster, None)

def getVideoFilenameBase(playlistId, part):
    video = getVideo(playlistId, part)
    if video["filename"]:
        return video["filename"]
    else:
        if video["hosters"]["youtube"]["version"] == "Original":
            return storage.getPlaylistName(playlist) + "_{0:0>2}".format(args.part)
        else:
            return storage.getPlaylistName(playlist) + "_{0:0>2}_".format(args.part) + video["hosters"]["youtube"]["version"]
