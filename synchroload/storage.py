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

HOSTER_SORTING = [
    "youtube",
    "gdrive",
    "dropbox",
    "onedrive",
    "archive",
    "u6656",
    "linuj24",
    "twitch",
    "vimeo",
    "openload",
    "dailymotion"
]

class Upload():
    hoster = ""
    id = ""
    version = "Original"
    resolution = -1
    enabled = True
    origin = ""
    container = ""

    def __init__(self, structs = None):
        if structs:
            self.hoster = structs["hoster"]
            self.id = structs["id"]
            self.version = structs["version"]
            self.resolution = structs["resolution"]
            if "enabled" in structs:
                self.enabled = bool(structs["enabled"])
            if "origin" in structs:
                self.origin = str(structs["origin"])
            if "container" in structs:
                self.container = str(structs["container"])

    def toJsonSerializable(self) -> dict:
        output = {}
        output["hoster"] = self.hoster
        output["enabled"] = self.enabled
        output["id"] = self.id
        output["version"] = self.version
        output["resolution"] = self.resolution
        if self.origin:
            output["origin"] = self.origin
        if self.container:
            output["container"] = self.container
        return output

    def __lt__(self, other) -> bool:
        if HOSTER_SORTING.index(self.hoster) != HOSTER_SORTING.index(other.hoster):
            return HOSTER_SORTING.index(self.hoster) < HOSTER_SORTING.index(other.hoster)
        return self.resolution < other.resolution

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
            self.uploads.sort()

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
        self.uploads.sort()
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

    def disableUpload(self, uploadId):
        for u in self.uploads:
            if u.id == uploadId:
                u.enabled = False

    def enableUpload(self, uploadId: str):
        for u in self.uploads:
            if u.id == uploadId:
                u.enabled = True


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

    def getVideo(self, id):
        for v in self.videos:
            if str(v.id) == str(id):
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

    def writePlaylist(self, playlist):
        f = open(
            COLLECTIONS_PLAYLISTS_LOCATION + playlist.short + ".md",
            "w"
        )
        f.write("---\n")
        f.write("layout: playlist\n")
        f.write("title: \"{}\"\n".format(playlist.title))
        f.write("permalink: /{}/\n".format(playlist.short))
        f.write("playlist: \"{}\"\n".format(playlist.short))
        f.write("---\n")
        f.close()

    def writeVideo(self, playlist, video, nextI, lastI):
        f = open(
            COLLECTIONS_VIDEOS_LOCATION + playlist.short + "_{}.md".format(video.id),
            "w"
        )
        f.write("---\n")
        f.write("layout: video\n")

        if video.title:
            f.write("title: \"{}\"\n".format(video.title))
        else:
            f.write("title: \"{} Teil {}\"\n".format(playlist.title, str(int(video.id))))
        f.write("permalink: /" + playlist.short + "/{}/\n".format(video.id))
        f.write("playlist: \"{}\"\n".format(playlist.short))
        f.write("part: \"{}\"\n".format(video.id))

        if nextI >= 0:
            f.write("nextVideoI: {}\n".format(nextI))
        if lastI >= 0:
            f.write("prevVideoI: {}\n".format(lastI))

        f.write("---\n")
        f.close()

    def writeCollections(self):
        print("[storage] Cleaning up...")
        # delete everything
        for directory in ["_playlists", "_videos"]:
            shutil.rmtree(directory)
            os.mkdir(directory)

        print("[storage] Generating collections...")
        for playlist in self.playlists:
            self.writePlaylist(playlist)
            i: int = 0
            for video in playlist.videos:
                last: int = -1
                next: int = -1
                if i > 0:
                    last = i - 1
                if i < len(playlist.videos) - 1:
                    next = i + 1

                if not video.available_soon:
                    if playlist.newest_first:
                        self.writeVideo(playlist, video, last, next)
                    else:
                        self.writeVideo(playlist, video, next, last)
                i += 1

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.toJsonSerializable(), f, indent=4)
            f.write("\n")

        self.writeCollections()

    def getPlaylistByName(self, name: str):
        for p in self.playlists:
            if p.short == name or p.name == name:
                return p
    
    def getVideoFilenameBase(self, video, upload, playlist=None):
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

    def getVideoFilename(self, video: Video, upload: Upload, playlist: Playlist | None = None):
        container = upload.container if upload.container else upload.id.split('.')[-1]
        match container:
            case "mkv" | "mp4" | "webm":
                pass
            case _:
                raise Exception("Invalid container")
        return self.getVideoFilenameBase(video, upload, playlist) + "." + container


if __name__ == "__main__":
    db = Database()
    #print(db.toJsonSerializable())
    db.save()
