import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Software.Utilities import FileManager, CompressionUtility, SystemCleaner

class TestUtilities:
    @pytest.fixture
    def sample_file_manager(self):
        return FileManager()

    def test_file_manager_initialization(self, sample_file_manager):
        assert sample_file_manager.current_directory == "/"

    def test_file_manager_list_files(self, sample_file_manager):
        files = sample_file_manager.list_files()
        assert isinstance(files, list)

    def test_file_manager_comprehensive(self):
        fm = FileManager()

        # Test directory operations
        fm.create_directory("docs")
        fm.create_directory("pictures")

        # Test file operations (mock)
        files = fm.list_files()
        assert isinstance(files, list)

        fm.delete_file("old_file.txt")

        # Test current directory
        fm.current_directory = "/home/user"
        assert fm.current_directory == "/home/user"

    def test_compression_utility(self):
        comp = CompressionUtility()

        # Test compression
        files = ["file1.txt", "file2.jpg", "file3.pdf"]
        result = comp.compress_files(files, "archive.zip")
        assert result is True

        # Test extraction
        result = comp.extract_files("archive.zip", "/tmp/extract")
        assert result is True

        # Test supported formats
        assert len(comp.supported_formats) > 0
        assert 'zip' in comp.supported_formats

    def test_system_cleaner(self):
        cleaner = SystemCleaner()

        # Test scanning
        junk_count = cleaner.scan_system()
        assert junk_count >= 0
        assert len(cleaner.temp_files) >= 0
        assert len(cleaner.cache_directories) >= 0

        # Test cleaning
        cleaned_count = cleaner.clean_system()
        assert cleaned_count == junk_count
        assert len(cleaner.temp_files) == 0
        assert len(cleaner.cache_directories) == 0