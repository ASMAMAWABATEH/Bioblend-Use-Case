import pytest
from unittest.mock import Mock, patch
import BioBlend.view_data_library as view_data_library

class TestViewDataLibrary:

    @pytest.fixture
    def mock_gi(self):
        """Mock GalaxyInstance with libraries and datasets"""
        gi = Mock()

        # Mock get_libraries to return a single library
        gi.libraries.get_libraries.return_value = [
            {"id": "lib-001", "name": "Test Library"}
        ]

        # Mock show_library to return description and datasets
        gi.libraries.show_library.return_value = {
            "description": "Test description",
            "datasets": [
                {"id": "ds-001", "name": "file1.fastq"},
                {"id": "ds-002", "name": "file2.fastq"}
            ]
        }

        return gi

    def test_list_libraries(self, mock_gi):
        """Test listing libraries with datasets"""
        result = view_data_library.list_libraries(mock_gi)
        
        assert len(result) == 1
        lib = result[0]
        assert lib["name"] == "Test Library"
        assert lib["description"] == "Test description"
        assert len(lib["datasets"]) == 2
        assert lib["datasets"][0]["name"] == "file1.fastq"
        assert lib["datasets"][1]["name"] == "file2.fastq"

    def test_list_libraries_empty(self):
        """Test empty library list is handled correctly"""
        mock_gi = Mock()
        mock_gi.libraries.get_libraries.return_value = []

        result = view_data_library.list_libraries(mock_gi)
        assert result == []

    def test_get_galaxy_instance(self):
        """GalaxyInstance should be created with correct URL and key"""
        # PATCH THE LOCAL MODULE PATH, NOT bioblend.galaxy
        with patch("BioBlend.view_data_library.GalaxyInstance") as mock_gi_class:
            gi = view_data_library.get_galaxy_instance()
            mock_gi_class.assert_called_once_with(
                url=view_data_library.GALAXY_URL,
                key=view_data_library.API_KEY
            )
