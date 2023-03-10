HOSTER_NAME = "gdrive"
HOSTER_HAS_DIRECT_LINKS = True
HOSTER_KEEP_UNAVAILABLE_UPLOADS = False


def linkFromId(id: str) -> str:
    return "https://drive.google.com/uc?export=download&id=" + id