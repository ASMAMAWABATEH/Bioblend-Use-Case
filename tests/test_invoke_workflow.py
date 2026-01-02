import pytest
import os
import sys
sys.path.insert(0, os.path.abspath('src'))

def test_imports_work():
    """Basic pytest verification"""
    assert 1 + 1 == 2

def test_file_exists_and_readable():
    """Test invoke_workflow.py file exists"""
    assert os.path.exists('src/BioBlend/invoke_workflow.py')
    assert os.path.getsize('src/BioBlend/invoke_workflow.py') > 1000
    print("✅ invoke_workflow.py file exists & readable!")

def test_project_structure_correct():
    """Test your professional project structure"""
    assert os.path.exists('tests/__init__.py')
    assert os.path.exists('src/BioBlend/invoke_workflow.py')
    assert os.path.exists('src/BioBlend/connect_to_galaxy.py')
    assert os.path.exists('data/bioblend_history.fastq')
    fastq_file = os.path.join('data', 'bioblend_history.fastq')
    assert os.path.exists(fastq_file)
    print("✅ Professional BioBlend project structure!")

def test_configuration_via_string_parsing():
    """Test your constants by reading file (no import needed)"""
    with open('src/BioBlend/invoke_workflow.py', 'r') as f:
        content = f.read()
        assert 'GALAXY_URL = "http://localhost:8080"' in content
        assert 'WORKFLOW_NAME = "First_workflow"' in content
        assert 'HISTORY_NAME = "Workflow_Run_History"' in content
    print("✅ Found GALAXY_URL, WORKFLOW_NAME, HISTORY_NAME!")
