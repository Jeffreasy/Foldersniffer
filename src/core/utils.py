import os
import time
import logging

def get_file_info(file_path):
    try:
        size = os.path.getsize(file_path)
        last_modified = time.ctime(os.path.getmtime(file_path))
        created = time.ctime(os.path.getctime(file_path))
        mode = oct(os.stat(file_path).st_mode)
        owner = os.stat(file_path).st_uid

        num_lines, num_chars = 0, 0
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                num_lines += 1
                num_chars += len(line)

        file_info = {
            'path': file_path,
            'size': size,
            'last_modified': last_modified,
            'created': created,
            'mode': mode,
            'owner': owner,
            'num_lines': num_lines,
            'num_chars': num_chars
        }
        return file_info

    except Exception as e:
        logging.error(f"Error getting file info for {file_path}: {e}")
        return None
