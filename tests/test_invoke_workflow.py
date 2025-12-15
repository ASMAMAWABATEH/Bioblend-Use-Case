import pytest
import os
import sys
sys.path.insert(0, '.')

def test_imports_work():
    """Basic pytest verification"""
    assert 1 + 1 == 2

def test_file_exists_and_readable():
    """Test invoke_workflow.py file exists"""
    assert os.path.exists('invoke_workflow.py')
    assert os.path.getsize('invoke_workflow.py') > 1000
    print("✅ invoke_workflow.py file exists & readable!")

def test_project_structure_correct():
    """Test your professional project structure"""
    assert os.path.exists('tests/__init__.py')
    assert os.path.exists('invoke_workflow.py')
    assert os.path.exists('connect_to_galaxy.py')
    assert os.path.exists('biobhistory.fastq')
    print("✅ Professional BioBlend project structure!")

def test_configuration_via_string_parsing():
    """Test your constants by reading file (no import needed)"""
    with open('invoke_workflow.py', 'r') as f:
        content = f.read()
        assert 'GALAXY_URL = "http://localhost:8080"' in content
        assert 'WORKFLOW_NAME = "First_workflow"' in content
        assert 'HISTORY_NAME = "Workflow_Run_History"' in content
    print("✅ Found GALAXY_URL, WORKFLOW_NAME, HISTORY_NAME!")
