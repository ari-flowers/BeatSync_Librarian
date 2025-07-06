from mutagen import File

def analyze_track(file_path):
    audio = File(file_path, easy=True)
    if audio is None:
        return None

    tags = {
        'title': audio.get('title', [None])[0],
        'artist': audio.get('artist', [None])[0],
        'album': audio.get('album', [None])[0],
        'track': audio.get('tracknumber', [None])[0],
        'duration': int(audio.info.length) if audio.info else None,
        'bitrate': getattr(audio.info, 'bitrate', None),
        'format': file_path.split('.')[-1].lower(),
        'filename': file_path
    }

    return tags