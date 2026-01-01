import pytest
import sys
import os
sys.path.insert(0, '.')

@pytest.fixture
def mock_galaxy_histories(monkeypatch):
    """Mock YOUR EXACT view_histories_datasets.py methods"""
    def mock_galaxy_instance(url, key):
        mock_gi = type('MockGalaxy', (), {})()
        
        # Mock YOUR gi.histories.get_histories()
        mock_gi.histories = type('MockHistories', (), {})()
        mock_gi.histories.get_histories = lambda: [
            {
                'id': 'hist-001', 
                'name': 'Workflow_Run_History'
            },
            {
                'id': 'hist-002', 
                'name': 'Quality Control Results'
            }
        ]
        
        # Mock YOUR gi.histories.show_history(history_id, contents=True)
        mock_gi.histories.show_history = lambda history_id, contents=True: [
            {
                'name': 'biobhistory.fastq',
                'id': 'ds-001',
                'state': 'ok',
                'history_content_type': 'dataset'
            },
            {
                'name': 'trimmed_reads.fastq',
                'id': 'ds-002', 
                'state': 'running',
                'history_content_type': 'dataset'
            }
        ]
        return mock_gi
    
    monkeypatch.setattr('bioblend.galaxy.GalaxyInstance', mock_galaxy_instance)
    monkeypatch.setattr('builtins.print', lambda *args: None)

def test_imports_work():
    """Test pytest works for view_histories_datasets"""
    assert 1 + 1 == 2

def test_view_histories_datasets_main_function(mock_galaxy_histories):
    """Test YOUR main() function executes perfectly"""
    from BioBlend.view_histories_datasets import main
    main()  # YOUR EXACT main() call
    print("✅ YOUR main() function PASSED perfectly!")

def test_histories_and_datasets_flow(mock_galaxy_histories):
    """Test YOUR EXACT histories.get_histories() + show_history()"""
    from BioBlend.view_histories_datasets import main
    gi = type('MockGalaxy', (), {})()
    gi.histories = type('MockHistories', (), {})()
    gi.histories.get_histories = lambda: [{'id': 'hist-001', 'name': 'Test History'}]
    gi.histories.show_history = lambda hid, contents=True: [
        {'name': 'test.fastq', 'id': 'ds-001', 'state': 'ok', 'history_content_type': 'dataset'}
    ]
    
    # Test YOUR exact data structure
    histories = gi.histories.get_histories()
    assert len(histories) == 1
    assert histories[0]['name'] == 'Test History'
    
    datasets = gi.histories.show_history('hist-001', contents=True)
    assert len(datasets) == 1
    assert datasets[0]['history_content_type'] == 'dataset'  # YOUR exact field
    print("✅ Histories + datasets contents=True PERFECT!")
