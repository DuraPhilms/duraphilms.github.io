import yt_dlp
import urllib.error
import ffmpeg
import json
import requests


def check_availability(url):
    try:
        yt_dlp.YoutubeDL({"quiet": True}).extract_info(
            url,
            download=False
        )
    except urllib.error.HTTPError:
        return False
    except yt_dlp.utils.ExtractorError:
        return False
    except yt_dlp.utils.DownloadError: # Copyright
        return False
    except KeyboardInterrupt:
        print("Aborting.")
        exit(1)
    except:
        return False
    return True


def download(url, basename):
    fullname = basename + ".mkv"
    ydl = yt_dlp.YoutubeDL({
        'format': "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo[ext=webm]+bestaudio[ext=webm]",
        'outtmpl': fullname,
        "merge_output_format": "mkv"
    })

    try:
        ydl.extract_info(url)
    except urllib.error.HTTPError:
        return ""
    except yt_dlp.utils.ExtractorError:
        return ""
    except yt_dlp.utils.DownloadError: # Copyright
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


def downloadDirect(url: str, filename: str) -> str:
    print(f"[downloader] Downloading {url} -> {filename}…")

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return filename
