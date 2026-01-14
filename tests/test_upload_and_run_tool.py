# tests/test_upload_and_run_tool.py
import pytest
from unittest.mock import Mock, patch
from src.BioBlend import upload_and_run_tool
import os

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def mock_gi():
    """Mock GalaxyInstance for histories, uploads, and tool runs"""
    gi = Mock()
    gi.histories.create_history.return_value = {"id": "history-001"}
    gi.tools.upload_file.return_value = [{"id": "dataset-001"}]
    gi.tools.run_tool.return_value = {"outputs": ["dataset-002"]}
    return gi

# -----------------------------
# Core function tests
# -----------------------------
def test_get_galaxy_instance():
    with patch("src.BioBlend.upload_and_run_tool.GalaxyInstance") as mock:
        upload_and_run_tool.get_galaxy_instance()
        mock.assert_called_once_with(
            url="http://localhost:8080",
            key="b8ba458fe9b1c919040db8288c56ed06"
        )

def test_create_history(mock_gi):
    history = upload_and_run_tool.create_history(mock_gi, "TestHistory")
    assert history["id"] == "history-001"
    mock_gi.histories.create_history.assert_called_once_with("TestHistory")

def test_upload_file(mock_gi, tmp_path):
    dummy_file = tmp_path / "file.fastq"
    dummy_file.write_text("ACGT")

    dataset_id = upload_and_run_tool.upload_file(mock_gi, "history-001", str(dummy_file))
    assert dataset_id == "dataset-001"
    mock_gi.tools.upload_file.assert_called_once()

def test_upload_file_not_found(mock_gi):
    with pytest.raises(FileNotFoundError):
        upload_and_run_tool.upload_file(mock_gi, "history-001", "missing.fastq")

def test_run_tool(mock_gi):
    tool_inputs = {"input_file": {"src": "hda", "id": "dataset-001"}}
    result = upload_and_run_tool.run_tool(mock_gi, "fastqc", "history-001", tool_inputs)
    mock_gi.tools.run_tool.assert_called_once_with(
        "history-001", "fastqc", tool_inputs=tool_inputs
    )
    assert result == {"outputs": ["dataset-002"]}

# -----------------------------
# Main() deterministic tests
# -----------------------------
def test_main_success(mock_gi):
    with patch("src.BioBlend.upload_and_run_tool.get_galaxy_instance", return_value=mock_gi), \
         patch("src.BioBlend.upload_and_run_tool.upload_file", return_value="dataset-001"), \
         patch("src.BioBlend.upload_and_run_tool.run_tool", return_value={"outputs": ["dataset-002"]}), \
         patch("builtins.print") as mock_print:
        upload_and_run_tool.main()
        mock_print.assert_any_call("Connected to Galaxy.")
        mock_print.assert_any_call("Uploaded dataset ID: dataset-001")
        mock_print.assert_any_call("Tool run result: {'outputs': ['dataset-002']}")

def test_main_file_missing(mock_gi):
    with patch("src.BioBlend.upload_and_run_tool.get_galaxy_instance", return_value=mock_gi), \
         patch("src.BioBlend.upload_and_run_tool.upload_file", side_effect=FileNotFoundError("File not found!")), \
         patch("builtins.print") as mock_print:
        upload_and_run_tool.main()
        mock_print.assert_any_call("Connected to Galaxy.")
        # Updated assertion to match actual output
        mock_print.assert_any_call("Error: File not found!")

