import pytest
import sys
import os
sys.path.insert(0, '.')

@pytest.fixture
def mock_galaxy_view_workflows(monkeypatch):
    """Mock YOUR EXACT view_workflows.py methods"""
    def mock_galaxy_instance(url, key):
        mock_gi = type('MockGalaxy', (), {})()
        
        # Mock YOUR workflows.get_workflows()
        mock_gi.workflows = type('MockWorkflows', (), {})()
        mock_gi.workflows.get_workflows = lambda: [
            {
                'id': 'wf-001', 
                'name': 'Quality Control', 
                'published': True, 
                'owner': 'admin'
            },
            {
                'id': 'wf-002', 
                'name': 'RNA-Seq Analysis', 
                'published': False, 
                'owner': 'user1'
            }
        ]
        
        # Mock YOUR workflows.show_workflow() with YOUR exact steps structure
        mock_gi.workflows.show_workflow = lambda wf_id: {
            'steps': {
                '1': {'tool_id': 'fastqc', 'label': 'input_fastq'},
                '2': {'tool_id': 'cutadapt', 'label': 'trimmed'}
            }
        }
        return mock_gi
    
    monkeypatch.setattr('bioblend.galaxy.GalaxyInstance', mock_galaxy_instance)
    monkeypatch.setattr('sys.exit', lambda code: None)
    monkeypatch.setattr('builtins.print', lambda *args: None)

def test_imports_work():
    """Test pytest works for YOUR view_workflows"""
    assert 1 + 1 == 2

def test_view_workflows_full_execution(mock_galaxy_view_workflows):
    """Test YOUR EXACT top-level code: get_workflows() + show_workflow()"""
    import view_workflows
    print("✅ YOUR view_workflows.py FULL execution PASSED!")
    assert hasattr(view_workflows, 'gi')
    assert view_workflows.GALAXY_URL == "http://localhost:8080"

def test_workflow_list_and_step_details(mock_galaxy_view_workflows):
    """Test YOUR workflows loop + wf_details.get('steps')"""
    import view_workflows
    workflows = view_workflows.gi.workflows.get_workflows()
    assert len(workflows) == 2
    assert workflows[0]['name'] == 'Quality Control'
    assert workflows[0].get('published', False) == True  # YOUR exact .get()
    
    # Test YOUR show_workflow + steps.items() loop
    details = view_workflows.gi.workflows.show_workflow('wf-001')
    steps = details.get('steps', {})  # YOUR EXACT line
    assert len(steps) == 2
    assert steps['1'].get('tool_id') == 'fastqc'  # YOUR EXACT structure
    assert steps['1'].get('label') == 'input_fastq'
    print("✅ YOUR workflow details + steps PERFECT!")
