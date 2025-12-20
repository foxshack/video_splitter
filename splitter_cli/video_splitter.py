import cv2
import argparse
import os


def video_splitter(filename, directory):
    """Split video out into separate frames and output as jpegs"""
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()

    count = 0
    while success:

        new_file = os.path.join(directory, "frame%d.jpg" % count)

        cv2.imwrite(new_file, image)
        success, image = vidcap.read()
        count += 1


def create_file_path(path):
    head, tail = os.path.split(path)
    filename, extension = os.path.splitext(tail)

    filename = "{}_{}".format(filename, "frames")

    return os.path.join(os.path.dirname(path), filename)


def splitter(path):

    if os.path.exists(path):
        dir = create_file_path(path)

    if not os.path.exists(dir):
        os.mkdir(dir)
        video_splitter(path, dir)


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="Split movie into frames")

    parser.add_argument(dest="filenames", metavar="filename", nargs="*")

    args = parser.parse_args()

    if not args.filenames:
        parser.error("No file reference provided. Please provide a video file path.")

    file_path = args.filenames[0]

    if not file_path:
        parser.error(
            "No file reference provided. Please provide a valid video file path."
        )

    splitter(file_path)


if __name__ == "__main__":
    main()
