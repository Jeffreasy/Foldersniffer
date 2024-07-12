import re
import os

def regex_search(directory, pattern, file_types=None):
    results = []
    regex = re.compile(pattern)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file_types and not any(file.endswith(ft) for ft in file_types):
                continue
            
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if regex.search(content):
                        results.append({
                            'path': file_path,
                            'matches': [m.group() for m in regex.finditer(content)]
                        })
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    
    return results