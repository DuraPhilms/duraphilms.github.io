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

from gen_vtt import VttConfig, generate_vtt_thumbnails
from image_optimization import compress_lossy

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

args = parser.parse_args()

db = storage.Database()

def pluginByName(pluginName):
    return SYNCHROLOAD_PLUGINS[pluginName]

def check_availability(video: storage.Video, upload: storage.Upload, playlist: storage.Playlist, part: str):
    indent = " " * len("[check-online]")

    plugin = SYNCHROLOAD_PLUGINS[upload.hoster]
    print(f"[check-online] {playlist.name} {part} on {plugin.HOSTER_NAME} ({upload.id})…")

    if not downloader.check_availability(plugin.linkFromId(upload.id)):
        if upload.enabled:
            if plugin.HOSTER_KEEP_UNAVAILABLE_UPLOADS:
                print(f"{indent} Upload is offline. Disabling.")
                video.disableUpload(upload.id)
            else:
                print(f"{indent} Upload is offline. Removing.")
                video.removeUpload(upload.id)
        else:
            print(f"{indent} Still offline.")
    else:
        if not upload.enabled:
            print(f"{indent} Upload is online again. Re-enabling.")
            video.enableUpload(upload.id)


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

def getPlaylist(playlistName) -> storage.Playlist:
    playlist = db.getPlaylistByName(playlistName)
    if playlist:
        return playlist

    print("No such playlist: " + playlistName)
    exit(1)

def getVideo(playlist, part) -> storage.Video:
    video = playlist.getVideo(part)
    if video:
        return video

    print("No such video: " + str(part))
    exit(1)

def getUpload(video, hoster, resolution) -> storage.Upload:
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
        case "check-online":
            hoster = args.hoster or None

            for playlist in db.playlists:
                for video in playlist.videos:
                    for upload in video.uploads:
                        if not hoster or hoster == upload.hoster:
                            check_availability(video, upload, playlist, video.id)

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

            vtt_filename = f"thumbs/vtt/{playlist.name}_{video.id}.vtt"
            thumb_image = f"thumbs/vtt/{playlist.name}_{video.id}"
            thumb_png = f"{thumb_image}.png"
            thumb_jpg = f"{thumb_image}.jpg"

            vtt_config = VttConfig(frame_delta=5, frame_width=200, referenced_image_filename=f"{playlist.name}_{video.id}.jpg")
            generate_vtt_thumbnails(source, thumb_png, vtt_filename, vtt_config)

            compress_lossy(thumb_png, thumb_jpg)

            # delete .png variant
            os.remove(thumb_png)

        case "build":
            pass

        case _:
            print(f"What do you mean by {args.action}?")
            exit(1)

    db.save()
