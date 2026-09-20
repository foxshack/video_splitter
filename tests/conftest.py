"""Pytest configuration and fixtures"""

import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup after test
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_video_file(temp_dir):
    """Create a mock video file path"""
    video_path = os.path.join(temp_dir, "test_video.mp4")
    # Create an empty file to simulate a video
    Path(video_path).touch()
    return video_path


@pytest.fixture
def mock_cv2(monkeypatch):
    """Mock cv2 module for testing"""
    mock_capture = MagicMock()
    mock_image = MagicMock()

    # Simulate video with 3 frames
    mock_capture.read.side_effect = [
        (True, mock_image),
        (True, mock_image),
        (True, mock_image),
        (False, None),
    ]

    mock_cv2 = MagicMock()
    mock_cv2.VideoCapture.return_value = mock_capture
    mock_cv2.imwrite.return_value = True

    monkeypatch.setattr("splitter_cli.video_splitter.cv2", mock_cv2)
    return mock_cv2
