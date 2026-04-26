import argparse
import sys
from .processor import process_files
from .logger import configureLogger

def main():
    parser = argparse.ArgumentParser(description="Easy File Manager - Manage files with prefix/suffix filters.")
    parser.add_argument("path", nargs='?', help="Path to the directory to process")
    parser.add_argument("--prefix", help="Prefix to filter by")
    parser.add_argument("--suffix", help="Suffix to filter by")
    parser.add_argument("--action", choices=['d', 'r', 'c', 's'], 
                        help="Action to perform: (d)elete, (r)ename, (c)alculate duration, (s)kip")
    parser.add_argument("--rename-search", help="Pattern to search for when renaming")
    parser.add_argument("--rename-replace", help="Replacement pattern when renaming")
    parser.add_argument("--video-ext", help="Video extension for duration calculation")

    args = parser.parse_args()

    # If path is not provided, enter interactive mode
    target_path = args.path
    if not target_path:
        target_path = input("Enter the path to the directory you want to process: ").strip()
        if not target_path:
            print("Error: Path is required.")
            sys.exit(1)

    prefix_filter = args.prefix
    if prefix_filter is None and not any(v in sys.argv for v in ["--prefix"]):
        prefix_filter = input("Enter the prefix to filter by (leave blank for none): ").strip() or None

    suffix_filter = args.suffix
    if suffix_filter is None and not any(v in sys.argv for v in ["--suffix"]):
        suffix_filter = input("Enter the suffix to filter by (leave blank for none): ").strip() or None

    action = args.action
    if not action:
        action = input("Choose action - (d)elete, (r)ename, (c)alculate duration, (s)kip: ").lower().strip()
        if action not in ['d', 'r', 'c', 's']:
            print("Error: Invalid action.")
            sys.exit(1)

    rename_search = args.rename_search or "_en.srt"
    rename_replace = args.rename_replace or ".srt"
    video_ext = args.video_ext or ".mp4"

    # Configure logger
    log = configureLogger('video_processor')
    
    log.info(f"Starting processing in: {target_path}")
    process_files(
        target_path, 
        prefix_filter, 
        suffix_filter, 
        action,
        rename_search=rename_search,
        rename_replace=rename_replace,
        video_ext=video_ext,
        logger=log
    )
    log.info("File processing complete.")

if __name__ == "__main__":
    main()
