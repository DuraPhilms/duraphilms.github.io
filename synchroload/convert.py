#!/usr/bin/env python3

import json

file = open("_data/videos.json", "r+")
videos = json.load(file)

for i in videos:
    for v in i["videos"].values():
        new_hosters = []

        for h in v["hosters"].keys():
            new_hosters.append({
                "hoster": h,
                "id": v["hosters"][h]["id"],
                "version": v["hosters"][h]["version"],
                "resolution": 720
            })
        
        v["hosters"] = new_hosters

file.seek(0)
file.write(json.dumps(videos,indent=4))
file.close()