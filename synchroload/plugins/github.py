import requests
import json
import os

import magic

HOSTER_NAME = "github"
HOSTER_HAS_DIRECT_LINKS = True
HOSTER_KEEP_UNAVAILABLE_UPLOADS = False

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_OWNER = os.getenv("GITHUB_OWNER", "duramedia")
GITHUB_REPO = os.getenv("GITHUB_REPO", "synchro")

def upload(filename):
    url = "https://api.github.com/repos/{}/{}/releases".format(GITHUB_OWNER, GITHUB_REPO)
    print(url)
    releaseCreate = {
        "tag_name": filename.split(".")[0]
    }
    
    result = requests.post(
        url,
        headers = {
            "Authorization": "token {}".format(GITHUB_TOKEN)
        },
        data = json.dumps(releaseCreate)
    )

    release = json.loads(result.text)
    print(release)

    url = "https://uploads.github.com/repos/{}/{}/releases/{}/assets?name={}".format(GITHUB_OWNER, GITHUB_REPO, release["id"], filename)
    result = requests.post(
        url,
        headers = {
            "Authorization": "token {}".format(GITHUB_TOKEN),
            "Content-Type": magic.Magic(mime=True).from_file(filename)
        },
        files = {
            "": open(filename, "rb")
        }
    )
    print(result)
    
