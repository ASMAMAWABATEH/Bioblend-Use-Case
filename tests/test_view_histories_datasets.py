# tests/test_view_histories_datasets.py
import pytest
from unittest.mock import Mock, patch
import src.BioBlend.view_histories_datasets as view_histories_datasets

class TestViewHistoriesDatasets:

    @pytest.fixture
    def mock_gi(self):
        """Mock GalaxyInstance with histories and datasets"""
        gi = Mock()

        # Mock get_histories to return a single history
        gi.histories.get_histories.return_value = [
            {'id': 'hist1', 'name': 'History 1', 'state': 'ok'}
        ]

        # Mock show_history to return datasets for the history
        gi.histories.show_history.return_value = [
            {'id': 'ds1', 'name': 'Dataset 1', 'state': 'ok', 'deleted': False},
            {'id': 'ds2', 'name': 'Dataset 2', 'state': 'ok', 'deleted': False}
        ]

        return gi

    def test_fetch_histories(self, mock_gi):
        """Test fetching histories with datasets"""
        result = view_histories_datasets.fetch_histories(mock_gi)

        assert len(result) == 1
        h = result[0]
        assert h['name'] == 'History 1'
        assert h['state'] == 'ok'
        assert len(h['datasets']) == 2
        assert h['datasets'][0]['name'] == 'Dataset 1'
        assert h['datasets'][1]['name'] == 'Dataset 2'

    def test_fetch_histories_empty(self):
        """Test empty histories list is handled correctly"""
        mock_gi = Mock()
        mock_gi.histories.get_histories.return_value = []

        result = view_histories_datasets.fetch_histories(mock_gi)
        assert result == []

    def test_format_histories_output(self):
        """Test formatting of histories and datasets"""
        histories = [
            {
                'id': 'hist1',
                'name': 'History 1',
                'state': 'ok',
                'datasets': [
                    {'id': 'ds1', 'name': 'Dataset 1', 'state': 'ok', 'deleted': False}
                ]
            },
            {
                'id': 'hist2',
                'name': 'Empty History',
                'state': 'new',
                'datasets': []
            }
        ]

        output = view_histories_datasets.format_histories_output(histories)

        # Check first history with datasets
        assert any("History: History 1 | State: ok" in line for line in output)
        assert any("Dataset: Dataset 1 | State: ok | Deleted: False" in line for line in output)

        # Check second history with no datasets
        assert any("History: Empty History | State: new" in line for line in output)
        assert any("No datasets" in line for line in output)

    def test_get_galaxy_instance(self):
        """GalaxyInstance should be created with correct URL and key"""
        with patch("src.BioBlend.view_histories_datasets.GalaxyInstance") as mock_gi_class:
            gi = view_histories_datasets.get_galaxy_instance()
            mock_gi_class.assert_called_once_with(
                url=view_histories_datasets.GALAXY_URL,
                key=view_histories_datasets.API_KEY
            )
