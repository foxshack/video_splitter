"""Tests for video_splitter module"""

import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from splitter_cli.video_splitter import create_file_path, main, splitter, video_splitter


class TestCreateFilePath:
    """Tests for create_file_path function"""

    def test_creates_frames_directory_name(self):
        """Test that create_file_path creates the correct frames directory name"""
        result = create_file_path("/path/to/video.mp4")
        assert "video_frames" in result

    def test_preserves_directory_structure(self):
        """Test that the output directory is in the same location as input"""
        input_path = "/path/to/my_video.mp4"
        result = create_file_path(input_path)
        assert result.startswith("/path/to/")

    def test_handles_different_extensions(self):
        """Test that create_file_path works with different video extensions"""
        for ext in [".mp4", ".avi", ".mov", ".mkv"]:
            result = create_file_path(f"/path/to/video{ext}")
            assert "_frames" in result
            assert ext not in result

    def test_handles_relative_paths(self):
        """Test that create_file_path works with relative paths"""
        result = create_file_path("video.mp4")
        assert "_frames" in result

    def test_handles_files_with_multiple_dots(self):
        """Test that create_file_path handles filenames with multiple dots"""
        result = create_file_path("/path/to/my.video.file.mp4")
        # Splits on last dot, so extension is removed correctly
        assert "my.video.file_frames" in result

    def test_output_path_structure(self):
        """Test the complete output path structure"""
        input_path = "/home/user/downloads/myvideo.mp4"
        result = create_file_path(input_path)
        expected = "/home/user/downloads/myvideo_frames"
        assert result == expected


class TestVideoSplitter:
    """Tests for video_splitter function"""

    def test_video_splitter_creates_frames(self, mock_cv2, mock_video_file, temp_dir):
        """Test that video_splitter calls cv2 functions correctly"""
        output_dir = os.path.join(temp_dir, "output_frames")
        os.makedirs(output_dir, exist_ok=True)

        video_splitter(mock_video_file, output_dir)

        # Verify VideoCapture was called with the video file
        mock_cv2.VideoCapture.assert_called_once_with(mock_video_file)

        # Verify imwrite was called 3 times (one for each frame)
        assert mock_cv2.imwrite.call_count == 3

    def test_video_splitter_frame_naming(self, mock_cv2, mock_video_file, temp_dir):
        """Test that frames are named correctly"""
        output_dir = os.path.join(temp_dir, "output_frames")
        os.makedirs(output_dir, exist_ok=True)

        video_splitter(mock_video_file, output_dir)

        # Check that imwrite was called with correct frame names
        calls = mock_cv2.imwrite.call_args_list
        for i, call in enumerate(calls):
            frame_path = call[0][0]
            assert f"frame{i}.jpg" in frame_path

    def test_video_splitter_uses_jpeg_format(self, mock_cv2, mock_video_file, temp_dir):
        """Test that frames are saved as JPEG"""
        output_dir = os.path.join(temp_dir, "output_frames")
        os.makedirs(output_dir, exist_ok=True)

        video_splitter(mock_video_file, output_dir)

        # Verify all frames end with .jpg
        calls = mock_cv2.imwrite.call_args_list
        for call in calls:
            frame_path = call[0][0]
            assert frame_path.endswith(".jpg")

    def test_video_splitter_frame_count_matches_video(self, mock_cv2, mock_video_file, temp_dir):
        """Test that the number of frames written matches video frames"""
        output_dir = os.path.join(temp_dir, "output_frames")
        os.makedirs(output_dir, exist_ok=True)

        video_splitter(mock_video_file, output_dir)

        # 3 frames (from mock_cv2 fixture setup)
        assert mock_cv2.imwrite.call_count == 3


class TestSplitter:
    """Tests for splitter orchestration function"""

    def test_splitter_creates_output_directory(self, mock_cv2, mock_video_file, temp_dir):
        """Test that splitter creates the output directory"""
        # Move the video file to temp_dir for this test
        video_path = os.path.join(temp_dir, "test.mp4")
        Path(video_path).touch()

        with patch("splitter_cli.video_splitter.video_splitter"):
            splitter(video_path)

            expected_dir = os.path.join(temp_dir, "test_frames")
            assert os.path.exists(expected_dir)

    def test_splitter_calls_video_splitter(self, mock_cv2, temp_dir):
        """Test that splitter calls video_splitter function"""
        video_path = os.path.join(temp_dir, "test.mp4")
        Path(video_path).touch()

        with patch("splitter_cli.video_splitter.video_splitter") as mock_vs:
            splitter(video_path)
            mock_vs.assert_called_once()

    def test_splitter_handles_nonexistent_file(self, temp_dir):
        """Test that splitter raises FileNotFoundError for nonexistent files"""
        nonexistent_path = os.path.join(temp_dir, "nonexistent.mp4")

        with pytest.raises(FileNotFoundError):
            splitter(nonexistent_path)

    def test_splitter_does_not_recreate_existing_directory(
        self, mock_cv2, mock_video_file, temp_dir
    ):
        """Test that splitter doesn't call video_splitter if directory exists"""
        video_path = os.path.join(temp_dir, "test.mp4")
        Path(video_path).touch()
        output_dir = os.path.join(temp_dir, "test_frames")
        os.makedirs(output_dir, exist_ok=True)

        with patch("splitter_cli.video_splitter.video_splitter") as mock_vs:
            splitter(video_path)
            # Function should NOT be called if directory already exists
            mock_vs.assert_not_called()


class TestMain:
    """Tests for main CLI entry point"""

    def test_main_requires_filename(self, capsys):
        """Test that main exits with error when no filename provided"""
        with patch.object(sys, "argv", ["video-splitter"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 2
            captured = capsys.readouterr()
            assert "No file reference provided" in captured.err

    def test_main_with_valid_file(self, mock_cv2, mock_video_file):
        """Test that main processes a valid video file"""
        with patch.object(sys, "argv", ["video-splitter", mock_video_file]):  # noqa: SIM117
            with patch("splitter_cli.video_splitter.splitter") as mock_splitter:
                main()
                mock_splitter.assert_called_once_with(mock_video_file)

    def test_main_handles_multiple_arguments(self, mock_cv2, mock_video_file):
        """Test that main uses only the first argument if multiple provided"""
        second_file = f"{mock_video_file}_2.mp4"
        with patch.object(sys, "argv", ["video-splitter", mock_video_file, second_file]):  # noqa: SIM117
            with patch("splitter_cli.video_splitter.splitter") as mock_splitter:
                main()
                # Should only process the first file
                mock_splitter.assert_called_once_with(mock_video_file)

    def test_main_with_empty_string_argument(self, capsys):
        """Test that main rejects empty string arguments"""
        with patch.object(sys, "argv", ["video-splitter", ""]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 2
            captured = capsys.readouterr()
            assert "No file reference provided" in captured.err


@pytest.mark.integration
class TestIntegration:
    """Integration tests for the complete workflow"""

    def test_complete_workflow(self, mock_cv2, temp_dir):
        """Test the complete workflow from CLI to frame extraction"""
        video_path = os.path.join(temp_dir, "sample.mp4")
        Path(video_path).touch()

        with patch.object(sys, "argv", ["video-splitter", video_path]):
            main()

        # Check that output directory was created
        expected_dir = os.path.join(temp_dir, "sample_frames")
        assert os.path.exists(expected_dir)

    def test_frames_output_format(self, mock_cv2, temp_dir):
        """Test that frames are created with correct naming convention"""
        video_path = os.path.join(temp_dir, "movie.mp4")
        Path(video_path).touch()

        with patch.object(sys, "argv", ["video-splitter", video_path]):
            main()

        # Verify cv2.imwrite was called with proper paths
        calls = mock_cv2.imwrite.call_args_list
        assert len(calls) > 0

        for i, call in enumerate(calls):
            frame_path = call[0][0]
            expected_name = f"frame{i}.jpg"
            assert expected_name in frame_path
