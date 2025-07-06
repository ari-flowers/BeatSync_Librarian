import yaml
import os
import logging

DEFAULT_CONFIG = {
    "folder_format": "{artist} - {album} [{catalogue}][{year}]",
    "track_format": "{track:02d} - {title}.{ext}",
    "fallbacks": {
        "artist": ["track_artist", "album_artist", "folder_guess"],
        "title": ["title_tag", "filename_guess"],
        "album": ["album_tag", "parent_folder"],
        "year": ["year_tag", "folder_guess"],
        "catalogue": ["catalogue_tag", "folder_guess"],
        "track": ["track_tag", "filename_guess"]
    },
    "dry_run": True,
    "rename_tracks": True,
    "rename_folders": True,
    "interactive": False,
    "skip_on_missing_metadata": True,
    "fail_on_conflict": True,
    "clean_tokens": {
        "enabled": True,
        "remove_double_spaces": True,
        "trim_whitespace": True,
        "replace_illegal_chars": True
    },
    "rename_hidden_files": False,
    "file_extensions": ["flac", "mp3", "wav", "m4a", "aiff"],
    "log_changes": True,
    "log_path": "logs/rename.log"
}

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        print(f"⚠️ Config file not found at {config_path}. Using default config.")
        return DEFAULT_CONFIG

    with open(config_path, "r") as f:
        try:
            user_config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"❌ Error parsing config file: {e}")

    return merge_defaults(DEFAULT_CONFIG, user_config)


def merge_defaults(defaults, user_config):
    if isinstance(defaults, dict):
        merged = {}
        for key, val in defaults.items():
            if key in user_config:
                merged[key] = merge_defaults(val, user_config[key])
            else:
                merged[key] = val
        for extra_key in user_config:
            if extra_key not in merged:
                merged[extra_key] = user_config[extra_key]
        return merged
    else:
        return user_config if user_config is not None else defaults


# Optional logger setup (could be expanded later)
def setup_logging(config):
    if not config.get("log_changes"):
        return

    log_path = config.get("log_path", "logs/rename.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logging.basicConfig(
        filename=log_path,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.info("Started logging rename session.")