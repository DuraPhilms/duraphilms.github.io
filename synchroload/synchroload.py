#!/usr/bin/env python3

import json
import argparse
import os

import storage
import downloader
import plugins.archive
import plugins.dropbox
import plugins.openload
import plugins.vimeo
import plugins.youtube

SYNCHROLOAD_PLUGINS = [
    plugins.archive,
    plugins.dropbox,
    plugins.openload,
    plugins.vimeo,
    plugins.youtube
]

parser = argparse.ArgumentParser(description='Synchronize ')
parser.add_argument("--insert", action="store_true", help='Adds a new video to the database')
parser.add_argument("--part", type=int, default=-1)
parser.add_argument("--playlist", type=str)
parser.add_argument("--hoster", type=str)
parser.add_argument("--download", action="store_true")
parser.add_argument("--upload", action="store_true")
parser.add_argument("--delete-offline", action="store_true")

args = parser.parse_args()

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
    options = ["Original", "Remake", "1080Rmk"]
    i = 0
    for x in options:
        i += 1
        print("{}: {}".format(str(i), x))

    version = -1
    while version < 0 or version > i:
        try:
            version = int(input("Select the version [1-{}]: ".format(i)))
        except ValueError:
            pass

    return options[version - 1]

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

if args.delete_offline:
    for playlistId in storage.getPlaylistIds():
        for part in storage.getVideos(playlist = playlistId):
            video = storage.getVideo(playlistId, part)
            for plugin in SYNCHROLOAD_PLUGINS:
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

if args.download or args.upload:
    video = storage.getVideo(storage.getPlaylistId(args.playlist), args.part)

    if video["hosters"]["youtube"]["version"] == "Original":
        filename = storage.getPlaylistName(playlist) + "_{0:0>2}".format(args.part)
    else:
        filename = storage.getPlaylistName(playlist) + "_{0:0>2}_".format(args.part) + video["hosters"]["youtube"]["version"]

    if video["hosters"]["youtube"]:
        if not downloader.download(video["hosters"]["youtube"]["id"], filename):
            print("Could not download video from youtube.")
            exit(1)

if args.upload:
    playlistName = storage.getPlaylistName(storage.getPlaylistId(args.playlist))
    filename = playlistName + "_{0:0>2}.".format(args.part)
    if os.path.isfile(filename + "mp4"):
        filename += "mp4"
    elif os.path.isfile(filename + "webm"):
        filename += "webm"
    elif os.path.isfile(filename + "mkv"):
        filename += "mkv"
    else:
        print("Could not find local file: " + filename + "{mp4,webm,mkv}.")
        exit(1)

    videoId = ""
    if args.hoster == "openload":
        videoId = plugins.openload.upload(filename)
    elif args.hoster == "dropbox":
        videoId = plugins.dropbox.upload(filename)
    elif args.hoster == "archive":
        videoId = plugins.archive.upload(filename)
    else:
        print("Could not upload: unknown hoster.")
        exit(1)

    if videoId:
        storage.setVideoId(storage.getPlaylistId(args.playlist), args.part, args.hoster, videoId)
        storage.saveDatabase()
