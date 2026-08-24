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

def monitor_integrity(target_dir, interval=3):
    if not os.path.exists(BASELINE_FILE):
        print(f"[!] {BASELINE_FILE} not found! First run --setup mode")
        return

    with open(BASELINE_FILE, 'r') as f:
        baseline = json.load(f)

    print(f"[=] Monitoring started (with interval {interval}s). To stop: Ctrl+C\n" + "-"*60)

    try:
        while True:
            for filepath, old_hash in baseline.items():
                if not os.path.exists(filepath):
                    print(f"[DELETED] File deleted {filepath}")
                else:
                    current_hash = get_file_hash(filepath)
                    if current_hash != old_hash:
                        print(f"[NEW FILE] New file added: {filepath}")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[=] Tracking stopped")

def main():
    parser = argparse.ArgumentParser(description="JSON-based File Integrity Monitor (FIM)")
    parser.add_argument("-d", "--dir", default=".", help="Folder to watch (Default: current folder)")  
    parser.add_argument("--setup", action="store_true", help="Create a new baseline (hash database)")  
    parser.add_argument("--monitor", action="store_true", help="Start file integrity monitoring)")
    parser.add_argument("-i", "--interval", type=int, default=3, help="Tracking interval in seconds (Default: 3s)")

    args = parser.parse_args()

    if args.setup:
        create_baseline(args.dir)
    elif args.monitor:
        monitor_integrity(args.dir, args.interval)
    else:
        print("Please select a mode: --setup (create a database) or --monitor (monitor)")
        print("Example: python fim.py --setup")


if __name__ == "__main__":
    main()