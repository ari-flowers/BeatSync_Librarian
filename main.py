import sys
from scanner import scan_music_directory
from analyzer import analyze_track
from reporter import print_album_report

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_music_folder>")
        return

    music_path = sys.argv[1]
    album_map = scan_music_directory(music_path)

    analyzed_data = {}
    for album_path, files in album_map.items():
        analyzed_data[album_path] = [analyze_track(f) for f in files]

    print_album_report(analyzed_data)

if __name__ == "__main__":
    main()