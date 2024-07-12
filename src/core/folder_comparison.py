import os
import filecmp
import difflib

def compare_folders(dir1, dir2):
    comparison = filecmp.dircmp(dir1, dir2)
    return {
        'common': comparison.common,
        'left_only': comparison.left_only,
        'right_only': comparison.right_only,
        'diff_files': comparison.diff_files,
        'funny_files': comparison.funny_files
    }

def compare_file_contents(file1, file2):
    with open(file1, 'r', encoding='utf-8', errors='ignore') as f1, \
         open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
        diff = list(difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file1, tofile=file2))
    return diff