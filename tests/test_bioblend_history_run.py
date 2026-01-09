import pytest
from unittest.mock import Mock, patch
import builtins

# Import the refactored module
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
    gi.tools.upload_file.return_value = {
        "outputs": [{"id": "dataset-001"}]
    }

    # Mock running tool
    gi.tools.run_tool.return_value = {
        "jobs": [{"id": "job-001"}]
    }

    # Mock job polling
    gi.jobs.show_job.return_value = {"state": "ok"}

    return gi


def test_get_galaxy_instance():
    """Test GalaxyInstance creation"""
    with patch("src.BioBlend.bioblend_history_run.GalaxyInstance") as mock:
     bhr.get_galaxy_instance()
     mock.assert_called_once_with(
        url=bhr.GALAXY_URL,
        key=bhr.API_KEY
    )



def test_create_history(mock_gi):
    """Test creating a history"""
    history_id = bhr.create_history(mock_gi, "TestHistory")
    assert history_id == "history-001"
    mock_gi.histories.create_history.assert_called_once_with("TestHistory")


def test_upload_file_to_history(mock_gi):
    """Test uploading a file returns dataset ID"""
    dataset_id = bhr.upload_file_to_history(mock_gi, "file.fastq", "history-001")
    assert dataset_id == "dataset-001"
    mock_gi.tools.upload_file.assert_called_once_with(
        "file.fastq",
        "history-001",
        file_type=bhr.FILE_TYPE
    )


def test_run_tool(mock_gi):
    """Test running a tool returns job ID"""
    job_id = bhr.run_tool(mock_gi, "history-001", "cat1", "dataset-001")
    assert job_id == "job-001"
    mock_gi.tools.run_tool.assert_called_once_with(
        history_id="history-001",
        tool_id="cat1",
        tool_inputs={"input1": {"src": "hda", "id": "dataset-001"}}
    )


def test_wait_for_job(mock_gi):
    """Test job polling returns 'ok'"""
    state = bhr.wait_for_job(mock_gi, "job-001")
    assert state == "ok"
    mock_gi.jobs.show_job.assert_called()


def test_show_history_contents(mock_gi):
    """Test history contents listing"""
    contents = bhr.show_history_contents(mock_gi, "history-001")
    assert len(contents) == 2
    assert contents[0]["name"] == "dataset1"
    assert contents[1]["state"] == "running"


def test_run_main(monkeypatch, mock_gi):
    """Test main() workflow with mocked GalaxyInstance"""
    # Patch GalaxyInstance creation to return mock_gi
    monkeypatch.setattr(bhr, "get_galaxy_instance", lambda: mock_gi)

    # Patch sys.exit to prevent exiting
    monkeypatch.setattr("sys.exit", lambda code=None: None)

    # Patch INPUT_FILE to a dummy filename
    monkeypatch.setattr(bhr, "INPUT_FILE", "dummy.fastq")

    # Run main
    bhr.main()

    # Ensure all key methods were called
    mock_gi.histories.create_history.assert_called_once()
    mock_gi.tools.upload_file.assert_called_once()
    mock_gi.tools.run_tool.assert_called_once()
    mock_gi.jobs.show_job.assert_called()
    mock_gi.histories.show_history.assert_called_once()
