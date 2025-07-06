from rich.console import Console
from rich.table import Table

console = Console()

def print_album_report(album_data):
    for album_path, tracks in album_data.items():
        console.rule(f"[bold cyan]{album_path}")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Track")
        table.add_column("Title")
        table.add_column("Artist")
        table.add_column("Duration", justify="right")
        table.add_column("Format", justify="right")

        for track in tracks:
            if track is None:
                continue
            table.add_row(
                str(track.get("track") or "?"),
                track.get("title") or "—",
                track.get("artist") or "—",
                str(track.get("duration") or "?"),
                track.get("format") or "—"
            )

        console.print(table)