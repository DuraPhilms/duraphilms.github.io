import youtube_dl
import urllib.error
import ffmpeg
import json

def check_availability(url):
    try:
        youtube_dl.YoutubeDL().extract_info(
            url,
            download=False
        )
    except urllib.error.HTTPError:
        return False
    except youtube_dl.utils.ExtractorError:
        return False
    except youtube_dl.utils.DownloadError: # Copyright
        return False
    except:
        return False
    return True

def download(url, basename):
    fullname = basename + ".mkv"
    ydl = youtube_dl.YoutubeDL({
        'format': "bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo[ext=mp4]+bestaudio[ext=m4a]",
        'outtmpl': fullname,
        "merge_output_format": "mkv"
    })

    try:
        ydl.extract_info(url)
    except urllib.error.HTTPError:
        return ""
    except youtube_dl.utils.ExtractorError:
        return ""
    except youtube_dl.utils.DownloadError: # Copyright
        return ""
    except:
        return ""

    probe = ffmpeg.probe(fullname)

    outputName = basename + "."
    if probe["streams"][0]["codec_name"] == "vp9":
        outputName += "webm"
    elif probe["streams"][0]["codec_name"] == "h264":
        outputName += "mp4"
    else:
        outputName += "mkv"

    inputStream = ffmpeg.input(fullname)
    outputStream = ffmpeg.output(
        inputStream,
        outputName,
        c="copy",
        movflags="+faststart",
        strict="-2"
    )

    ffmpeg.run(outputStream, overwrite_output=True)

    return outputName
