import os
import re
from datetime import datetime

AUDIO_EXTENSIONS = {'.mp3', '.flac', '.wav', '.aiff', '.ogg', '.m4a'}


def is_audio_file(filename):
    return os.path.splitext(filename)[1].lower() in AUDIO_EXTENSIONS


def parse_album_folder_name(folder_path):
    folder_name = os.path.basename(folder_path)

    # Attempt to extract metadata using regex
    catalog_match = re.search(r'\[([A-Za-z0-9\-_.]+)\]', folder_name)
    year_match = re.search(r'\((\d{4})\)', folder_name)
    artist_title_match = re.search(r'^(?:\[.*\]\s*)?(.*?)-\s*(.*?)(?:\s*\[.*\])?(?:\s*\(.*\))?$', folder_name)

    return {
        "catalog": catalog_match.group(1) if catalog_match else None,
        "year": year_match.group(1) if year_match else None,
        "artist": artist_title_match.group(1).strip() if artist_title_match else None,
        "title": artist_title_match.group(2).strip() if artist_title_match else None
    }


def sanitize_folder_name(name):
    return re.sub(r'[\\/:*?"<>|]', '', name).strip()


def capitalize_title(s):
    if not s:
        return s
    return ' '.join(word.capitalize() if word.islower() else word for word in s.split())


def save_log_entry(log_path, original, new, status):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    timestamp = datetime.now().isoformat()
    with open(log_path, 'a') as f:
        f.write(f"[{timestamp}] {status.upper()}: '{original}' -> '{new}'\n")