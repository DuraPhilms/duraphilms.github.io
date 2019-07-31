#!/usr/bin/env python3

import json
import argparse
import os

import storage
import downloader
import plugins.archive
import plugins.dropbox
import plugins.dailymotion
import plugins.openload
import plugins.vimeo
import plugins.youtube

SYNCHROLOAD_PLUGINS = {
    "archive": plugins.archive,
    "dropbox": plugins.dropbox,
    "dailymotion": plugins.dailymotion,
    "openload": plugins.openload,
    "vimeo": plugins.vimeo,
    "youtube": plugins.youtube
}

parser = argparse.ArgumentParser(description='Synchronize ')
parser.add_argument("--insert", action="store_true", help='Adds a new video to the database')
parser.add_argument("--part", type=int, default=-1)
parser.add_argument("--playlist", type=str)
parser.add_argument("--hoster", type=str, default="youtube")
parser.add_argument("--download", action="store_true")
parser.add_argument("--upload", action="store_true")
parser.add_argument("--delete-offline", action="store_true")

args = parser.parse_args()

def pluginByName(pluginName):
    return SYNCHROLOAD_PLUGINS[pluginName]

def selectPlaylist():
    i = 0
    for x in storage.getPlaylistTitles():
        i += 1
        print("{}: {}".format(str(i), x))

    playlistId = -1
    while playlistId < 0 or playlistId > i:
        try:
            playlistId = int(input("Select the playlist [1-{}]: ".format(i)))
        except ValueError:
            pass

    return playlistId - 1

def selectPart():
    partnumber = -1
    while partnumber < 0:
        try:
            partnumber = int(input("Part number: "))
        except ValueError:
            pass
    return partnumber

def selectVideoVersion():
    i = 0
    for x in storage.VIDEO_VERSIONS:
        i += 1
        print("{}: {}".format(str(i), x))

    version = -1
    while version < 0 or version > i:
        try:
            version = int(input("Select the version [1-{}]: ".format(i)))
        except ValueError:
            pass

    return storage.VIDEO_VERSIONS[version - 1]

def selectHosterIds():
    hosters = {}

    for hoster in ["youtube", "archive", "openload"]:
        videoId = input("Video ID on {}: ".format(hoster))
        if videoId:
            version = selectVideoVersion()
            hosters[hoster] = {"id": videoId, "version": version}

    return hosters

def check_availability(plugin):
    if plugin.HOSTER_NAME in video["hosters"] and video["hosters"][plugin.HOSTER_NAME]:
        print("[check online] Checking availability for {} {} on {}...".format(storage.getPlaylistName(playlistId), int(part), plugin.HOSTER_NAME))
        if not downloader.check_availability(plugin.linkFromId(video["hosters"][plugin.HOSTER_NAME]["id"])):
            print("[check online] {} {} on {} is not available: Removing...".format(storage.getPlaylistName(playlistId), int(part), plugin.HOSTER_NAME))
            storage.removeVideoHoster(playlistId, part, plugin.HOSTER_NAME)

def check_file_extension(basename, extension):
    if os.path.isfile(basename + "." + extension):
        return basename + "." + extension

def find_local_video(playlistId, part):
    filename = storage.getVideoFilenameBase(playlistId, part, "")

    versions = []
    for version in storage.VIDEO_VERSIONS:
        if version == "Original":
            versions.append("")
        else:
            versions.append("_" + version)

    for version in versions:
        for ext in ["mp4", "webm", "mkv"]:
            if check_file_extension(filename + version, ext):
                return "{}{}.{}".format(filename, version, ext)

    print("Could not find local file: " + filename + ".{mp4,webm,mkv}.")
    return ""

if args.delete_offline:
    for playlistId in storage.getPlaylistIds():
        for part in storage.getVideos(playlist = playlistId):
            video = storage.getVideo(playlistId, part)
            for plugin in SYNCHROLOAD_PLUGINS.values():
                check_availability(plugin)

    storage.saveDatabase()

if args.insert:
    playlist = selectPlaylist()

    newVideo = {}
    newVideo["part"] = selectPart()
    newVideo["version"] = selectVideoVersion()
    newVideo["hosters"] = selectHosterIds()

    storage.addVideo(playlist, newVideo)

    storage.saveDatabase()
    print("Added {} Teil {}!".format(DB[playlist]["title"], newVideo["part"]))

if args.download:
    video = storage.getVideo(storage.getPlaylistId(args.playlist), args.part)
    filename = storage.getVideoFilenameBase(storage.getPlaylistId(args.playlist), args.part, args.hoster)
    plugin = pluginByName(args.hoster)
    url = plugin.linkFromId(video["hosters"][args.hoster]["id"])

    if plugin.HOSTER_HAS_DIRECT_LINKS:
        download = downloader.downloadDirect(url, filename)
    else:
        download = downloader.download(url, filename)

    if download:
        print("Downloaded video to: {}".format(download))
    else:
        print("Could not download video from youtube.")
        exit(1)

if args.upload:
    filename = find_local_video(storage.getPlaylistId(args.playlist), args.part)

    videoId = ""
    plugin = pluginByName(args.hoster)
    if plugin:
        videoId = plugin.upload(filename)
    else:
        print("Could not upload: unknown hoster.")
        exit(1)

    version = filename.split("_")[-1].split(".")[0]
    if not version in storage.VIDEO_VERSIONS:
        version = "Original"

    if videoId:
        storage.setVideoId(storage.getPlaylistId(args.playlist), args.part, args.hoster, videoId, version)
        storage.saveDatabase()
