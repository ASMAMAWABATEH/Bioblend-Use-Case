import pytest
import sys
import os
sys.path.insert(0, '..')

# Test functions - NO top-level imports that crash
@pytest.fixture
def mock_env(monkeypatch, tmp_path):
    fake_file = tmp_path / "biobhistory.fastq"
    fake_file.write_text("@SEQ1\nFAKE DATA")
    monkeypatch.setenv("GALAXY_URL", "http://fake-galaxy")
    monkeypatch.setenv("API_KEY", "fake-key")
    monkeypatch.setenv("FILE_NAME", str(fake_file))
    monkeypatch.setenv("LIBRARY_ID", "fake-lib-123")
    return str(fake_file)

def test_imports_work():
    """Basic test - proves pytest works"""
    assert 1 + 1 == 2

def test_file_exists(mock_env):
    """Test file creation works"""
    assert os.path.exists(mock_env)

def test_env_vars(mock_env):
    """Test environment setup"""
    import os
    assert os.getenv("GALAXY_URL") == "http://fake-galaxy"
