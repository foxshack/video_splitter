# Video Splitter CLI

A command-line tool to split videos into individual frames.

## Installation

Install using pipx (recommended):

```bash
pipx install .
```

Or install using pip:

```bash
pip install .
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

- Python 3.8 or higher
- opencv-python

## Development

To install in development mode:

```bash
pip install -e .
```
