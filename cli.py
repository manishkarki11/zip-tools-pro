import argparse
from zip_manager import ZipManager
from rich.console import Console
from rich.table import Table
from logger import logger

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Powerful & Error-Free ZIP Tool")
    parser.add_argument('zipfile', help="Path to the ZIP file")
    parser.add_argument('--password', help="Password for archive", default=None)
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help="List files in the archive")

    extract = subparsers.add_parser('extract', help="Extract all files")
    extract.add_argument('output', help="Output directory")

    add = subparsers.add_parser('add', help="Add a file to archive")
    add.add_argument('filepath', help="File to add")
    add.add_argument('--arcname', help="Name inside archive", default=None)

    delete = subparsers.add_parser('delete', help="Delete a file from archive")
    delete.add_argument('filename', help="Filename inside archive to delete")

    search = subparsers.add_parser('search', help="Search file by keyword")
    search.add_argument('keyword', help="Keyword to search for")

    args = parser.parse_args()

    manager = ZipManager(args.zipfile, password=args.password)

    try:
        if args.command == 'list':
            files = manager.list_files()
            table = Table(title="Files in Archive")
            table.add_column("Filename", justify="left", style="cyan")
            for file in files:
                table.add_row(file)
            console.print(table)
        elif args.command == 'extract':
            manager.extract_all(args.output)
            console.print(f"[green]Extracted to {args.output}[/green]")
        elif args.command == 'add':
            manager.add_file(args.filepath, args.arcname)
            console.print(f"[green]Added {args.filepath}[/green]")
        elif args.command == 'delete':
            manager.delete_file(args.filename)
            console.print(f"[green]Deleted {args.filename}[/green]")
        elif args.command == 'search':
            matches = manager.search_file(args.keyword)
            if matches:
                for match in matches:
                    console.print(f"[blue]{match}[/blue]")
            else:
                console.print(f"[yellow]No matches found[/yellow]")
        else:
            parser.print_help()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logger.error(f"CLI command failed: {e}")

if __name__ == "__main__":
    main()
