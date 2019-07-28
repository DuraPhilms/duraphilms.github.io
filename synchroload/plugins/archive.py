import internetarchive
import subprocess
import os
import random
import string

HOSTER_NAME = "archive"

if not os.path.isfile(os.environ.get("HOME") + "/" + ".config/ia.ini"):
    subprocess.call(["ia", "configure"])

def linkFromId(id):
    return "https://archive.org/download/" + id

def upload(filename):
    itemname = "DuraPhilmsSynchro_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=3))
    print("[archive] Uploading {}/{}...".format(itemname, filename))

    md = dict(title=itemname.upper(), mediatype='movies')
    r = internetarchive.upload(itemname, files=filename, metadata=md)

    print("[archive] Result {}".format(r[0].status_code))
    return "{}/{}".format(itemname, filename)
