import internetarchive
import subprocess
import os
import random
import string

HOSTER_NAME = "archive"
HOSTER_HAS_DIRECT_LINKS = True

if not os.path.isfile(os.environ.get("HOME") + "/" + ".config/ia.ini"):
    subprocess.call(["ia", "configure"])

# get item name from environment; use default if nothing set
ARCHIVE_ITEM_NAME = os.getenv(
    "ARCHIVE_ITEM_NAME",
    "DuraphilmsSynchro_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=3))
)

# save item name for next execution
os.putenv("ARCHIVE_ITEM_NAME", ARCHIVE_ITEM_NAME)

def linkFromId(id):
    return "https://archive.org/download/" + id

def upload(filename):
    itemname = ARCHIVE_ITEM_NAME
    print("[archive] Uploading {}/{}...".format(itemname, filename))

    md = dict(title=itemname.upper(), mediatype='movies')
    r = internetarchive.upload(itemname, files=filename, metadata=md)

    print("[archive] Result {}".format(r[0].status_code))
    return "{}/{}".format(itemname, filename)
