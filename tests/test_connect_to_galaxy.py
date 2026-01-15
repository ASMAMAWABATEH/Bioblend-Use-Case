import pytest
from unittest.mock import Mock, patch
from src.BioBlend import connect_to_galaxy

class TestConnectToGalaxy:

    def test_get_galaxy_instance(self):
        """GalaxyInstance is called with correct URL and key"""
        with patch("src.BioBlend.connect_to_galaxy.GalaxyInstance") as mock:
            connect_to_galaxy.get_galaxy_instance()
            mock.assert_called_once_with(
                url=connect_to_galaxy.GALAXY_URL,
                key=connect_to_galaxy.API_KEY
            )

    def test_connection_success(self):
        """Test successful connection"""
        mock_gi = Mock()
        mock_gi.gi_version = "23.1"
        result = connect_to_galaxy.test_connection(mock_gi)
        assert result == {"status": "ok", "version": "23.1"}

    def test_connection_failure(self):
        """Test connection failure"""
        mock_gi = Mock()
        type(mock_gi).gi_version = property(lambda self: 1/0)  # raises exception
        result = connect_to_galaxy.test_connection(mock_gi)
        assert result["status"] == "error"
        assert "division by zero" in result["message"]

    def test_main_success(self):
        """Test main() with successful connection"""
        mock_gi = Mock()
        mock_gi.gi_version = "23.1"
        with patch("src.BioBlend.connect_to_galaxy.get_galaxy_instance", return_value=mock_gi), \
             patch("builtins.print") as mock_print:
            connect_to_galaxy.main()
            mock_print.assert_any_call("Connecting to Galaxy...")
            mock_print.assert_any_call("Connected successfully! Galaxy version: 23.1")

    def test_main_failure(self):
        """Test main() when connection fails"""
        mock_gi = Mock()
        type(mock_gi).gi_version = property(lambda self: 1/0)
        with patch("src.BioBlend.connect_to_galaxy.get_galaxy_instance", return_value=mock_gi), \
             patch("builtins.print") as mock_print:
            connect_to_galaxy.main()
            mock_print.assert_any_call("Connecting to Galaxy...")
            assert any("Connection failed:" in call.args[0] for call in mock_print.call_args_list)
