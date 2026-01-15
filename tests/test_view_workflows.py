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
        """GalaxyInstance created with correct URL and key"""
        with patch('src.BioBlend.view_workflows.GalaxyInstance') as mock:
            view_workflows.get_galaxy_instance()
            mock.assert_called_once_with(
                url="http://localhost:8080",
                key="b8ba458fe9b1c919040db8288c56ed06"
            )

    def test_list_workflows_normal(self, mock_gi):
        """Test standard workflow listing"""
        result = view_workflows.list_workflows(mock_gi)
        assert len(result) == 1
        wf = result[0]
        assert wf['name'] == 'Test Workflow'
        assert wf['published'] is True
        assert wf['owner'] == 'N/A'
        assert 'steps' in wf
        mock_gi.workflows.get_workflows.assert_called_once()
        mock_gi.workflows.show_workflow.assert_called_once_with('wf-001')

    def test_list_workflows_empty(self, mock_gi):
        """Empty workflow list returns empty array"""
        mock_gi.workflows.get_workflows.return_value = []
        result = view_workflows.list_workflows(mock_gi)
        assert result == []

    def test_list_workflows_missing_fields(self, mock_gi):
        """Workflow missing 'published' or 'owner' fields defaults correctly"""
        mock_gi.workflows.get_workflows.return_value = [
            {'id': 'wf-002', 'name': 'No Fields'}
        ]
        mock_gi.workflows.show_workflow.return_value = {'steps': {}}
        result = view_workflows.list_workflows(mock_gi)
        wf = result[0]
        assert wf['published'] is False
        assert wf['owner'] == 'N/A'
        assert wf['steps'] == {}

    def test_list_workflows_show_failure(self, mock_gi):
        """If show_workflow raises an exception, test is caught"""
        mock_gi.workflows.get_workflows.return_value = [{'id': 'wf-003', 'name': 'Broken'}]
        mock_gi.workflows.show_workflow.side_effect = Exception("Galaxy API error")
        with pytest.raises(Exception) as exc:
            view_workflows.list_workflows(mock_gi)
        assert "Galaxy API error" in str(exc.value)

    def test_main_print_output(self, mock_gi):
        """Test main() prints workflow details"""
        with patch('src.BioBlend.view_workflows.get_galaxy_instance', return_value=mock_gi), \
             patch('builtins.print') as mock_print:
            view_workflows.main()
            mock_print.assert_any_call("Workflow: Test Workflow")
            mock_print.assert_any_call("Published: True, Owner: N/A")
            mock_print.assert_any_call("Steps: ['1']")
            mock_print.assert_any_call("-" * 40)
