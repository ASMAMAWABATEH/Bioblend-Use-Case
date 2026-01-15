# tests/test_upload_to_library.py
import pytest
from unittest.mock import Mock, patch
from src.BioBlend import upload_to_library
import os

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def mock_gi():
    """Mock GalaxyInstance for libraries and uploads"""
    gi = Mock()
    gi.libraries.get_libraries.return_value = [{"id": "lib-001", "name": "MyLibrary"}]
    gi.libraries.upload_file_from_local_path.return_value = [{"id": "ds-001"}]
    return gi

# -----------------------------
# Core function tests
# -----------------------------
def test_get_galaxy_instance():
    """GalaxyInstance is called with correct URL and key"""
    with patch("src.BioBlend.upload_to_library.GalaxyInstance") as mock:
        upload_to_library.get_galaxy_instance()
        mock.assert_called_once_with(
            url="http://localhost:8080",
            key="b8ba458fe9b1c919040db8288c56ed06"
        )

def test_select_library_existing(mock_gi):
    lib_id = upload_to_library.select_library(mock_gi, "MyLibrary")
    assert lib_id == "lib-001"

def test_select_library_nonexistent(mock_gi):
    lib_id = upload_to_library.select_library(mock_gi, "NonExistent")
    assert lib_id is None

def test_upload_file_to_library(mock_gi):
    dataset_id = upload_to_library.upload_file_to_library(mock_gi, "lib-001", "file.fastq")
    assert dataset_id == "ds-001"
    mock_gi.libraries.upload_file_from_local_path.assert_called_once_with("lib-001", "file.fastq", "fastqsanger")

def test_perform_upload_success(mock_gi, tmp_path):
    dummy_file = tmp_path / "bioblend_history.fastq"
    dummy_file.write_text("ACGT")

    with patch("os.path.exists", return_value=True):
        dataset_id, error = upload_to_library.perform_upload(
            mock_gi,
            file_name=str(dummy_file),
            library_name="MyLibrary"
        )
    assert dataset_id == "ds-001"
    assert error is None

def test_perform_upload_file_missing(mock_gi):
    with patch("os.path.exists", return_value=False):
        dataset_id, error = upload_to_library.perform_upload(
            mock_gi,
            file_name="missing.fastq",
            library_name="MyLibrary"
        )
    assert dataset_id is None
    assert "not found" in error

def test_perform_upload_library_missing(mock_gi, tmp_path):
    dummy_file = tmp_path / "bioblend_history.fastq"
    dummy_file.write_text("ACGT")

    mock_gi.libraries.get_libraries.return_value = []
    with patch("os.path.exists", return_value=True):
        dataset_id, error = upload_to_library.perform_upload(
            mock_gi,
            file_name=str(dummy_file),
            library_name="NonExistent"
        )
    assert dataset_id is None
    assert "not found" in error

# -----------------------------
# Main() function tests
# -----------------------------
# -----------------------------
# Main() function tests
# -----------------------------
def test_main_success(mock_gi, tmp_path):
    dummy_file = tmp_path / "bioblend_history.fastq"
    dummy_file.write_text("ACGT")

    with patch("src.BioBlend.upload_to_library.get_galaxy_instance", return_value=mock_gi), \
         patch("src.BioBlend.upload_to_library.perform_upload", return_value=("ds-001", None)), \
         patch("builtins.print") as mock_print:
        upload_to_library.main()
        mock_print.assert_any_call("Connected to Galaxy.")
        mock_print.assert_any_call("File uploaded successfully! Dataset ID: ds-001")


def test_main_file_missing(mock_gi):
    with patch("src.BioBlend.upload_to_library.get_galaxy_instance", return_value=mock_gi), \
         patch("src.BioBlend.upload_to_library.perform_upload", return_value=(None, "Error: File 'missing.fastq' not found!")), \
         patch("builtins.print") as mock_print:
        upload_to_library.main()
        mock_print.assert_any_call("Error: File 'missing.fastq' not found!")
