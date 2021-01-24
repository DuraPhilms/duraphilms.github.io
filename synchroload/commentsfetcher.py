#!/usr/bin/env python3

import storage
import requests
import json
import os
import sys

INVIDIOUS_INSTANCE = "https://invidious.tube"
COMMENTS_ENDPOINT = "/api/v1/comments/"
COMMENTS_DATA = "_data/comments"


def mkdirIfMissing(path):
    if not os.path.isdir(path):
        os.mkdir(path)

class CreatorHeart:
    creatorThumbnail: str = ""
    creatorName: str = ""
    
    def __init__(self, structs = None):
        if not structs:
            return
        self.creatorThumbnail = structs["creatorThumbnail"]
        self.creatorName = structs["creatorName"]

    def toJsonSerializable(self) -> dict:
        output = {}
        output["creatorThumbnail"] = self.creatorThumbnail
        output["creatorName"] = self.creatorName
        return output

    def __bool__(self):
        return bool(self.creatorThumbnail) and bool(self.creatorName)

class AuthorThumbnail:
    url: str = ""
    width: int = 0
    height: int = 0
    
    def __init__(self, structs = None):
        if not structs:
            return
        self.url = structs["url"]
        self.width = structs["width"]
        self.height = structs["height"]

    def toJsonSerializable(self) -> dict:
        output = {}
        output["url"] = self.url
        output["width"] = self.width
        output["height"] = self.height
        return output

class Comment:
    author: str = ""
    authorThumbnails: list[AuthorThumbnail] = []
    authorId: str = ""
    authorUrl: str = ""
    isEdited: bool = False
    content: str = ""
    contentHtml: str = ""
    published: int = 0
    publishedText: str = ""
    likeCount: int = 0
    commentId: str = ""
    authorIsChannelOwner: bool = False
    creatorHeart: CreatorHeart = CreatorHeart()
    replyCount: int = 0

    def __init__(self, structs = None):
        self.authorThumbnails = []
        if not structs:
            return

        self.author = structs["author"]
        for thumb in structs["authorThumbnails"]:
            self.authorThumbnails.append(AuthorThumbnail(thumb))
        self.authorId = structs["authorId"]
        self.authorUrl = structs["authorUrl"]
        self.isEdited = structs["isEdited"]
        self.content = structs["content"]
        self.contentHtml = structs["contentHtml"]
        self.published = structs["published"]
        self.publishedText = structs["publishedText"]
        self.likeCount = structs["likeCount"]
        self.commentId = structs["commentId"]
        self.authorIsChannelOwner = structs["authorIsChannelOwner"]
        if "creatorHeart" in structs:
            self.creatorHeart = CreatorHeart(structs["creatorHeart"])
        if "replies" in structs:
            self.replyCount = structs["replies"]["replyCount"]
        # todo: replies/continuation

    def toJsonSerializable(self) -> dict:
        output = {}
        output["author"] = self.author
        output["authorThumbnails"] = []
        for t in self.authorThumbnails:
            output["authorThumbnails"].append(t.toJsonSerializable())
        output["authorId"] = self.authorId
        output["authorUrl"] = self.authorUrl
        output["isEdited"] = self.isEdited
        output["content"] = self.content
        output["contentHtml"] = self.contentHtml
        output["published"] = self.published
        output["publishedText"] = self.publishedText
        output["likeCount"] = self.likeCount
        output["commentId"] = self.commentId
        output["authorIsChannelOwner"] = self.authorIsChannelOwner
        if self.creatorHeart:
            output["creatorHeart"] = self.creatorHeart.toJsonSerializable()
        if self.replyCount:
            output["replies"] = {"replyCount": self.replyCount}
        return output

class VideoComments:
    videoId: str
    commentCount: int
    comments: list[Comment]
    continuation: str

    def __init__(self, structs = None):
        self.videoId = ""
        self.commentCount = 0
        self.continuation = ""
        self.comments = []

        if not structs:
            return

        self.videoId = structs["videoId"]
        if "commentCount" in structs:
            self.commentCount = structs["commentCount"]
        for comment in structs["comments"]:
            self.comments.append(Comment(comment))
        if "continuation" in structs:
            self.continuation = structs["continuation"]

    def toJsonSerializable(self) -> dict:
        output = {}
        output["videoId"] = self.videoId
        output["commentCount"] = self.commentCount
        output["comments"] = []
        for c in self.comments:
            output["comments"].append(c.toJsonSerializable())
        return output

    def __iadd__(self, other):
        self.videoId = self.videoId or other.videoId
        self.comments += other.comments
        self.commentCount = self.commentCount or other.commentCount
        return self

def videoFetchAllComments(videoId):
    comments = VideoComments()
    urlParams = {"hl": "de"}
    while True:
        try:
            print(".", end="", flush=True)
            response = requests.get(INVIDIOUS_INSTANCE + COMMENTS_ENDPOINT + videoId, params=urlParams)
            if response.status_code != 200:
                print("Error:", str(response.status_code))
                break

            parsedJson = json.loads(response.content.decode("utf-8"))

            currentPage = VideoComments(parsedJson)
            #print(currentPage.continuation)
            comments += currentPage

            urlParams["continuation"] = currentPage.continuation
            if not currentPage.continuation:
                print("")
                break
        except json.decoder.JSONDecodeError:
            print("json.decoder.JSONDecodeError:")
            print(response.content.decode("utf-8"))
            break
    return comments

def fetchComments():
    db = storage.Database()
    
    # create _data/comments folder
    mkdirIfMissing(COMMENTS_DATA)

    for playlist in db.playlists:
        for video in playlist.videos:
            videoCommentsFilePath = COMMENTS_DATA + "/" + playlist.short + "_" + video.id + ".json"
            # write empty comments
            if not os.path.isfile(videoCommentsFilePath):
                with open(videoCommentsFilePath, 'w') as f:
                    json.dump(VideoComments().toJsonSerializable(), f, indent=4)
                    f.write("\n")

            # search for youtube upload
            for upload in video.uploads:
                if upload.hoster == "youtube":
                    print("Fetching comments for {}/{} (https://www.youtube.com/watch?v={})".format(playlist.short, video.id, upload.id))
                    comments = videoFetchAllComments(upload.id)

                    # check whether comments could be loaded
                    #print(len(comments.comments))
                    if len(comments.comments) > 0:
                        # write to disk
                        with open(videoCommentsFilePath, "w") as f:
                            json.dump(comments.toJsonSerializable(), f, indent=0, ensure_ascii=False)
                            f.write("\n")

                    # do not load comments of any other youtube uploads (maybe
                    # this could be changed later)
                    break

if __name__ == "__main__":
    fetchComments()
