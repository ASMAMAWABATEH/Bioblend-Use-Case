# tests/test_create_sample_workflow.py
import pytest
from unittest.mock import patch, MagicMock
from src.BioBlend import create_sample_workflow as csw

# ----------------------------
# Fixture: mock GalaxyInstance
# ----------------------------
@pytest.fixture
def mock_gi():
    gi = MagicMock()
    gi.tools.show_tool.return_value = {"version": "1.0.0"}
    gi.workflows.import_workflow_dict.return_value = {"id": "workflow-001"}
    gi.workflows.get_workflows.return_value = [
        {"name": "WF1", "id": "wf-001", "published": False},
        {"name": "WF2", "id": "wf-002", "published": True},
    ]
    return gi

# ----------------------------
# Test get_galaxy_instance
# ----------------------------
def test_get_galaxy_instance():
    with patch("src.BioBlend.create_sample_workflow.GalaxyInstance") as mock_cls:
        csw.get_galaxy_instance()
        mock_cls.assert_called_once_with(url=csw.GALAXY_URL, key=csw.API_KEY)

# ----------------------------
# Test create_workflow
# ----------------------------
def test_create_workflow(mock_gi):
    workflow_id = csw.create_workflow(
        mock_gi,
        name="TestWorkflow",
        steps=[{"tool_id": "cat1", "label": "Step 1"}]
    )
    assert workflow_id == "workflow-001"
    args, _ = mock_gi.workflows.import_workflow_dict.call_args
    wf_dict = args[0]
    assert wf_dict["name"] == "TestWorkflow"
    step0 = wf_dict["steps"]["0"]
    assert step0["tool_id"] == "cat1"
    assert step0["label"] == "Step 1"

# ----------------------------
# Test show_workflows
# ----------------------------
def test_show_workflows(mock_gi):
    workflows = csw.show_workflows(mock_gi)
    assert len(workflows) == 2
    assert workflows[0]["name"] == "WF1"
    assert workflows[1]["published"] is True

# ----------------------------
# Test CLI main block
# ----------------------------
def test_main(monkeypatch, mock_gi):
    # Patch get_galaxy_instance to return mock_gi
    monkeypatch.setattr(csw, "get_galaxy_instance", lambda: mock_gi)
    
    # Patch print to capture output
    printed = []
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(" ".join(str(a) for a in args)))

    # Run main
    csw.main()

    # Assertions
    assert any("Workflow created with ID: workflow-001" in line for line in printed)
    assert any("Current workflows on server:" in line for line in printed)
    assert any("WF1 | ID: wf-001" in line for line in printed)
    assert any("WF2 | ID: wf-002" in line for line in printed)
    assert any("✅ Workflow creation and verification complete!" in line for line in printed)
