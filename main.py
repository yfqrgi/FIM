import hashlib

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        print("File not found")
        return None

filepath = 'example.txt'
original_hash = get_file_hash(filepath)

if original_hash:
    print(f"Initial hash {original_hash}")