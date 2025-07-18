import os
from utils import is_audio_file

def scan_music_directory(root_path, config):
    album_map = {}

    for dirpath, _, filenames in os.walk(root_path):
        if config.get("rename_hidden_files") is False:
            filenames = [f for f in filenames if not f.startswith(".")]

        audio_files = [f for f in filenames if is_audio_file(f, config)]
        if audio_files:
            full_paths = [os.path.join(dirpath, f) for f in audio_files]
            album_map[dirpath] = full_paths

    return album_map