import pytest
import sys
import os
sys.path.insert(0, '../src/bioblend')

@pytest.fixture
def mock_galaxy(monkeypatch):
    """Mock ALL GalaxyInstance network calls"""
    def mock_galaxy_instance(url, key):
        mock_gi = type('MockGalaxy', (), {})()
        mock_gi.config = type('MockConfig', (), {})()
        mock_gi.config.get_version = lambda: "22.05"  # Fake version
        return mock_gi
    monkeypatch.setattr('bioblend.galaxy.GalaxyInstance', mock_galaxy_instance)

def test_imports_work():
    """Test pytest works"""
    assert 1 + 1 == 2

def test_connect_to_galaxy_imports_without_crashing(mock_galaxy):
    """Test import works WITHOUT real HTTP calls"""
    import connect_to_galaxy
    print("✅ Import PASSED - no network calls!")
    assert hasattr(connect_to_galaxy, 'gi')
    assert connect_to_galaxy.GI_URL == "http://localhost:8080"

def test_galaxy_connection_exists(mock_galaxy):
    """Test GalaxyInstance object exists"""
    import connect_to_galaxy
    assert hasattr(connect_to_galaxy, 'gi')
    print("✅ Galaxy connection object found!")
