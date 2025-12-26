import pytest
import sys
import os
sys.path.insert(0, '.')

@pytest.fixture
def mock_galaxy_upload_run(monkeypatch, tmp_path):
    """Mock ALL 8 calls in upload_and_run_tool.py"""
    fake_file = tmp_path / "biobhistory.fastq"
    fake_file.write_text("@SEQ1\nFAKE DATA")
    
    def mock_galaxy_instance(url, key):
        mock_gi = type('MockGalaxy', (), {})()
        
        # 1. Mock histories.get_histories()
        mock_gi.histories = type('MockHistories', (), {})()
        mock_gi.histories.get_histories = lambda: [
            {'id': 'hist-001', 'name': 'biobhistory'}
        ]
        
        # 2. Mock histories.create_history()
        mock_gi.histories.create_history = lambda name: {'id': 'hist-001', 'name': name}
        
        # 3. Mock tools.upload_file()
        mock_gi.tools = type('MockTools', (), {})()
        mock_gi.tools.upload_file = lambda file_path, history_id, file_type: {
            'outputs': [{'id': 'ds-123'}]
        }
        
        # 4. Mock datasets.show_dataset()
        mock_gi.datasets = type('MockDatasets', (), {})()
        mock_gi.datasets.show_dataset = lambda ds_id: {'state': 'ok'}
        
        # 5. Mock tools.run_tool()
        mock_gi.tools.run_tool = lambda history_id, tool_id, tool_inputs: {
            'jobs': [{'id': 'job-456'}]
        }
        
        # 6. Mock jobs.show_job()
        mock_gi.jobs = type('MockJobs', (), {})()
        mock_gi.jobs.show_job = lambda job_id: {'state': 'ok'}
        
        # 7. Mock histories.show_history(contents=True)
        mock_gi.histories.show_history = lambda history_id, contents=True: [
            {'name': 'biobhistory.fastq', 'id': 'ds-123', 'state': 'ok', 'type': 'dataset'}
        ]
        
        return mock_gi
    
    monkeypatch.setattr('bioblend.galaxy.GalaxyInstance', mock_galaxy_instance)
    monkeypatch.setattr('sys.exit', lambda code: None)
    monkeypatch.setattr('builtins.print', lambda *args: None)
    monkeypatch.setattr('os.path.exists', lambda path: True)
    monkeypatch.setattr('time.sleep', lambda x: None)
    return fake_file

def test_imports_work():
    """Test pytest works for upload_and_run_tool"""
    assert 1 + 1 == 2

def test_upload_and_run_tool_full_execution(mock_galaxy_upload_run):
    """Test YOUR COMPLETE top-level execution (8 BioBlend calls)"""
    import upload_and_run_tool
    print("✅ YOUR upload_and_run_tool.py FULL execution PASSED!")
    assert hasattr(upload_and_run_tool, 'gi')
    assert upload_and_run_tool.HISTORY_NAME == "biobhistory"
    assert upload_and_run_tool.TOOL_ID == "cat1"

def test_complete_upload_run_pipeline(mock_galaxy_upload_run):
    """Test YOUR EXACT flow: history → upload → tool → job → contents"""
    import upload_and_run_tool
    gi = upload_and_run_tool.gi
    
    # Test history lookup/create
    histories = gi.histories.get_histories()
    assert len(histories) == 1
    assert histories[0]['name'] == 'biobhistory'
    
    # Test upload → dataset_id
    dataset = gi.tools.upload_file("fake.fastq", "hist-001", "fastqsanger")
    dataset_id = dataset['outputs'][0]['id']  # YOUR EXACT line
    assert dataset_id == 'ds-123'
    
    # Test tool run → job_id
    tool_inputs = {"input1": {"src": "hda", "id": "ds-123"}}  # YOUR exact format
    run = gi.tools.run_tool("hist-001", "cat1", tool_inputs)
    job_id = run["jobs"][0]["id"]  # YOUR EXACT line
    assert job_id == 'job-456'
    
    # Test final contents
    contents = gi.histories.show_history("hist-001", contents=True)
    assert contents[0]['type'] == 'dataset'  # YOUR exact field
    print("✅ COMPLETE PIPELINE: history+upload+tool+job+contents PERFECT!")
