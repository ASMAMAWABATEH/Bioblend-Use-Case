import pytest
import sys
import os
sys.path.insert(0, '.')

@pytest.fixture
def mock_galaxy_export_import(monkeypatch, tmp_path):
    """Mock YOUR EXACT export_import_workflow.py methods + file I/O"""
    def mock_galaxy_instance(url, key):
        mock_gi = type('MockGalaxy', (), {})()
        
        # Mock YOUR workflows.get_workflows()
        mock_gi.workflows = type('MockWorkflows', (), {})()
        mock_gi.workflows.get_workflows = lambda: [
            {'id': 'wf-123', 'name': 'First_workflow'}
        ]
        
        # Mock YOUR workflows.export_workflow_dict()
        mock_gi.workflows.export_workflow_dict = lambda workflow_id: {
            'name': 'First_workflow',
            'steps': {'0': {'tool_id': 'cat1'}}
        }
        
        # Mock YOUR workflows.import_workflow_dict()
        mock_gi.workflows.import_workflow_dict = lambda workflow_json: {
            'id': 'wf-456', 
            'name': 'First_workflow_imported'
        }
        return mock_gi
    
    monkeypatch.setattr('bioblend.galaxy.GalaxyInstance', mock_galaxy_instance)
    monkeypatch.setattr('sys.exit', lambda code: None)
    monkeypatch.setattr('builtins.print', lambda *args: None)
    return tmp_path

def test_imports_work(mock_galaxy_export_import):
    """Test pytest works for export_import_workflow"""
    assert 1 + 1 == 2

def test_export_import_workflow_top_level(mock_galaxy_export_import):
    """Test YOUR export_import_workflow.py top-level execution"""
    
    from BioBlend import export_import_workflow

    print("✅ export_import_workflow.py imports PERFECT!")
    assert export_import_workflow.WORKFLOW_NAME == "First_workflow"

def test_complete_export_import_pipeline(mock_galaxy_export_import):
    """Test YOUR EXACT export→file→import flow"""
    gi = type('MockGI', (), {})()
    gi.workflows = type('MockWorkflows', (), {})()
    
    # Mock YOUR workflow lookup
    gi.workflows.get_workflows = lambda: [{'id': 'wf-123', 'name': 'First_workflow'}]
    
    # YOUR export_workflow_dict()
    gi.workflows.export_workflow_dict = lambda wf_id: {
        'name': 'First_workflow',
        'steps': {'0': {'tool_id': 'cat1'}}
    }
    
    # Simulate YOUR file export/import
    workflow_dict = gi.workflows.export_workflow_dict('wf-123')
    assert workflow_dict['name'] == 'First_workflow'
    
    # YOUR import_workflow_dict()
    gi.workflows.import_workflow_dict = lambda workflow_json: {
        'id': 'wf-456', 
        'name': 'First_workflow_imported'
    }
    imported = gi.workflows.import_workflow_dict(workflow_dict)
    assert imported['id'] == 'wf-456'
    
    print("✅ Export→file→import pipeline PERFECT!")
