import os
import subprocess
import logging

def process_files(root_path, prefix=None, suffix=None, action='d', 
                  rename_search="_en.srt", rename_replace=".srt", 
                  video_ext=".mp4", logger=None):
    """
    Recursively finds files under the given path that match the prefix or suffix,
    and allows the user to delete or rename them.
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    # Lazy import of moviepy to speed up non-duration actions
    if action == 'c':
        try:
            from moviepy import VideoFileClip
        except ImportError:
            logger.error("Error: 'moviepy' is required for duration calculation. Install it with 'pip install moviepy'.")
            return

    videosLength = 0
    for root, _, files in os.walk(root_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            
            # Filter logic
            matches_prefix = prefix is None or filename.startswith(prefix)
            matches_suffix = suffix is None or filename.endswith(suffix)
            
            if matches_prefix and matches_suffix and action != 'c':
                logger.info(f"Found file: {full_path}")
                while True:
                    if action == 'd':
                        confirm = input(f"Are you sure you want to delete '{full_path}'? (y/N): ").lower()
                        if confirm == 'y':
                            try:
                                os.remove(full_path)
                                logger.info(f"Deleted: {full_path}")
                                break
                            except PermissionError:
                                logger.error(f"Permission denied: Could not delete {full_path}")
                                break
                            except OSError as e:
                                logger.error(f"Error deleting {full_path}: {e}")
                                break
                        else:
                            logger.info("Skipping deletion.")
                            break
                    elif action == 'r':
                        if filename.endswith(rename_search):
                            new_filename = filename.replace(rename_search, rename_replace)
                            new_full_path = os.path.join(root, new_filename)

                            try:
                                os.rename(full_path, new_full_path)
                                logger.info(f"Renamed: {full_path} -> {new_full_path}")
                            except OSError as e:
                                logger.error(f"Error renaming {full_path}: {e}")
                        break
                    elif action == 's':
                        logger.info(f"Skipped: {full_path}")
                        break
                    else:
                        logger.warning(f"Invalid action '{action}' for file {full_path}")
                        return
            elif action == 'c' and filename.endswith(video_ext):
                try:
                    video = VideoFileClip(full_path)
                    duration = video.duration
                    logger.info(f"{filename}: {duration} seconds")
                    video.close()
                    videosLength += duration
                except Exception as e:
                    logger.error(f"Error processing duration for {full_path}: {e}")
    
    if action == 'c':
        h = int(videosLength // 3600)
        m = int((videosLength % 3600) // 60)
        s = int(videosLength % 60)
        logger.info(f"\nOverall Duration: {h} Hours {m} Minutes {s} Seconds")
