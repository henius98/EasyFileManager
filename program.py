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
                        new_name = filename + "_"
                        # new_name = filename[:-1] # + ".srt"    #input("Enter the new name for the file (including extension): ")
                        new_path = os.path.join(root, new_name)
                        # action1 = input(f"Are you sure you want to rename '{filename}' to '{new_name}'? (y/N): ")
                        try:
                            os.rename(full_path, new_path)
                            print(f"Renamed '{full_path}' to '{new_path}'")
                            break
                        except FileNotFoundError:
                            print(
                                f"Error: Original file not found - {full_path}")
                            break
                        except FileExistsError:
                            print(
                                f"Error: A file with the name '{new_name}' already exists in this directory.")
                            break
                        except PermissionError:
                            print(
                                f"Error: Permission denied to rename - {full_path}")
                            break
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
    target_path = "C:\\Users\\ROG_Q\\Desktop\\AWS"
    # input("Enter the prefix to filter by (leave blank for none): ") or None
    prefix_filter = None
    # input("Enter the suffix to filter by (leave blank for none): ") or None
    suffix_filter = "Hands On.mp4"

    process_files(target_path, prefix_filter, suffix_filter, 'r')
    # print(f"{int(9223372036854775807 // 3600)}")

    print("\nFile processing complete.")
