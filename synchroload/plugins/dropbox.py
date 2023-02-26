import dropbox
import os

HOSTER_NAME = "dropbox"
HOSTER_HAS_DIRECT_LINKS = True
HOSTER_KEEP_UNAVAILABLE_UPLOADS = False

CHUNK_SIZE = 4 * 1024 * 1024

def linkFromId(id):
    return "https://dl.dropboxusercontent.com/s/" + id

def upload(filename):
    """
    We could also use the "remote upload" from an archive.org url or something:
    https://dropbox-sdk-python.readthedocs.io/en/latest/api/dropbox.html#dropbox.dropbox.Dropbox.files_save_url
    """
    DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN", "")
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)

    print("[dropbox] Uploading {}...".format(filename))
    f = open(filename, "rb")
    file_size = os.path.getsize(filename)

    dest_path = "/" + filename

    upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))

    cursor = dropbox.files.UploadSessionCursor(
        session_id=upload_session_start_result.session_id,
        offset=f.tell()
    )

    commit = dropbox.files.CommitInfo(path=dest_path)

    while f.tell() < file_size:
        if (file_size - f.tell()) <= CHUNK_SIZE:
            # print
            dbx.files_upload_session_finish(
                f.read(CHUNK_SIZE),
                cursor,
                commit
            )
        else:
            dbx.files_upload_session_append_v2(
                f.read(CHUNK_SIZE),
                cursor
            )
            cursor.offset = f.tell()

    print("[dropbox] Creating shared link...")
    return dbx.sharing_create_shared_link(dest_path).url.replace("https://www.dropbox.com/s/", "").replace("?dl=0", "")
