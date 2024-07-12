import mimetypes
import math

def calculate_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x])))/len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def is_likely_encrypted(file_path):
    try:
        file_type, _ = mimetypes.guess_type(file_path)
        
        if file_type and ('text' in file_type or 'empty' in file_type):
            return False

        with open(file_path, 'rb') as f:
            data = f.read(1024)  # Read first 1KB of file
        
        entropy = calculate_entropy(data)
        
        # High entropy (> 7.5) often indicates encryption or compression
        return entropy > 7.5
    except Exception as e:
        print(f"Error analyzing file {file_path}: {e}")
        return False