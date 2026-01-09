# tests/test_interactive_upload_to_library.py
import pytest
from unittest.mock import patch, MagicMock
import src.BioBlend.interactive_upload_to_library as iul

def test_get_galaxy_instance_called():
    """Test GalaxyInstance is called via get_galaxy_instance"""
    with patch("src.BioBlend.interactive_upload_to_library.get_galaxy_instance") as mock_gi:
        iul.get_galaxy_instance()
        mock_gi.assert_called_once()

def test_select_library_found():
    mock_gi = MagicMock()
    mock_gi.libraries.get_libraries.return_value = [
        {"name": "Lib1", "id": "lib-001"},
        {"name": "Lib2", "id": "lib-002"},
    ]
    lib = iul.select_library(mock_gi, "Lib2")
    assert lib["id"] == "lib-002"

def test_select_library_not_found():
    mock_gi = MagicMock()
    mock_gi.libraries.get_libraries.return_value = []
    lib = iul.select_library(mock_gi, "NonExistent")
    assert lib is None

def test_upload_file():
    mock_gi = MagicMock()
    mock_gi.libraries.upload_file_from_local_path.return_value = [{"name": "file.txt", "id": "data-001", "file_ext": "txt"}]

    result = iul.upload_file(mock_gi, "lib-001", "file.txt", "txt")
    assert result[0]["id"] == "data-001"
    mock_gi.libraries.upload_file_from_local_path.assert_called_once_with("file.txt", "lib-001", file_type="txt")
