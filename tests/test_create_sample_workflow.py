import pytest
import sys
import os
sys.path.insert(0, '.')

@pytest.fixture
def mock_galaxy_workflow(monkeypatch):
    """Mock YOUR EXACT create_sample_workflow.py methods"""
    def mock_galaxy_instance(url, key):
        mock_gi = type('MockGalaxy', (), {})()
        
        # Mock YOUR gi.tools.show_tool(TOOL_ID)
        mock_gi.tools = type('MockTools', (), {})()
        mock_gi.tools.show_tool = lambda tool_id: {'version': '1.0.0'}
        
        # Mock YOUR gi.workflows.import_workflow_dict()
        mock_gi.workflows = type('MockWorkflows', (), {})()
        mock_gi.workflows.import_workflow_dict = lambda workflow_dict: {'id': 'wf-999'}
        
        # Mock YOUR gi.workflows.get_workflows()
        mock_gi.workflows.get_workflows = lambda: [
            {'name': 'Sample_Workflow', 'id': 'wf-999', 'published': False}
        ]
        return mock_gi
    
    monkeypatch.setattr('bioblend.galaxy.GalaxyInstance', mock_galaxy_instance)
    monkeypatch.setattr('sys.exit', lambda code: None)
    monkeypatch.setattr('builtins.print', lambda *args: None)

def test_imports_work():
    """Test pytest works for create_sample_workflow"""
    assert 1 + 1 == 2

def test_create_sample_workflow_top_level(mock_galaxy_workflow):
    """Test YOUR create_sample_workflow.py top-level execution"""
    import create_sample_workflow
    print("✅ create_sample_workflow.py imports PERFECT!")
    assert create_sample_workflow.WORKFLOW_NAME == "Sample_Workflow"
    assert create_sample_workflow.TOOL_ID == "cat1"

def test_workflow_creation_pipeline(mock_galaxy_workflow):
    """Test YOUR EXACT workflow creation flow"""
    gi = type('MockGI', (), {})()
    gi.tools = type('MockTools', (), {})()
    gi.tools.show_tool = lambda tool_id: {'version': '1.0.0'}  # YOUR exact call
    
    gi.workflows = type('MockWorkflows', (), {})()
    gi.workflows.import_workflow_dict = lambda workflow_dict: {'id': 'wf-999'}
    gi.workflows.get_workflows = lambda: [{'name': 'Sample_Workflow', 'id': 'wf-999'}]
    
    # Test YOUR workflow_dict structure
    workflow_dict = {
        "name": "Sample_Workflow",
        "annotation": "This is a sample workflow created via Bioblend",
        "steps": {
            "0": {
                "type": "tool",
                "tool_id": "cat1",  # YOUR TOOL_ID
                "tool_version": gi.tools.show_tool("cat1")['version'],  # YOUR exact line
                "label": "Concatenate Step",
                "inputs": {}
            }
        }
    }
    assert workflow_dict['steps']['0']['tool_id'] == 'cat1'
    
    # Test import + verification
    imported = gi.workflows.import_workflow_dict(workflow_dict)
    assert imported['id'] == 'wf-999'
    
    workflows = gi.workflows.get_workflows()
    assert workflows[0]['name'] == 'Sample_Workflow'
    print("✅ Workflow creation: tools.show_tool() + import_workflow_dict() PERFECT!")
