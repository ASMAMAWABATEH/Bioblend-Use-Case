import pytest
from unittest.mock import Mock, patch
import BioBlend.view_data_library as view_data_library


class TestViewDataLibrary:

    @pytest.fixture
    def mock_gi(self):
        """Mock GalaxyInstance with one library and datasets"""
        gi = Mock()

        gi.libraries.get_libraries.return_value = [
            {"id": "lib-001", "name": "Test Library"}
        ]

        gi.libraries.show_library.return_value = {
            "description": "Test description",
            "datasets": [
                {"id": "ds-001", "name": "dataset1.fastq"},
                {"id": "ds-002", "name": "dataset2.fastq"},
            ],
        }

        return gi

    def test_get_galaxy_instance(self):
        """GalaxyInstance should be created with correct URL and key"""
        with patch("BioBlend.view_data_library.GalaxyInstance") as mock_gi_class:
            gi = view_data_library.get_galaxy_instance()

            mock_gi_class.assert_called_once_with(
                url=view_data_library.GALAXY_URL,
                key=view_data_library.API_KEY,
            )

    def test_list_libraries(self, mock_gi):
        """Test listing libraries with datasets"""
        result = view_data_library.list_libraries(mock_gi)

        assert len(result) == 1

        lib = result[0]
        assert lib["id"] == "lib-001"
        assert lib["name"] == "Test Library"
        assert lib["description"] == "Test description"

        assert len(lib["datasets"]) == 2
        assert lib["datasets"][0]["name"] == "dataset1.fastq"
        assert lib["datasets"][1]["name"] == "dataset2.fastq"

    def test_list_libraries_empty(self):
        """Test empty library list"""
        gi = Mock()
        gi.libraries.get_libraries.return_value = []

        result = view_data_library.list_libraries(gi)

        assert result == []
