# tests/test_view_workflows.py
import pytest
from unittest.mock import Mock, patch
from src.BioBlend import view_workflows

class TestViewWorkflows:

    @pytest.fixture
    def mock_gi(self):
        """Fixture for a mocked GalaxyInstance"""
        gi = Mock()
        gi.workflows.get_workflows.return_value = [
            {'id': 'wf-001', 'name': 'Test Workflow', 'published': True}
        ]
        gi.workflows.show_workflow.return_value = {
            'steps': {'1': {'tool_id': 'cat1', 'label': 'test'}}
        }
        return gi

    def test_get_galaxy_instance(self):
        """Test that GalaxyInstance is created with correct parameters"""
        # Patch where GalaxyInstance is imported, not where it's defined
        with patch('src.BioBlend.view_workflows.GalaxyInstance') as mock:
            view_workflows.get_galaxy_instance()
            mock.assert_called_once_with(
                url="http://localhost:8080",
                key="b8ba458fe9b1c919040db8288c56ed06"
            )

    def test_list_workflows(self, mock_gi):
        """Test listing of workflows"""
        result = view_workflows.list_workflows(mock_gi)
        assert len(result) == 1
        assert result[0]['name'] == 'Test Workflow'
        assert result[0]['published'] is True
        assert 'steps' in result[0]
        mock_gi.workflows.get_workflows.assert_called_once()
        mock_gi.workflows.show_workflow.assert_called_once_with('wf-001')

    def test_list_workflows_empty(self, mock_gi):
        """Test handling of empty workflow list"""
        mock_gi.workflows.get_workflows.return_value = []
        result = view_workflows.list_workflows(mock_gi)
        assert result == []
