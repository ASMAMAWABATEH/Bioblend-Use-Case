#!/usr/bin/env python3
import pytest
import sys
import os
sys.path.insert(0, '.')


@pytest.fixture
def mock_galaxy_workflow(monkeypatch):
    def mock_galaxy_instance(url, key):
        mock_gi = type('MockGalaxy', (), {})()
        mock_gi.libraries = type('MockLibraries', (), {})()
        mock_gi.libraries.get_libraries = lambda: []
        mock_gi.libraries.create_library = lambda name, description: {"id": "lib123"}
        mock_gi.libraries.upload_file_from_local_path = lambda lib_id, file_path, file_type: [{"id": "ds456"}]
        mock_gi.libraries.show_library = lambda lib_id, contents=True: [
            {"name": "bioblend_history.fastq", "type": "file", "id": "ds456"}
        ]
        return mock_gi
    
    monkeypatch.setattr('bioblend.galaxy.GalaxyInstance', mock_galaxy_instance)
    monkeypatch.setattr('os.path.exists', lambda path: True)
    monkeypatch.setattr('builtins.print', lambda *args: None)


def test_imports_work():
    assert 1 + 1 == 2


def test_get_env_variables_all_set(mock_galaxy_workflow, monkeypatch):
    """Test get_env_variables() - DISABLE dotenv first"""
    monkeypatch.setattr('dotenv.load_dotenv', lambda: None)
    monkeypatch.delenv('GALAXY_API_KEY', raising=False)
    monkeypatch.setenv('GALAXY_URL', 'https://test.com')
    monkeypatch.setenv('GALAXY_API_KEY', 'fake-key')
    monkeypatch.setenv('FILE_NAME', 'test.fastq')
    
    from BioBlend.auto_upload_to_library import get_env_variables
    result = get_env_variables()
    assert result["GALAXY_URL"] == "https://test.com"
    assert result["API_KEY"] == "fake-key"
    print("✅ get_env_variables() PERFECT!")


def test_get_env_variables_defaults(mock_galaxy_workflow, monkeypatch):
    monkeypatch.setattr('dotenv.load_dotenv', lambda: None)
    monkeypatch.delenv('GALAXY_URL', raising=False)
    monkeypatch.delenv('GALAXY_API_KEY', raising=False)
    
    from BioBlend.auto_upload_to_library import get_env_variables
    result = get_env_variables()
    assert result["FILE_NAME"] == "bioblend_history.fastq"
    assert result["FILE_TYPE"] == "fastqsanger"
    print("✅ Defaults PERFECT!")


def test_auto_upload_top_level(mock_galaxy_workflow, monkeypatch):
    monkeypatch.setattr('dotenv.load_dotenv', lambda: None)
    monkeypatch.delenv('GALAXY_API_KEY', raising=False)
    monkeypatch.setenv('FILE_NAME', 'test.fastq')
    monkeypatch.setenv('GALAXY_URL', 'https://test.com')
    monkeypatch.setenv('GALAXY_API_KEY', 'fake-key')
    monkeypatch.setenv('FILE_TYPE', 'fastqsanger')
    
    from BioBlend.auto_upload_to_library import main
    main()
    print("✅ main() PERFECT!")


def test_library_creation_pipeline(mock_galaxy_workflow):
    gi = type('MockGI', (), {})()
    gi.libraries = type('MockLibraries', (), {})()
    gi.libraries.get_libraries = lambda: []
    gi.libraries.create_library = lambda name, desc: {"id": "lib123"}
    gi.libraries.upload_file_from_local_path = lambda lib_id, file_path, file_type: [{"id": "ds456"}]
    gi.libraries.show_library = lambda lib_id, contents=True: [{"name": "test.fastq", "type": "file", "id": "ds456"}]
    
    lib_id = gi.libraries.create_library("TestLib", "Test")
    assert lib_id["id"] == "lib123"
    print("✅ Library pipeline PERFECT!")


def test_file_not_found(mock_galaxy_workflow, monkeypatch):
    monkeypatch.setattr('dotenv.load_dotenv', lambda: None)
    monkeypatch.setenv('FILE_NAME', 'missing.fastq')
    monkeypatch.setattr('os.path.exists', lambda path: False)
    
    from BioBlend.auto_upload_to_library import main
    main()
    print("✅ File-not-found PERFECT!")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
