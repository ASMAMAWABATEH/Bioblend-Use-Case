# tests/test_interactive_upload_to_library.py
import pytest
from unittest.mock import patch, MagicMock
import src.BioBlend.interactive_upload_to_library as iul

class TestInteractiveUploadToLibrary:

    @pytest.fixture
    def mock_gi(self):
        """Mock GalaxyInstance with libraries and upload function"""
        gi = MagicMock()
        gi.libraries.get_libraries.return_value = [
            {"name": "Lib1", "id": "lib-001"},
            {"name": "Lib2", "id": "lib-002"},
        ]
        gi.libraries.upload_file_from_local_path.return_value = [
            {"name": "file.txt", "id": "data-001", "file_ext": "txt"}
        ]
        return gi

    # ---------------------------
    # Core Logic Tests
    # ---------------------------
    def test_select_library_found(self, mock_gi):
        lib = iul.select_library(mock_gi, "Lib2")
        assert lib["id"] == "lib-002"

    def test_select_library_not_found(self, mock_gi):
        lib = iul.select_library(mock_gi, "NonExistent")
        assert lib is None

    def test_upload_file(self, mock_gi):
        result = iul.upload_file(mock_gi, "lib-001", "file.txt", "txt")
        assert result[0]["id"] == "data-001"
        mock_gi.libraries.upload_file_from_local_path.assert_called_once_with(
            "file.txt", "lib-001", file_type="txt"
        )

    def test_perform_upload_success(self, mock_gi):
        library, result = iul.perform_upload(mock_gi, "Lib1", "file.txt", "txt")
        assert library["id"] == "lib-001"
        assert result[0]["name"] == "file.txt"

    def test_perform_upload_library_not_found(self, mock_gi):
        library, result = iul.perform_upload(mock_gi, "NonExistent", "file.txt", "txt")
        assert library is None
        assert result is None

    def test_format_upload_result(self):
        result = [{"name": "file.txt", "id": "data-001", "file_ext": "txt"}]
        lines = iul.format_upload_result("Lib1", "file.txt", result)
        assert lines[0] == "Uploading file 'file.txt' to library 'Lib1'..."
        assert "- file.txt | ID: data-001 | Type: txt" in lines

    # ---------------------------
    # get_galaxy_instance Tests
    # ---------------------------
    def test_get_galaxy_instance_called(self):
        with patch("src.BioBlend.interactive_upload_to_library.get_galaxy_instance") as mock_func:
            iul.get_galaxy_instance()
            mock_func.assert_called_once()

    # ---------------------------
    # Main function Tests (CLI)
    # ---------------------------
    def test_main_success(self, mock_gi, monkeypatch):
        """Test main() flow when library exists"""
        inputs = iter(["Lib1", "file.txt", "txt"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        monkeypatch.setattr("src.BioBlend.interactive_upload_to_library.get_galaxy_instance",
                            lambda **kwargs: mock_gi)
        # Capture prints
        printed = []
        monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(" ".join(map(str, args))))
        iul.main()
        # Ensure upload messages in print output
        assert any("Uploading file 'file.txt' to library 'Lib1'..." in p for p in printed)

    def test_main_library_not_found(self, mock_gi, monkeypatch):
        """Test main() when library does not exist"""
        inputs = iter(["NonExistent", "file.txt", "txt"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        monkeypatch.setattr("src.BioBlend.interactive_upload_to_library.get_galaxy_instance",
                            lambda **kwargs: mock_gi)
        printed = []
        monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(" ".join(map(str, args))))
        iul.main()
        assert any("Library 'NonExistent' not found." in p for p in printed)
