# Easy File Manager

A simple Python utility to manage files recursively. It can be used as a command-line tool or interactively.

## Features
- **Delete**: Batch delete files matching prefix/suffix filters (with confirmation).
- **Rename**: Batch rename files using custom search and replace patterns.
- **Calculate Duration**: Calculate total duration of video files in a directory.
- **Interactive Mode**: If run without arguments, the tool will prompt you for all necessary information.

## Installation

```bash
pip install .
```

## Usage

### Interactive Mode
Simply run the command and follow the prompts:
```bash
easy-file-manager
```

### Command Line Mode
```bash
easy-file-manager "/path/to/dir" --action r --suffix "_en.srt" --rename-search "_en.srt" --rename-replace ".srt"
```

### Arguments
- `path`: The root directory to scan.
- `--prefix`: Filter files starting with this string.
- `--suffix`: Filter files ending with this string.
- `--action`: 
    - `d`: Delete matching files (asks for confirmation for each file).
    - `r`: Rename matching files.
    - `c`: Calculate total video duration.
    - `s`: Skip (dry run/list).
- `--rename-search`: Pattern to search for in filenames (default: `_en.srt`).
- `--rename-replace`: Pattern to replace with (default: `.srt`).
- `--video-ext`: File extension for duration calculation (default: `.mp4`).
