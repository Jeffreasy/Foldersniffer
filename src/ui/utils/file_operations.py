import json
import os
import zipfile

def export_as_json(scan_results, output_directory):
    with open(os.path.join(output_directory, 'scan_results.json'), 'w') as f:
        json.dump(scan_results, f, indent=4)

def export_as_txt(results, output_directory):
    output_file = os.path.join(output_directory, "scan_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(f"Path: {result['path']}\n")
            f.write(f"Size: {result['size']}\n")
            f.write(f"Last Modified: {result['last_modified']}\n")
            f.write(f"Created: {result['created']}\n")
            f.write(f"Mode: {result['mode']}\n")
            f.write(f"Owner: {result['owner']}\n")
            f.write(f"Content:\n{result['content']}\n\n")

def export_as_zip(scan_results, output_directory):
    json_path = os.path.join(output_directory, 'scan_results.json')
    txt_path = os.path.join(output_directory, 'scan_results.txt')

    export_as_json(scan_results, output_directory)
    export_as_txt(scan_results, output_directory)

    with zipfile.ZipFile(os.path.join(output_directory, 'scan_results.zip'), 'w') as zipf:
        zipf.write(json_path, os.path.basename(json_path))
        zipf.write(txt_path, os.path.basename(txt_path))
