# tests/test_create_sample_workflow.py
from unittest.mock import patch, MagicMock
import pytest
import src.BioBlend.create_sample_workflow as csw

def test_get_galaxy_instance():
    """GalaxyInstance is called with correct URL and key"""
    # Patch where GalaxyInstance is actually used in create_sample_workflow
    with patch("src.BioBlend.create_sample_workflow.GalaxyInstance") as mock_gi:
        csw.get_galaxy_instance()
        mock_gi.assert_called_once_with(
            url=csw.GALAXY_URL,
            key=csw.API_KEY
        )

def test_create_workflow():
    """Test creating a workflow with a single step"""
    mock_gi = MagicMock()
    mock_gi.tools.show_tool.return_value = {"version": "1.0.0"}
    mock_gi.workflows.import_workflow_dict.return_value = {"id": "workflow-001"}

    workflow_id = csw.create_workflow(
        mock_gi,
        name="Test_Workflow",
        steps=[{"tool_id": "cat1", "label": "Step 1"}]
    )

    # Check returned workflow ID
    assert workflow_id == "workflow-001"

    # Verify the workflow dict passed to import_workflow_dict
    args, kwargs = mock_gi.workflows.import_workflow_dict.call_args
    wf_dict = args[0]
    assert wf_dict["name"] == "Test_Workflow"
    assert "steps" in wf_dict
    step0 = wf_dict["steps"]["0"]
    assert step0["tool_id"] == "cat1"
    assert step0["label"] == "Step 1"
    assert step0["type"] == "tool"

def test_show_workflows():
    """Test listing workflows"""
    mock_gi = MagicMock()
    mock_gi.workflows.get_workflows.return_value = [
        {"name": "WF1", "id": "wf-001", "published": False},
        {"name": "WF2", "id": "wf-002", "published": True}
    ]

    workflows = csw.show_workflows(mock_gi)
    assert len(workflows) == 2
    assert workflows[0]["name"] == "WF1"
    assert workflows[1]["published"] is True
