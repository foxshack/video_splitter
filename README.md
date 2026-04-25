# Video Splitter CLI

A command-line tool to split videos into individual frames.

This is not optimized for large video and only intended to be used on short clips
of a few seconds.


## Installation

Install using pipx (recommended):

```bash
pipx install git+https://github.com/foxshack/video_splitter.git
```

## Usage

After installation, you can use the `video-splitter` command from anywhere:

```bash
video-splitter path/to/your/video.mp4
```

This will create a directory next to your video file with the suffix `_frames` containing all extracted frames as JPEG images.

## Example

```bash
video-splitter my_video.mp4
# Creates: my_video_frames/frame0.jpg, frame1.jpg, ...
```

## Requirements

- Python 3.9 or higher
- opencv-python
