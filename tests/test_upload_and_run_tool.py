import pytest
from unittest.mock import Mock, patch
from src.BioBlend import upload_and_run_tool

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def mock_gi():
    gi = Mock()
    gi.histories.create_history.return_value = {"id": "history-001"}
    gi.tools.upload_file.return_value = [{"id": "dataset-001"}]
    gi.tools.run_tool.return_value = {"outputs": ["dataset-002"]}
    return gi

# -----------------------------
# Tests
# -----------------------------
class TestUploadAndRunTool:

    def test_get_galaxy_instance(self):
        """GalaxyInstance is called with correct URL and key."""
        with patch("src.BioBlend.upload_and_run_tool.GalaxyInstance") as mock:
            upload_and_run_tool.get_galaxy_instance()
            mock.assert_called_once_with(
                url="http://localhost:8080",
                key="b8ba458fe9b1c919040db8288c56ed06"
            )

    def test_create_history(self, mock_gi):
        """Test history creation."""
        history = upload_and_run_tool.create_history(mock_gi, "My_History")
        assert history["id"] == "history-001"
        mock_gi.histories.create_history.assert_called_once_with("My_History")

    def test_upload_file(self, mock_gi, tmp_path):
        """Test file upload to history."""
        dummy_file = tmp_path / "file.fastq"
        dummy_file.write_text("ACGT")  # create dummy file

        dataset_id = upload_and_run_tool.upload_file(
            mock_gi, "history-001", str(dummy_file)
        )
        assert dataset_id == "dataset-001"
        mock_gi.tools.upload_file.assert_called_once()

    def test_upload_file_not_found(self, mock_gi):
        """Ensure FileNotFoundError is raised if file missing."""
        with pytest.raises(FileNotFoundError):
            upload_and_run_tool.upload_file(mock_gi, "history-001", "missing.fastq")

    def test_run_tool(self, mock_gi):
        """Test running a Galaxy tool."""
        tool_inputs = {"input_file": {"src": "hda", "id": "dataset-001"}}
        result = upload_and_run_tool.run_tool(mock_gi, "fastqc", "history-001", tool_inputs)
        
        # Verify call
        mock_gi.tools.run_tool.assert_called_once_with(
            "history-001", "fastqc", tool_inputs=tool_inputs
        )
        assert result == {"outputs": ["dataset-002"]}
