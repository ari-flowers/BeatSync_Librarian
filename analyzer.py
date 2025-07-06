import os
from utils import (
    extract_metadata,
    clean_title,
    clean_artist_name,
    clean_label_name,
    extract_date_from_metadata,
    parse_album_folder_name,
)


def analyze_album(folder_path, files):
    # Extract metadata from all audio files in the folder
    metadata_list = [extract_metadata(os.path.join(folder_path, f)) for f in files]

    # Fallback parsing from folder name
    folder_fallback = parse_album_folder_name(folder_path)

    def pick_first_valid(field):
        for metadata in metadata_list:
            value = metadata.get(field)
            if value:
                return value
        return None

    artist = clean_artist_name(pick_first_valid("artist") or folder_fallback.get("artist"))
    title = clean_title(pick_first_valid("title") or folder_fallback.get("title"))
    label = clean_label_name(pick_first_valid("label"))
    year = extract_date_from_metadata(pick_first_valid("date") or "") or folder_fallback.get("year")
    catalog = folder_fallback.get("catalog")

    # Handle VA / Various Artists
    if artist and "various" in artist.lower():
        artist = "Various Artists"

    return {
        "artist": artist,
        "title": title,
        "label": label,
        "year": year,
        "catalog": catalog
    }