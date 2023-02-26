#!/usr/bin/env python3

import argparse
import os

import storage
import downloader
import plugins.archive
import plugins.dropbox
import plugins.dailymotion
import plugins.openload
import plugins.twitch
import plugins.u6656
import plugins.vimeo
import plugins.youtube
import plugins.dummy

from makesprites import SpriteTask

SYNCHROLOAD_PLUGINS = {
    "archive": plugins.archive,
    "dropbox": plugins.dropbox,
    "dailymotion": plugins.dailymotion,
    "openload": plugins.openload,
    "twitch": plugins.twitch,
    "u6656": plugins.u6656,
    "vimeo": plugins.vimeo,
    "youtube": plugins.youtube,
    
    "dummy": plugins.dummy
}

parser = argparse.ArgumentParser(description="SynchroLoad: Manage duraphilms.tk sources")
parser.add_argument("action", type=str)
parser.add_argument("--part", type=str)
parser.add_argument("--playlist", type=str)
parser.add_argument("--hoster", type=str)
parser.add_argument("--resolution", type=int, default=-1)
parser.add_argument("--delete-offline", action="store_true")

args = parser.parse_args()

db = storage.Database()

def pluginByName(pluginName):
    return SYNCHROLOAD_PLUGINS[pluginName]

def check_availability(video, upload, playlist, part):
    plugin = SYNCHROLOAD_PLUGINS[upload.hoster]
    print("[check online] {} {} on {} ({}) ...".format(playlist.name, part, plugin.HOSTER_NAME, upload.id), end="", flush=True)
    if not downloader.check_availability(plugin.linkFromId(upload.id)):
        if plugin.HOSTER_KEEP_UNAVAILABLE_UPLOADS:
            print(" [FAIL] - Disabling!")
            video.disableUpload(upload.id)
        else:
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
    return "", ""

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

def getUpload(video, hoster, resolution):
    upload = video.getUpload(args.hoster, args.resolution)
    if upload:
        return upload

    print("No upload for this hoster: " + args.hoster)
    exit(1)

def importU6656(playlist):
    baseId = "hpudpva"
    if playlist == "OdP":
        baseId = "hpudodp"

    plist = getPlaylist(playlist)
    for video in plist.videos:
        upl = storage.Upload()
        upl.hoster = "u6656"
        upl.id = baseId + "/" + video.id + ".mp4"
        upl.origin = "youtube"
        upl.resolution = 720

        video.uploads.append(upl)

if __name__ == "__main__":
    match args.action:
        case "delete-offline":
            for playlist in db.playlists:
                for video in playlist.videos:
                    for upload in video.uploads:
                        check_availability(video, upload, playlist, video.id)

            db.save()

        case "download":
            playlist = getPlaylist(args.playlist)
            video = getVideo(playlist, args.part)
            upload = getUpload(video, args.hoster, args.resolution)

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

        case "upload":
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

        case "gen-vtt":
            playlist = getPlaylist(args.playlist)
            video = getVideo(playlist, args.part)

            source = ""

            if args.hoster:
                upload = getUpload(video, args.hoster, args.resolution)

                plugin = pluginByName(args.hoster)
                url = plugin.linkFromId(upload.id)
                source = url
            else:
                (upload, fileName) = findLocalVideo(playlist, video)
                source = fileName

            task = SpriteTask(source)
            task.vttfile = "thumbs/vtt/{}_{}.vtt".format(playlist.name, video.id)
            task.spritefile = "thumbs/vtt/{}_{}.jpg".format(playlist.name, video.id)
            task.thumb_rate_seconds = 5
            task.thumb_width = 200
            task.outdir = "/tmp/spritesgen"
            task.use_sips = False

            task.makeOutDir("/tmp/spritesgen")

            task.run()

        case _:
            print(f"What do you mean by {args.action}?")
            exit(1)

    db.save()
