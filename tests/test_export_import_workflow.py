# tests/test_export_import_workflow.py
import pytest
from unittest.mock import patch, MagicMock
import os
import json
import tempfile

import src.BioBlend.export_import_workflow as eiw

# ----------------------------
# TEST: get_galaxy_instance
# ----------------------------
def test_get_galaxy_instance():
    with patch("src.BioBlend.export_import_workflow.GalaxyInstance") as mock_gi:
        eiw.get_galaxy_instance()
        mock_gi.assert_called_once_with(url=eiw.GALAXY_URL, key=eiw.API_KEY)

# ----------------------------
# TEST: export_workflow
# ----------------------------
def test_export_workflow(tmp_path):
    mock_gi = MagicMock()
    workflow_dict = {"name": "TestWorkflow", "steps": {}}
    mock_gi.workflows.export_workflow_dict.return_value = workflow_dict

    exported_file = eiw.export_workflow(mock_gi, workflow_id="wf-001", output_dir=tmp_path)

    assert os.path.exists(exported_file)
    with open(exported_file, "r") as f:
        data = json.load(f)
    assert data == workflow_dict

# ----------------------------
# TEST: import_workflow
# ----------------------------
def test_import_workflow(tmp_path):
    workflow_dict = {"name": "TestWorkflow", "steps": {}}
    workflow_file = tmp_path / "workflow.ga"
    with open(workflow_file, "w") as f:
        json.dump(workflow_dict, f)

    mock_gi = MagicMock()
    mock_gi.workflows.import_workflow_dict.return_value = {"id": "wf-001"}

    workflow_id = eiw.import_workflow(mock_gi, str(workflow_file))
    assert workflow_id == "wf-001"
    mock_gi.workflows.import_workflow_dict.assert_called_once_with(workflow_dict)

def test_import_workflow_file_not_found():
    mock_gi = MagicMock()
    with pytest.raises(FileNotFoundError):
        eiw.import_workflow(mock_gi, "non_existent_file.ga")

# ----------------------------
# TEST: show_workflows
# ----------------------------
def test_show_workflows():
    mock_gi = MagicMock()
    mock_gi.workflows.get_workflows.return_value = [{"name": "WF1", "id": "wf-001"}]
    workflows = eiw.show_workflows(mock_gi)
    assert workflows == [{"name": "WF1", "id": "wf-001"}]

# ----------------------------
# TEST: perform_export_import
# ----------------------------
def test_perform_export_import(tmp_path):
    mock_gi = MagicMock()

    workflow_dict = {"name": "TestWorkflow", "steps": {}}
    mock_gi.workflows.export_workflow_dict.return_value = workflow_dict
    mock_gi.workflows.import_workflow_dict.return_value = {"id": "wf-001"}

    exported_file, imported_id = eiw.perform_export_import(mock_gi, "wf-001", output_dir=tmp_path)
    assert os.path.exists(exported_file)
    assert imported_id == "wf-001"

# ----------------------------
# EDGE CASE: main() with no workflows
# ----------------------------
def test_main_no_workflows(monkeypatch):
    mock_gi = MagicMock()
    mock_gi.workflows.get_workflows.return_value = []

    monkeypatch.setattr(eiw, "get_galaxy_instance", lambda: mock_gi)
    # Patch print to capture
    printed = []
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(" ".join(str(a) for a in args)))

    eiw.main()
    assert "No workflows available to export." in printed
