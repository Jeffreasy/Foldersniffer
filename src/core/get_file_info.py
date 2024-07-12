import os
import stat
import time

def get_file_info(file_path):
    file_info = os.stat(file_path)
    
    size = file_info.st_size
    last_modified = time.ctime(file_info.st_mtime)
    created = time.ctime(file_info.st_ctime)
    mode = stat.filemode(file_info.st_mode)
    owner = file_info.st_uid  # UID van de eigenaar

    return {
        "size": size,
        "last_modified": last_modified,
        "created": created,
        "mode": mode,
        "owner": owner,
        "path": file_path
    }

def detect_modification_type(old_info, new_info):
    if old_info['size'] != new_info['size']:
        return "content modified"
    elif old_info['last_modified'] != new_info['last_modified']:
        return "metadata modified"
    elif old_info['mode'] != new_info['mode'] or old_info['owner'] != new_info['owner']:
        return "permission changed"
    return "modified"
