HOSTER_NAME = "onedrive"
HOSTER_HAS_DIRECT_LINKS = True
HOSTER_KEEP_UNAVAILABLE_UPLOADS = False


def linkFromId(id: str) -> str:
    return "https://onedrive.live.com/download?" + id