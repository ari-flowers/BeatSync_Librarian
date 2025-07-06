import os
import argparse
from config import load_config
from utils import (
    is_audio_file,
    parse_album_folder_name,
    sanitize_folder_name,
    capitalize_title,
    save_log_entry,
)

def rename_albums(paths, config, dry_run=False, export_path=None):
    for album_path in paths:
        print(f"\nAnalyzing: {album_path}")
        folder_meta = parse_album_folder_name(album_path)

        artist = folder_meta.get("artist") or "Unknown Artist"
        album = folder_meta.get("title") or "Unknown Album"
        year = folder_meta.get("year")
        catalog = folder_meta.get("catalog") if config.get("rename", {}).get("include_catalog", True) else None

        # Clean formatting
        artist = capitalize_title(artist)
        album = capitalize_title(album)
        if config.get("clean_tokens", {}).get("remove_double_spaces"):
            album = album.replace("  ", " ")

        if config.get("clean_tokens", {}).get("trim_whitespace"):
            artist = artist.strip()
            album = album.strip()

        if config.get("rename", {}).get("skip_on_missing_metadata", False) and (not artist or not album):
            print("⚠️  Skipping due to missing required metadata.")
            continue

        # Final name generation
        new_folder_name = config["folder_format"].format(
            artist=artist,
            album=album,
            year=year if year else "",
            catalogue=catalog if catalog else "",
        ).strip()

        new_folder_name = sanitize_folder_name(new_folder_name)
        new_path = os.path.join(os.path.dirname(album_path), new_folder_name)

        status = "Dry Run" if dry_run else "Renamed"

        print(f"👀 {status}: '{album_path}' -> '{new_path}'")
        if export_path:
            save_log_entry(export_path, album_path, new_path, status)

        if not dry_run:
            os.rename(album_path, new_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BeatSync Librarian - Folder Renamer")
    parser.add_argument("paths", nargs="+", help="Paths to album folders to rename")
    parser.add_argument("--dry-run", action="store_true", help="Preview renames without changing files")
    parser.add_argument("--export-log", help="Export log file to given path")

    args = parser.parse_args()

    config = load_config("config.yaml")
    rename_albums(args.paths, config, dry_run=args.dry_run, export_path=args.export_log)