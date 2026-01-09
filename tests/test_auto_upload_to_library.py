# tests/test_auto_upload_to_library.py
import pytest
from unittest.mock import Mock, patch
from src.BioBlend import auto_upload_to_library

class TestAutoUploadToLibrary:

    @pytest.fixture
    def mock_gi(self):
        gi = Mock()
        # Existing library
        gi.libraries.get_libraries.return_value = [{'id': 'lib-001', 'name': 'Test Library'}]
        # Library creation
        gi.libraries.create_library.return_value = {'id': 'lib-002'}
        # File upload
        gi.libraries.upload_file_from_local_path.return_value = [{'id': 'ds-001'}]
        # Library contents
        gi.libraries.show_library.return_value = [
            {'name': 'dataset1', 'type': 'fastqsanger', 'id': 'ds-001'}
        ]
        return gi

    def test_connect_galaxy(self):
        with patch('src.BioBlend.auto_upload_to_library.GalaxyInstance') as mock:
            auto_upload_to_library.connect_galaxy("url", "key")
            mock.assert_called_once_with(url="url", key="key")

    def test_select_or_create_library_existing(self, mock_gi):
        lib_id = auto_upload_to_library.select_or_create_library(mock_gi, "MyLib", "Desc")
        assert lib_id == 'lib-001'
        mock_gi.libraries.get_libraries.assert_called_once()

    def test_select_or_create_library_new(self, mock_gi):
        mock_gi.libraries.get_libraries.return_value = []
        lib_id = auto_upload_to_library.select_or_create_library(mock_gi, "MyLib", "Desc")
        assert lib_id == 'lib-002'
        mock_gi.libraries.create_library.assert_called_once_with(name="MyLib", description="Desc")

    def test_upload_file(self, mock_gi):
        dataset_id = auto_upload_to_library.upload_file(mock_gi, 'lib-001', 'file.fastq', 'fastqsanger')
        assert dataset_id == 'ds-001'
        mock_gi.libraries.upload_file_from_local_path.assert_called_once_with('lib-001', 'file.fastq', 'fastqsanger')

    def test_show_library_contents(self, mock_gi):
        contents = auto_upload_to_library.show_library_contents(mock_gi, 'lib-001')
        assert contents == [('dataset1', 'fastqsanger', 'ds-001')]
        mock_gi.libraries.show_library.assert_called_once_with('lib-001', contents=True)
