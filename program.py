import os
from moviepy import VideoFileClip
import subprocess
from logger import configureLogger


def process_files(root_path, prefix=None, suffix=None, action='d'):
    """
    Recursively finds files under the given path that match the prefix or suffix,
    and allows the user to delete or rename them.
    """
    videosLength = 0
    for root, _, files in os.walk(root_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            if (prefix is None or filename.startswith(prefix)) and \
               (suffix is None or filename.endswith(suffix)) and action != 'c':
                print(f"\nFound file: {full_path}")
                while True:
                    # action = input("Do you want to (D)elete, (R)ename, or (S)kip? (d/r/s): ").lower()
                    if action == 'd':
                        # input(f"Are you sure you want to delete '{full_path}'? (y/N): ").lower()
                        confirm = 'y'
                        if confirm == 'y':
                            try:
                                os.remove(full_path)
                                print(f"Deleted: {full_path}")
                                break
                            except FileNotFoundError:
                                print(f"Error: File not found - {full_path}")
                                break
                            except PermissionError:
                                print(
                                    f"Error: Permission denied - {full_path}")
                                break
                            except OSError as e:
                                print(f"Error deleting {full_path}: {e}")
                                break
                        else:
                            print("Skipping deletion.")
                            break
                    elif action == 'r':
                        if filename.endswith("_en.srt"):
                            new_filename = filename.replace("_en.srt", ".srt")
                            new_full_path = os.path.join(root, new_filename)

                            try:
                                os.rename(full_path, new_full_path)
                                print(f"Renamed: {full_path} -> {new_full_path}")
                            except FileNotFoundError:
                                print(f"Error: File not found - {full_path}")
                            except FileExistsError:
                                print(f"Error: Target already exists - {new_full_path}")
                            except PermissionError:
                                print(f"Error: Permission denied - {full_path}")
                            except OSError as e:
                                print(f"Error renaming {full_path}: {e}")
                        break
                    elif action == 's':
                        print("Skipping file.")
                        break
                    else:
                        print("Invalid option. Please enter 'd', 'r', or 's'.")
                        return
            elif action == 'c' and filename.endswith(".mp4"):
                try:
                    subprocess_params = {
                        "stdout": subprocess.DEVNULL,
                        "stderr": subprocess.DEVNULL
                    }
                    video = VideoFileClip(full_path)
                    duration = video.duration
                    print(f"{filename}: {duration} seconds")
                    # log.info(f"{filename}: {duration} seconds")
                    video.close()
                    videosLength += duration
                except Exception as e:
                    print(f"Error processing {full_path}: {e}")
                break
    print(
        f"Overall Duration: {int(videosLength // 3600)} Hours {int((videosLength % 3600) // 60)} Minutes {int(videosLength % 60)} Seconds")


if __name__ == "__main__":
    log = configureLogger('video_processor')
    # input("Enter the path to the directory you want to process: ")
    target_path = "/home/henius/Downloads/Ultimate AWS Certified Solutions Architect Associate SAA-C03/"
    # input("Enter the prefix to filter by (leave blank for none): ") or None
    prefix_filter = None
    # input("Enter the suffix to filter by (leave blank for none): ") or None
    # suffix_filter = "Hands On.mp4"
    suffix_filter = "_en.srt"

    process_files(target_path, prefix_filter, suffix_filter, 'r')
    # print(f"{int(9223372036854775807 // 3600)}")

    print("\nFile processing complete.")
