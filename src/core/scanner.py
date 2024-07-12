import os
import logging
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def setup_logging(output_directory):
    log_filename = os.path.join(output_directory, f"scan_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(message)s')
    return log_filename

def scan_file(file_path, log_fields):
    try:
        file_info = {
            'type': 'file',
            'path': file_path,
            'size': os.path.getsize(file_path),
            'last_modified': time.ctime(os.path.getmtime(file_path)),
            'created': time.ctime(os.path.getctime(file_path)),
            'mode': oct(os.stat(file_path).st_mode),
            'owner': os.stat(file_path).st_uid,
            'extension': os.path.splitext(file_path)[1].lower(),
        }

        if log_fields.get('content', False):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_info['content'] = f.read()

        return file_info
    except Exception as e:
        logging.error(f"Error scanning file {file_path}: {e}")
        return None

def count_scannable_items(directory, ignore_files, ignore_dirs, file_types):
    count = 0
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs and os.path.join(root, d) not in ignore_dirs]
        for file in files:
            if file not in ignore_files and (not file_types or any(file.endswith(ft) for ft in file_types)):
                count += 1
    return count

def scan_directory(directory, output_directory, log_fields, ignore_files=None, ignore_dirs=None, file_types=None, progress_callback=None):
    log_filename = setup_logging(output_directory)
    
    if ignore_files is None:
        ignore_files = []
    if ignore_dirs is None:
        ignore_dirs = []
    if file_types is None:
        file_types = []

    total_items = count_scannable_items(directory, ignore_files, ignore_dirs, file_types)
    scanned_items = 0

    result_list = []

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        future_to_file = {}
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs and os.path.join(root, d) not in ignore_dirs]
            for file in files:
                if file not in ignore_files and (not file_types or any(file.endswith(ft) for ft in file_types)):
                    file_path = os.path.join(root, file)
                    future_to_file[executor.submit(scan_file, file_path, log_fields)] = file_path

        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                result = future.result()
                if result:
                    result_list.append(result)
                    logging.info(f"File: {result['path']}")
                    for field, value in result.items():
                        if field != 'path' and log_fields.get(field, False):
                            logging.info(f"{field.capitalize()}: {value}")
                    logging.info("")
            except Exception as exc:
                logging.error(f'{file_path} generated an exception: {exc}')
            
            scanned_items += 1
            if progress_callback:
                progress_callback(int((scanned_items / total_items) * 100))

    scan_summary = {
        'total_files': len(result_list),
        'total_size': sum(file['size'] for file in result_list),
        'file_types': {},
        'size_distribution': {
            '0-1KB': 0,
            '1KB-1MB': 0,
            '1MB-10MB': 0,
            '10MB-100MB': 0,
            '100MB+': 0
        }
    }

    for file in result_list:
        # Update file types count
        ext = file['extension']
        scan_summary['file_types'][ext] = scan_summary['file_types'].get(ext, 0) + 1

        # Update size distribution
        size = file['size']
        if size < 1024:
            scan_summary['size_distribution']['0-1KB'] += 1
        elif size < 1024 * 1024:
            scan_summary['size_distribution']['1KB-1MB'] += 1
        elif size < 10 * 1024 * 1024:
            scan_summary['size_distribution']['1MB-10MB'] += 1
        elif size < 100 * 1024 * 1024:
            scan_summary['size_distribution']['10MB-100MB'] += 1
        else:
            scan_summary['size_distribution']['100MB+'] += 1

    return log_filename, result_list, scan_summary

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory to scan: ")
    output_directory = input("Enter the output directory for the log: ")
    log_file, results, summary = scan_directory(directory_to_scan, output_directory, {'size': True, 'last_modified': True, 'created': True, 'mode': True, 'owner': True, 'content': False})
    print(f"Scan complete. Log file created at: {log_file}")
    print(f"Scan summary: {summary}")