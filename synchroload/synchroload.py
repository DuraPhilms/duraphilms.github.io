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
import plugins.twitch
import plugins.vimeo
import plugins.youtube
import plugins.dummy

SYNCHROLOAD_PLUGINS = {
    "archive": plugins.archive,
    "dropbox": plugins.dropbox,
    "dailymotion": plugins.dailymotion,
    "openload": plugins.openload,
    "twitch": plugins.twitch,
    "vimeo": plugins.vimeo,
    "youtube": plugins.youtube,
    
    "dummy": plugins.dummy
}

parser = argparse.ArgumentParser(description='Synchronize ')
parser.add_argument("--part", type=int, default=-1)
parser.add_argument("--playlist", type=str)
parser.add_argument("--hoster", type=str, default="youtube")
parser.add_argument("--download", action="store_true")
parser.add_argument("--upload", action="store_true")
parser.add_argument("--delete-offline", action="store_true")

args = parser.parse_args()

db = storage.Database()

def pluginByName(pluginName):
    return SYNCHROLOAD_PLUGINS[pluginName]

def check_availability(video, upload, playlist, part):
    plugin = SYNCHROLOAD_PLUGINS[upload.hoster]
    print("[check online] Checking availability for {} {} on {} ({}) ...".format(playlist.name, part, plugin.HOSTER_NAME, upload.id), end="")
    if not downloader.check_availability(plugin.linkFromId(upload.id)):
        print(" [FAIL] - Removing!")
        video.removeUpload(upload.id)
    else:
        print(" [OK]")

def findLocalVideo(playlist, video, version = None, resolution = None, containers = ["mp4", "webm", "mkv"]):
    if version:
        versions = [version]
    else:
        versions = storage.VIDEO_VERSIONS

    if resolution:
        resolutions = [resolution]
    else:
        resolutions = [2160, 1440, 1080, 720, 540, 480, 360, 240, 144]

    upload = storage.Upload()
    for version in versions:
        upload.version = version
        for resolution in resolutions:
            upload.resolution = resolution

            base = db.getVideoFilenameBase(video, upload, playlist = playlist)

            for container in containers:
                fileName = base + "." + container
                if os.path.isfile(fileName):
                    return upload, fileName
    return ""

def getPlaylist(playlistName):
    playlist = db.getPlaylistByName(playlistName)
    if playlist:
        return playlist

    print("No such playlist: " + playlistName)
    exit(1)

def getVideo(playlist, part):
    video = playlist.getVideo(part)
    if video:
        return video

    print("No such video: " + str(part))
    exit(1)

def getUpload(video, hoster):
    upload = video.getUpload(args.hoster)
    if upload:
        return upload

    print("No upload for this hoster: " + args.hoster)
    exit(1)

if __name__ == "__main__":
    if args.delete_offline:
        for playlist in db.playlists:
            for video in playlist.videos:
                for upload in video.uploads:
                    check_availability(video, upload, playlist, video.id)

        db.save()

    if args.download:
        playlist = getPlaylist(args.playlist)
        video = getVideo(playlist, args.part)
        upload = getUpload(video, args.hoster)

        plugin = pluginByName(args.hoster)
        url = plugin.linkFromId(upload.id)

        filename = db.getVideoFilenameBase(video, upload, playlist = playlist)

        if plugin.HOSTER_HAS_DIRECT_LINKS:
            download = downloader.downloadDirect(url, filename)
        else:
            download = downloader.download(url, filename)

        if download:
            print("Downloaded video to: {}".format(download))
        else:
            print("Could not download video from {}.".format(plugin.HOSTER_NAME))
            exit(1)

    if args.upload:
        plugin = pluginByName(args.hoster)
        if not plugin:
            print("Could not upload: unknown hoster.")
            exit(1)

        playlist = getPlaylist(args.playlist)
        video = getVideo(playlist, args.part)
        (upload, fileName) = findLocalVideo(playlist, video)

        upload.hoster = args.hoster
        upload.id = plugin.upload(fileName)

        if upload.id:
            video.uploads.append(upload)

    db.save()
