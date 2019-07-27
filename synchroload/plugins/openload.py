import requests
import json

OPENLOAD_CO_UPLOAD_URL = "https://api.openload.co/1/file/ul"

def linkFromId(id):
    return "https://openload.co/embed/" + id

def upload(filename):
    print("[openload] Requesting upload slot...")
    result = requests.get(OPENLOAD_CO_UPLOAD_REQUEST_URL)

    uploadSlot = json.loads(result.text)
    
    if uploadSlot["status"] != 200:
        print("Requesting upload failed.")
        return ""

    print("[openload] Starting upload...")
    result = requests.post(
        uploadSlot["result"]["url"],
        files = {
            "file1": open(filename, "rb")
        }
    )

    return json.loads(result.text)["result"]["id"]
