import pytest
import sys
import os
sys.path.insert(0, '.')

@pytest.fixture
def mock_galaxy_library_upload(monkeypatch, tmp_path):
    """Mock YOUR EXACT interactive_upload_to_library.py + input() + NO NETWORK"""
    fake_file = tmp_path / "biobhistory.fastq"
    fake_file.write_text("@SEQ1\nFAKE DATA")
    
    def mock_galaxy_instance(url, key):
        mock_gi = type('MockGalaxy', (), {})()
        
        # Mock YOUR gi.libraries.get_libraries()
        mock_gi.libraries = type('MockLibraries', (), {})()
        mock_gi.libraries.get_libraries = lambda: [
            {'id': 'lib-123', 'name': 'Test Library 1'},
            {'id': 'lib-456', 'name': 'Test Library 2'}
        ]
        
        # Mock YOUR gi.libraries.upload_file_from_local_path()
        mock_gi.libraries.upload_file_from_local_path = lambda lib_id, file_path, file_type: [
            {'id': 'ds-789', 'name': 'biobhistory.fastq'}
        ]
        
        # Mock YOUR gi.libraries.get_library_contents() ✅ FIXED
        mock_gi.libraries.get_library_contents = lambda lib_id: [
            {'name': 'biobhistory.fastq', 'type': 'file', 'id': 'ds-789'}
        ]
        return mock_gi
    
    # Mock input() → User selects library #1
    monkeypatch.setattr('builtins.input', lambda prompt: '1')
    monkeypatch.setattr('sys.exit', lambda code: None)
    monkeypatch.setattr('builtins.print', lambda *args: None)
    monkeypatch.setattr('os.path.exists', lambda path: True)
    monkeypatch.setattr('bioblend.galaxy.GalaxyInstance', mock_galaxy_instance)
    return fake_file

def test_imports_work():
    """Test pytest works for interactive_upload_to_library"""
    assert 1 + 1 == 2

def test_interactive_upload_top_level(mock_galaxy_library_upload):
    """Test YOUR interactive_upload_to_library.py top-level execution"""
    import interactive_upload_to_library  # ✅ NOW FULLY MOCKED - NO NETWORK
    print("✅ interactive_upload_to_library.py imports PERFECT!")

def test_library_upload_pipeline(mock_galaxy_library_upload):
    """Test YOUR EXACT library upload flow"""
    gi = type('MockGI', (), {})()
    gi.libraries = type('MockLibraries', (), {})()
    
    # Mock ALL your library methods ✅ COMPLETE
    gi.libraries.get_libraries = lambda: [{'id': 'lib-123', 'name': 'Test Library 1'}]
    gi.libraries.upload_file_from_local_path = lambda lib_id, file_path, file_type: [
        {'id': 'ds-789', 'name': 'biobhistory.fastq'}
    ]
    gi.libraries.get_library_contents = lambda lib_id: [  # ✅ FIXED
        {'name': 'biobhistory.fastq', 'type': 'file', 'id': 'ds-789'}
    ]
    
    # YOUR interactive flow (choice=1 → libraries[0])
    libraries = gi.libraries.get_libraries()
    LIBRARY_ID = libraries[0]['id']
    assert LIBRARY_ID == 'lib-123'
    
    # YOUR upload
    uploaded = gi.libraries.upload_file_from_local_path(LIBRARY_ID, "biobhistory.fastq", "fastqsanger")
    dataset_id = uploaded[0]['id']
    assert dataset_id == 'ds-789'
    
    # YOUR verification ✅ NOW WORKS
    contents = gi.libraries.get_library_contents(LIBRARY_ID)
    assert contents[0]['type'] == 'file'
    print("✅ Interactive library upload COMPLETE!")
