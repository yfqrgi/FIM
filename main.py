import hashlib
import os
import json
import time
import argparse

BASELINE_FILE = 'baseline.json'

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        print("File not found")
        return None

def create_baseline(target_dir):
    baseline = {}
    print(f"[+] Creating Baseline for folder '{target_dir}'...")

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file == BASELINE_FILE:
                continue

            filepath = os.path.join(root, file)
            file_hash = get_file_hash(filepath)
            if file_hash:
                baseline[filepath] = file_hash

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print(f"Baseline saved: {len(baseline)} files written to {BASELINE_FILE}")


def check_integrity(filepath, original_hash):
    current_hash = get_file_hash(filepath)

    print(f"Old hash {original_hash}")
    print(f"Current hash {current_hash}")
    print('-'*50)

    if current_hash == original_hash:
        print("FILE ENTIRE: No change detected")
    else:
        print("WARNING: The file has been modified or corrupted!")

script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "example.txt")
original_hash = get_file_hash(filepath)

while True:
    if original_hash:
        print(f"Initial hash {original_hash}")
        check_integrity(filepath, original_hash)