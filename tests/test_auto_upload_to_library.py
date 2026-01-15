import pytest
from unittest.mock import Mock, patch
from src.BioBlend import auto_upload_to_library

class TestAutoUploadToLibrary:

    @pytest.fixture
    def mock_gi(self):
        """Mock GalaxyInstance with multiple libraries, creation, upload, and contents"""
        gi = Mock()
        # Existing libraries
        gi.libraries.get_libraries.return_value = [
            {'id': 'lib-001', 'name': 'Test Library'},
            {'id': 'lib-002', 'name': 'Other Library'}
        ]
        # Library creation
        gi.libraries.create_library.return_value = {'id': 'lib-003'}
        # File upload
        gi.libraries.upload_file_from_local_path.return_value = [{'id': 'ds-001'}]
        # Library contents
        gi.libraries.show_library.return_value = [
            {'name': 'dataset1', 'type': 'fastqsanger', 'id': 'ds-001'}
        ]
        return gi

    # ---------------------------
    # Core function tests
    # ---------------------------
    def test_connect_galaxy(self):
        with patch('src.BioBlend.auto_upload_to_library.GalaxyInstance') as mock:
            auto_upload_to_library.connect_galaxy("url", "key")
            mock.assert_called_once_with(url="url", key="key")

    def test_select_or_create_library_existing(self, mock_gi):
        lib_id = auto_upload_to_library.select_or_create_library(mock_gi, "Other Library", "Desc")
        assert lib_id == 'lib-002'
        mock_gi.libraries.get_libraries.assert_called_once()

    def test_select_or_create_library_new(self, mock_gi):
        lib_id = auto_upload_to_library.select_or_create_library(mock_gi, "New Library", "Desc")
        assert lib_id == 'lib-003'
        mock_gi.libraries.create_library.assert_called_once_with(name="New Library", description="Desc")

    def test_upload_file_success(self, mock_gi, tmp_path):
        test_file = tmp_path / "file.fastq"
        test_file.write_text("dummy content")
        dataset_id = auto_upload_to_library.upload_file(mock_gi, 'lib-001', str(test_file), 'fastqsanger')
        assert dataset_id == 'ds-001'

    def test_upload_file_not_found(self, mock_gi):
        with pytest.raises(FileNotFoundError):
            auto_upload_to_library.upload_file(mock_gi, 'lib-001', 'nonexistent.fastq', 'fastqsanger')

    def test_show_library_contents(self, mock_gi):
        contents = auto_upload_to_library.show_library_contents(mock_gi, 'lib-001')
        assert contents == [('dataset1', 'fastqsanger', 'ds-001')]
        mock_gi.libraries.show_library.assert_called_once_with('lib-001', contents=True)

    # ---------------------------
    # High-level wrapper tests
    # ---------------------------
    def test_perform_upload_workflow_existing_library(self, mock_gi, tmp_path):
        test_file = tmp_path / "file.fastq"
        test_file.write_text("dummy content")
        lib_id, ds_id, contents = auto_upload_to_library.perform_upload_workflow(
            mock_gi,
            file_name=str(test_file),
            file_type='fastqsanger',
            library_name='Test Library',
            library_desc='Desc'
        )
        assert lib_id == 'lib-001'
        assert ds_id == 'ds-001'
        assert contents == [('dataset1', 'fastqsanger', 'ds-001')]

    def test_perform_upload_workflow_new_library(self, mock_gi, tmp_path):
        mock_gi.libraries.get_libraries.return_value = []
        test_file = tmp_path / "file.fastq"
        test_file.write_text("dummy content")
        lib_id, ds_id, contents = auto_upload_to_library.perform_upload_workflow(
            mock_gi,
            file_name=str(test_file),
            file_type='fastqsanger',
            library_name='New Library',
            library_desc='Desc'
        )
        assert lib_id == 'lib-003'
        assert ds_id == 'ds-001'
        assert contents == [('dataset1', 'fastqsanger', 'ds-001')]
        mock_gi.libraries.create_library.assert_called_once_with(name='New Library', description='Desc')

    # ---------------------------
    # Environment variables test
    # ---------------------------
    def test_get_env_variables_defaults(self):
        with patch('src.BioBlend.auto_upload_to_library.os.getenv') as mock_getenv, \
             patch('src.BioBlend.auto_upload_to_library.load_dotenv'):
            mock_getenv.side_effect = lambda key, default=None: default
            env = auto_upload_to_library.get_env_variables()
            assert env["GALAXY_URL"] == "http://localhost:8080"
            assert env["API_KEY"] == "b8ba458fe9b1c919040db8288c56ed06"
            assert env["FILE_NAME"] == "bioblend_history.fastq"
            assert env["FILE_TYPE"] == "fastqsanger"
            assert env["NEW_LIBRARY_NAME"] == "MyLibrary"
            assert "Automatically created library" in env["NEW_LIBRARY_DESC"]

    # ---------------------------
    # Main function tests
    # ---------------------------
    def test_main_success(self, mock_gi, tmp_path):
        test_file = tmp_path / "file.fastq"
        test_file.write_text("dummy content")

        with patch('src.BioBlend.auto_upload_to_library.get_env_variables') as mock_env, \
             patch('src.BioBlend.auto_upload_to_library.connect_galaxy') as mock_connect, \
             patch('builtins.print') as mock_print:
            mock_env.return_value = {
                "GALAXY_URL": "url",
                "API_KEY": "key",
                "FILE_NAME": str(test_file),
                "FILE_TYPE": "fastqsanger",
                "NEW_LIBRARY_NAME": "Test Library",
                "NEW_LIBRARY_DESC": "Desc"
            }
            mock_connect.return_value = mock_gi

            auto_upload_to_library.main()

            mock_print.assert_any_call("Connected to Galaxy.")
            mock_print.assert_any_call("Using library ID: lib-001")
            mock_print.assert_any_call("File uploaded successfully! Dataset ID: ds-001")

    def test_main_file_not_found(self, mock_gi):
        with patch('src.BioBlend.auto_upload_to_library.get_env_variables') as mock_env, \
             patch('src.BioBlend.auto_upload_to_library.connect_galaxy') as mock_connect, \
             patch('builtins.print') as mock_print:
            mock_env.return_value = {
                "GALAXY_URL": "url",
                "API_KEY": "key",
                "FILE_NAME": "missing_file.fastq",
                "FILE_TYPE": "fastqsanger",
                "NEW_LIBRARY_NAME": "Test Library",
                "NEW_LIBRARY_DESC": "Desc"
            }
            mock_connect.return_value = mock_gi

            auto_upload_to_library.main()
            mock_print.assert_any_call("Connected to Galaxy.")
            mock_print.assert_any_call("Error: File not found: missing_file.fastq")
