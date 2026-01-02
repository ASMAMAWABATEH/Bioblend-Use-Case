import pytest
from unittest.mock import Mock
from BioBlend import invoke_workflow as iw

@pytest.fixture
def mock_gi():
    gi = Mock()
    # Mock workflow listing
    gi.workflows.get_workflows.return_value = [{"id": "wf-001", "name": "TestWorkflow"}]
    # Mock workflow invocation
    gi.workflows.invoke_workflow.return_value = {"id": "inv-001"}
    # Mock workflow status polling
    gi.workflows.show_invocation.return_value = {"state": "ok"}
    return gi

def test_find_workflow(mock_gi):
    """Test finding a workflow by name."""
    wf_id = iw.find_workflow(mock_gi, "TestWorkflow")
    assert wf_id == "wf-001"

    # Test workflow not found
    wf_id_none = iw.find_workflow(mock_gi, "NonexistentWorkflow")
    assert wf_id_none is None

def test_invoke_workflow(mock_gi):
    """Test invoking a workflow and checking state."""
    inv_id, state = iw.invoke_workflow(
        mock_gi,
        workflow_id="wf-001",
        history_id="hist-001",
        dataset_id="ds-001",
        max_wait=1,   # Short timeout for test
        interval=0    # No sleep for test speed
    )

    # Assertions
    assert inv_id == "inv-001"
    assert state == "ok"
    mock_gi.workflows.invoke_workflow.assert_called_once_with(
        workflow_id="wf-001",
        history_id="hist-001",
        inputs={"0": {"id": "ds-001"}}
    )
    mock_gi.workflows.show_invocation.assert_called()
