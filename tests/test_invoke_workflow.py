# tests/test_invoke_workflow.py
import pytest
from unittest.mock import Mock
from src.BioBlend import invoke_workflow as iw

# ----------------------------
# Fixtures
# ----------------------------
@pytest.fixture
def mock_gi():
    gi = Mock()
    # Mock workflow listing
    gi.workflows.get_workflows.return_value = [{"id": "wf-001", "name": "TestWorkflow"}]
    # Mock workflow invocation
    gi.workflows.invoke_workflow.return_value = {"id": "inv-001"}
    # Default workflow status polling
    gi.workflows.show_invocation.return_value = {"state": "ok"}
    return gi

# ----------------------------
# Tests: find_workflow
# ----------------------------
def test_find_workflow(mock_gi):
    """Test finding a workflow by name."""
    wf_id = iw.find_workflow(mock_gi, "TestWorkflow")
    assert wf_id == "wf-001"

    # Workflow not found
    wf_id_none = iw.find_workflow(mock_gi, "NonexistentWorkflow")
    assert wf_id_none is None

# ----------------------------
# Tests: invoke_workflow happy path
# ----------------------------
def test_invoke_workflow_ok(mock_gi):
    """Test workflow invocation completing successfully."""
    inv_id, state = iw.invoke_workflow(
        mock_gi,
        workflow_id="wf-001",
        history_id="hist-001",
        dataset_id="ds-001",
        max_wait=1,
        interval=0
    )
    assert inv_id == "inv-001"
    assert state == "ok"
    mock_gi.workflows.invoke_workflow.assert_called_once_with(
        workflow_id="wf-001",
        history_id="hist-001",
        inputs={"0": {"id": "ds-001"}}
    )
    mock_gi.workflows.show_invocation.assert_called()

# ----------------------------
# Tests: invoke_workflow error state
# ----------------------------
def test_invoke_workflow_error(mock_gi):
    """Test workflow invocation ending in 'error'."""
    mock_gi.workflows.show_invocation.return_value = {"state": "error"}
    inv_id, state = iw.invoke_workflow(
        mock_gi,
        workflow_id="wf-001",
        history_id="hist-001",
        dataset_id="ds-001",
        max_wait=1,
        interval=0
    )
    assert inv_id == "inv-001"
    assert state == "error"

# ----------------------------
# Tests: invoke_workflow failed state
# ----------------------------
def test_invoke_workflow_failed(mock_gi):
    """Test workflow invocation ending in 'failed'."""
    mock_gi.workflows.show_invocation.return_value = {"state": "failed"}
    inv_id, state = iw.invoke_workflow(
        mock_gi,
        workflow_id="wf-001",
        history_id="hist-001",
        dataset_id="ds-001",
        max_wait=1,
        interval=0
    )
    assert inv_id == "inv-001"
    assert state == "failed"

# ----------------------------
# Tests: invoke_workflow timeout
# ----------------------------
def test_invoke_workflow_timeout(mock_gi):
    """Test workflow invocation timing out."""
    # Simulate workflow never finishing
    states = [{"state": "running"}] * 5
    mock_gi.workflows.show_invocation.side_effect = states
    inv_id, state = iw.invoke_workflow(
        mock_gi,
        workflow_id="wf-001",
        history_id="hist-001",
        dataset_id="ds-001",
        max_wait=0,  # immediately trigger timeout
        interval=0
    )
    assert inv_id == "inv-001"
    assert state == "timeout"
