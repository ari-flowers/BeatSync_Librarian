import os
import argparse
from analyzer import analyze_album
from scanner import scan_music_directory
from utils import (
    save_log_entry,
    sanitize_folder_name,
    load_config,
)
from rich.console import Console
from rich.table import Table

console = Console()


def rename_albums(paths, config, dry_run=False, export_path=None):
    all_albums = {}
    for path in paths:
        all_albums.update(scan_music_directory(path, config))

    rows = []
    for folder_path, files in all_albums.items():
        result = analyze_album(folder_path, files)
        original_name = os.path.basename(folder_path)
        artist = result.get("artist") or "Unknown Artist"
        title = result.get("title") or "Unknown Title"
        label = result.get("label")
        catalog = result.get("catalog")
        year = result.get("year")

        new_name_parts = [f"{artist} - {title}"]

        if label:
            new_name_parts.append(f"[{label}]")
        if catalog:
            new_name_parts.append(f"[{catalog}]")
        if year:
            new_name_parts.append(f"[{year}]")

        new_name = " ".join(new_name_parts)
        new_name = sanitize_folder_name(new_name)

        rows.append((original_name, new_name))

        if not dry_run:
            new_path = os.path.join(os.path.dirname(folder_path), new_name)
            try:
                os.rename(folder_path, new_path)
                console.print(f"[green]✓ Renamed:[/green] {original_name} -> {new_name}")
                if export_path:
                    save_log_entry(export_path, original_name, new_name, status="renamed")
            except Exception as e:
                console.print(f"[red]✗ Error renaming {original_name}:[/red] {e}")
                if export_path:
                    save_log_entry(export_path, original_name, new_name, status=f"error: {e}")
        else:
            if export_path:
                save_log_entry(export_path, original_name, new_name, status="dry-run")

    if dry_run:
        print_dry_run_table(rows)


def print_dry_run_table(rows):
    table = Table(title="Folder Renames", show_lines=True, expand=True)
    table.add_column("Original Folder", style="cyan", overflow="fold")
    table.add_column("New Folder Name", style="green", overflow="fold")
    table.add_column("Status", style="magenta", justify="center")

    for original, new in rows:
        table.add_row(original, new, "👀 Dry Run")

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Rename music folders based on metadata.")
    parser.add_argument("paths", nargs="+", help="Paths to scan.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without renaming.")
    parser.add_argument("--export-log", help="Optional log file path.")

    args = parser.parse_args()
    config = load_config()
    rename_albums(args.paths, config, dry_run=args.dry_run, export_path=args.export_log)


if __name__ == "__main__":
    main()