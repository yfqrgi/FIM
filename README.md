# Simple File Integrity Monitor (FIM)

A Python-based File Integrity Monitor that tracks directory changes in real-time by storing cryptographic SHA-256 hashes in a JSON baseline

## Features
- **SHA-256 Hashing:** Safe for large files using chunked reading
- **Persistent Storage:** Stores baseline hashes in `baseline.json`
- **Real-Time Detection:** Flags modified, deleted, or newly added files
- **CLI Control:** Easy switches to create baseline or start monitoring

## Quick Start

### 1. Create Baseline
Generates initial SHA-256 signatures for all files in the directory:
```bash
python fim.py --setup
```

## Start Live Monitoring

Monitors the directory every 3 seconds for modifications, deletions, or new files:
```bash
python fim.py --monitor
```

## Command Options

- -d, --dir : Target directory to monitor (Default: current directory .)

- --setup : Build/Overwrite baseline.json database

- --monitor : Run continuous integrity checks

- -i, --interval : Check interval in seconds (Default: 3)