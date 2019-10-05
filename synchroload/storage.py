#!/usr/bin/env python3

import json
import shutil
import os

DATA_LOCATION = "_data/videos.json"
COLLECTIONS_PLAYLISTS_LOCATION = "_playlists/"
COLLECTIONS_VIDEOS_LOCATION = "_videos/"

VIDEO_VERSIONS = [
    "Remastered",
    "Remake",
    "Original",
]

with open(DATA_LOCATION) as f:
    DB = json.load(f)

class Upload():
    hoster = ""
    id = ""
    version = "Original"
    resolution = -1

    def __init__(self, structs = None):
        if structs:
            self.hoster = structs["hoster"]
            self.id = structs["id"]
            self.version = structs["version"]
            self.resolution = structs["resolution"]

    def toJsonSerializable(self) -> dict:
        output = {}
        output["hoster"] = self.hoster
        output["id"] = self.id
        output["version"] = self.version
        output["resolution"] = self.resolution
        return output

class Video():
    id = ""
    available_soon = False
    date = ""
    title = ""
    description = ""
    filename = ""
    uploads = []

    def __init__(self, structs = None):
        if structs:
            self.id = structs["id"]
            if "available_soon" in structs:
                self.available_soon = bool(structs["available_soon"])
            if "date" in structs:
                self.date = structs["date"]
            if "title" in structs:
                self.title = structs["title"]
            if "description" in structs:
                self.description = structs["description"]
            if "filename" in structs:
                self.filename = structs["filename"]
            self.uploads = []
            for u in structs["uploads"]:
                self.uploads.append(Upload(structs = u))
    
    def toJsonSerializable(self) -> dict:
        output = {}
        output["id"] = self.id
        if self.available_soon:
            output["available_soon"] = True
        if self.date:
            output["date"] = self.date
        if self.title:
            output["title"] = self.title
        if self.description:
            output["description"] = self.description
        if self.filename:
            output["filename"] = self.filename
        output["uploads"] = []
        for u in self.uploads:
            output["uploads"].append(u.toJsonSerializable())
        return output

    def getUpload(self, hoster: str, resolution: int) -> Upload:
        if resolution > 0:
            for u in self.uploads:
                if u.hoster == hoster and u.resolution == resolution:
                    return u
        else:
            for u in self.uploads:
                if u.hoster == hoster:
                    return u

    def removeUpload(self, uploadId):
        self.uploads = [u for u in self.uploads if u.id != uploadId]

class Playlist():
    title = ""
    name = ""
    short = ""
    videos = []
    newest_first = False

    def __init__(self, structs = None):
        if structs:
            self.title = structs["title"]
            self.name = structs["name"]
            self.short = structs["short"]
            if "newest_first" in structs:
                self.newest_first = bool(structs["newest_first"])
            self.videos = []
            for v in structs["videos"]:
                self.videos.append(Video(structs = v))
    
    def toJsonSerializable(self) -> dict:
        output = {}
        output["title"] = self.title
        output["name"] = self.name
        output["short"] = self.short
        if self.newest_first:
            output["newest_first"] = True
        output["videos"] = []
        for v in self.videos:
            output["videos"].append(v.toJsonSerializable())
        return output

    def getVideo(self, id: int):
        for v in self.videos:
            if int(v.id) == id:
                return v

class Database():
    playlists = []

    def __init__(self, filepath: str = DATA_LOCATION):
        self.filepath = filepath
        with open(self.filepath) as f:
            data = json.load(f)

        self.playlists = []
        for p in data:
            self.playlists.append(Playlist(structs = p))
    
    def toJsonSerializable(self) -> list:
        output = []
        for p in self.playlists:
            output.append(p.toJsonSerializable())
        return output

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.toJsonSerializable(), f, indent=4)
            f.write("\n")

    def getPlaylistByName(self, name: str):
        for p in self.playlists:
            if p.short == name or p.name == name:
                return p
    
    def getVideoFilenameBase(self, video, upload, playlist = None):
        name = ""
        if video.filename:
            name = video.filename
        else:
            name = playlist.name + "_" + "{0:0>2}".format(int(video.id))

        if upload.version and upload.version != "Original":
            name += "_" + upload.version

        if upload.resolution:
            name += "." + str(upload.resolution) + "p"

        return name

if __name__ == "__main__":
    db = Database()
    print(db.toJsonSerializable())
    db.save()

"""
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

    if "title" in playlist["videos"][videoId]:
        f.write("title: {}\n".format(playlist["videos"][videoId]["title"]))
    else:
        f.write("title: {} Teil {}\n".format(playlist["title"], videoId))

    f.write("permalink: /" + playlist["short"] + "/{0:0>2}/\n".format(videoId))

    f.write("playlist: {}\n".format(playlist["short"]))

    f.write("part: {}\n".format(videoId))

    if str(int(videoId) + 1) in playlist["videos"]:
        f.write("nextVideo: {}\n".format(int(videoId) + 1))
    if str(int(videoId) - 1) in playlist["videos"]:
        f.write("prevVideo: {}\n".format(int(videoId) - 1))

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
"""
