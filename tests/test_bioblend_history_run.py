# tests/test_bioblend_history_run.py
import pytest
from unittest.mock import Mock, patch
import sys
from src.BioBlend import bioblend_history_run as bhr

@pytest.fixture
def mock_gi():
    """Return a mocked GalaxyInstance with jobs, histories, and tools"""
    gi = Mock()

    # Mock histories
    gi.histories.create_history.return_value = {"id": "history-001"}
    gi.histories.show_history.return_value = [
        {"name": "dataset1", "id": "dataset-001", "state": "ok"},
        {"name": "dataset2", "id": "dataset-002", "state": "running"}
    ]

    # Mock file upload
    gi.tools.upload_file.return_value = {"outputs": [{"id": "dataset-001"}]}

    # Mock running tool
    gi.tools.run_tool.return_value = {"jobs": [{"id": "job-001"}]}

    # Mock job polling
    gi.jobs.show_job.return_value = {"state": "ok"}

    return gi

# ----------------------------
# Test Galaxy instance creation
# ----------------------------
def test_get_galaxy_instance():
    with patch("src.BioBlend.bioblend_history_run.GalaxyInstance") as mock_galaxy:
        bhr.get_galaxy_instance()
        mock_galaxy.assert_called_once_with(url=bhr.GALAXY_URL, key=bhr.API_KEY)

# ----------------------------
# Test history creation
# ----------------------------
def test_create_history(mock_gi):
    history_id = bhr.create_history(mock_gi, "TestHistory")
    assert history_id == "history-001"
    mock_gi.histories.create_history.assert_called_once_with("TestHistory")

# ----------------------------
# Test file upload
# ----------------------------
def test_upload_file_to_history(mock_gi):
    dataset_id = bhr.upload_file_to_history(mock_gi, "file.fastq", "history-001")
    assert dataset_id == "dataset-001"
    mock_gi.tools.upload_file.assert_called_once_with(
        "file.fastq", "history-001", file_type=bhr.FILE_TYPE
    )

# ----------------------------
# Test running tool
# ----------------------------
def test_run_tool_success(mock_gi):
    job_id = bhr.run_tool(mock_gi, "history-001", "cat1", "dataset-001")
    assert job_id == "job-001"
    mock_gi.tools.run_tool.assert_called_once_with(
        history_id="history-001",
        tool_id="cat1",
        tool_inputs={"input1": {"src": "hda", "id": "dataset-001"}}
    )

def test_run_tool_no_dataset(mock_gi):
    with pytest.raises(ValueError):
        bhr.run_tool(mock_gi, "history-001", "cat1", None)

# ----------------------------
# Test job polling
# ----------------------------
def test_wait_for_job_ok(mock_gi):
    state = bhr.wait_for_job(mock_gi, "job-001")
    assert state == "ok"

def test_wait_for_job_error(mock_gi):
    mock_gi.jobs.show_job.return_value = {"state": "error"}
    state = bhr.wait_for_job(mock_gi, "job-001")
    assert state == "error"

def test_wait_for_job_timeout(mock_gi):
    # Simulate never finishing
    mock_gi.jobs.show_job.return_value = {"state": "running"}
    state = bhr.wait_for_job(mock_gi, "job-001", timeout=0, interval=0)
    assert state == "timeout"

# ----------------------------
# Test showing history contents
# ----------------------------
def test_show_history_contents(mock_gi):
    contents = bhr.show_history_contents(mock_gi, "history-001")
    assert len(contents) == 2
    assert contents[0]["name"] == "dataset1"
    assert contents[1]["state"] == "running"

# ----------------------------
# Test main() workflow
# ----------------------------
def test_main_success(monkeypatch, mock_gi):
    # Patch GalaxyInstance creation
    monkeypatch.setattr(bhr, "get_galaxy_instance", lambda: mock_gi)
    monkeypatch.setattr(bhr, "INPUT_FILE", "dummy.fastq")

    # Prevent sys.exit
    monkeypatch.setattr("sys.exit", lambda code=None: None)

    printed = []
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(" ".join(str(a) for a in args)))

    bhr.main()

    # All key methods called
    mock_gi.histories.create_history.assert_called_once()
    mock_gi.tools.upload_file.assert_called_once()
    mock_gi.tools.run_tool.assert_called_once()
    mock_gi.jobs.show_job.assert_called()
    mock_gi.histories.show_history.assert_called()

    # Check some printed output
    assert any("Connecting to Galaxy..." in p for p in printed)
    assert any("Job completed successfully." in p for p in printed)

# ----------------------------
# Edge case: job finishes with error
# ----------------------------
def test_main_job_error(monkeypatch, mock_gi):
    monkeypatch.setattr(bhr, "get_galaxy_instance", lambda: mock_gi)
    monkeypatch.setattr(bhr, "INPUT_FILE", "dummy.fastq")
    monkeypatch.setattr("sys.exit", lambda code=None: None)

    # Simulate job error
    mock_gi.jobs.show_job.return_value = {"state": "error"}

    bhr.main()
    # Should print job finished with state
