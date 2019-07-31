import json
import shutil
import os

DATA_LOCATION = "_data/videos.json"
COLLECTIONS_PLAYLISTS_LOCATION = "_playlists/"
COLLECTIONS_VIDEOS_LOCATION = "_videos/"

VIDEO_VERSIONS = [
    "1080Rmk",
    "Remake",
    "Original",
]

with open(DATA_LOCATION) as f:
    DB = json.load(f)

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

def setVideoId(playlistId, part, hoster, videoId, version):
    DB[playlistId]["videos"][str(part)]["hosters"][hoster] = {"id": videoId, "version": version}

def removeVideoHoster(playlist, part, hoster):
    DB[playlist]["videos"][str(part)]["hosters"].pop(hoster, None)

def getVideoFilenameBase(playlistId, part, hoster):
    video = getVideo(playlistId, part)
    if "filename" in video and video["filename"]:
        return video["filename"]
    else:
        if not hoster or video["hosters"][hoster]["version"] == "Original":
            return getPlaylistName(playlistId) + "_{0:0>2}".format(part)
        else:
            return getPlaylistName(playlistId) + "_{0:0>2}_".format(part) + video["hosters"][hoster]["version"]

def writePlaylist(playlist):
    f = open(
        COLLECTIONS_PLAYLISTS_LOCATION + playlist["short"] + ".md",
        "w"
    )
    f.write("---\n")
    f.write("layout: playlist\n")
    f.write("title: {}\n".format(playlist["title"]))
    f.write("permalink: /{}/\n".format(playlist["short"]))
    f.write("playlist: {}\n".format(playlist["short"]))
    f.write("---\n")
    f.close()

def writeVideo(playlist, videoId):
    f = open(
        COLLECTIONS_VIDEOS_LOCATION + playlist["short"] + "_{0:0>2}.md".format(videoId),
        "w"
    )
    f.write("---\n")
    f.write("layout: video\n")
    f.write("title: {}".format(playlist["title"] + " {0:0>2}\n".format(videoId)))
    f.write("permalink: /" + playlist["short"] + "/{0:0>2}/\n".format(videoId))
    f.write("playlist: {}\n".format(playlist["short"]))
    f.write("part: {}\n".format(videoId))
    f.write("---\n")
    f.close()

def writeCollections():
    print("[storage] Cleaning up...")
    # delete everything
    for directory in ["_playlists", "_videos"]:
        shutil.rmtree(directory)
        os.mkdir(directory)

    print("[storage] Generating collections...")
    for playlist in DB:
        writePlaylist(playlist)
        for video in playlist["videos"]:
            writeVideo(playlist, video)

def saveDatabase():
    with open(DATA_LOCATION, 'w') as f:
        json.dump(DB, f, indent=4)
    writeCollections()
