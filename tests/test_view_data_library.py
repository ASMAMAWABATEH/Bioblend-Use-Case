import pytest
from unittest.mock import Mock, patch
import src.BioBlend.view_data_library as vdl

class TestViewDataLibrary:

    @pytest.fixture
    def mock_gi(self):
        gi = Mock()
        gi.libraries.get_libraries.return_value = [
            {"id": "lib-001", "name": "Test Library"}
        ]
        gi.libraries.show_library.return_value = {
            "description": "Test description",
            "datasets": [
                {"id": "ds-001", "name": "dataset1.fastq", "type": "fastqsanger"},
                {"id": "ds-002", "name": "dataset2.fastq", "type": "fastqsanger"},
            ],
        }
        return gi

    def test_get_galaxy_instance(self):
        with patch("src.BioBlend.view_data_library.GalaxyInstance") as mock_class:
            vdl.get_galaxy_instance()
            mock_class.assert_called_once_with(url=vdl.GALAXY_URL, key=vdl.API_KEY)

    def test_list_libraries(self, mock_gi):
        result = vdl.list_libraries(mock_gi)
        assert len(result) == 1
        lib = result[0]
        assert lib["id"] == "lib-001"
        assert lib["name"] == "Test Library"
        assert lib["description"] == "Test description"
        assert len(lib["datasets"]) == 2

    def test_list_libraries_empty(self):
        gi = Mock()
        gi.libraries.get_libraries.return_value = []
        result = vdl.list_libraries(gi)
        assert result == []

    def test_format_libraries_output(self):
        libraries = [
            {"name": "Lib1", "description": "Desc1", "datasets": [
                {"id": "ds-001", "name": "file1", "type": "txt"}
            ]}
        ]
        output = vdl.format_libraries_output(libraries)
        assert any("Lib1" in line for line in output)
        assert any("file1" in line for line in output)

    def test_format_libraries_output_no_datasets(self):
        libraries = [{"name": "Lib2", "description": "Desc2", "datasets": []}]
        output = vdl.format_libraries_output(libraries)
        assert any("(No datasets)" in line for line in output)
