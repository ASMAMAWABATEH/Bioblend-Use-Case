import pytest
from unittest.mock import Mock, patch
from src.BioBlend import upload_to_library

class TestUploadToLibrary:
    @pytest.fixture
    def mock_gi(self):
        gi = Mock()
        gi.libraries.get_libraries.return_value = [
            {"id": "lib-001", "name": "MyLibrary"}
        ]
        gi.libraries.upload_file_from_local_path.return_value = [{"id": "ds-001"}]
        return gi

    def test_get_galaxy_instance(self):
        """GalaxyInstance is called with correct URL and key"""
        with patch("src.BioBlend.upload_to_library.GalaxyInstance") as mock:
            upload_to_library.get_galaxy_instance()
            mock.assert_called_once_with(
                url="http://localhost:8080",
                key="b8ba458fe9b1c919040db8288c56ed06"
            )

    def test_select_library_existing(self, mock_gi):
        """Selects the correct library if exists"""
        lib_id = upload_to_library.select_library(mock_gi, "MyLibrary")
        assert lib_id == "lib-001"

    def test_select_library_not_found(self, mock_gi):
        """Returns None if library does not exist"""
        lib_id = upload_to_library.select_library(mock_gi, "NonExistent")
        assert lib_id is None

    def test_upload_file_to_library(self, mock_gi):
        """Uploads file and returns dataset ID"""
        ds_id = upload_to_library.upload_file_to_library(
            mock_gi, "lib-001", "bioblend_history.fastq"
        )
        assert ds_id == "ds-001"
        mock_gi.libraries.upload_file_from_local_path.assert_called_once_with(
            "lib-001", "bioblend_history.fastq", "fastqsanger"
        )
