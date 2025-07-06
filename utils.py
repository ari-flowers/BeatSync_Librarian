import os
import re
from datetime import datetime
from mutagen import File as MutagenFile


AUDIO_EXTENSIONS = {'.mp3', '.flac', '.wav', '.aiff', '.ogg', '.m4a'}


def is_audio_file(filename, config):
    ext = os.path.splitext(filename)[1].lower().lstrip(".")
    return ext in config.get("file_extensions", [])


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


def extract_metadata(filepath):
    try:
        audio = MutagenFile(filepath, easy=True)
        if audio is None:
            return {}

        return {
            "artist": audio.get("artist", [None])[0],
            "title": audio.get("title", [None])[0],
            "label": audio.get("label", [None])[0],
            "date": audio.get("date", [None])[0],
        }
    except Exception as e:
        print(f"Error reading metadata from {filepath}: {e}")
        return {}


def extract_date_from_metadata(date_str):
    # Normalize to year only
    if not date_str:
        return None
    match = re.match(r'(\d{4})', date_str)
    return match.group(1) if match else None


def clean_title(title):
    if not title:
        return None
    return re.sub(r'\s+', ' ', title).strip()


def clean_artist_name(name):
    if not name:
        return None
    name = name.strip()
    if name.lower() in ["va", "various", "various artists"]:
        return "Various Artists"
    return name


def clean_label_name(name):
    if not name:
        return None
    return re.sub(r'\s+', ' ', name).strip()


def sanitize_folder_name(name):
    return re.sub(r'[\\/:*?"<>|]', '', name).strip()


def save_log_entry(log_path, original, new, status):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    timestamp = datetime.now().isoformat()
    with open(log_path, 'a') as f:
        f.write(f"[{timestamp}] {status.upper()}: '{original}' -> '{new}'\n")