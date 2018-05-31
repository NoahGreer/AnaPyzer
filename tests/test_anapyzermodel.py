import unittest
import unittest.mock
# Import the AnaPyzerModel class
from anapyzermodel import AnaPyzerModel
from anapyzerparser import AnaPyzerParser
from anapyzeranalyzer import AnaPyzerAnalyzer

class TestAnaPyzerModelMethods(unittest.TestCase):
    def setUp(self):
        # Instantiate the parser object to be passed to the model
        parser = AnaPyzerParser()
        # Instantiate the analyzer object to be passed to the model
        analyzer = AnaPyzerAnalyzer()
        self.model = AnaPyzerModel(parser, analyzer)
        self.log_file_mock = unittest.mock.Mock()

    # If a blank string is passed, then the model should just set the path to the default path
    def test_set_in_file_path_blank(self):
        self.model.set_in_file_path('')
        self.assertEqual(str(self.model.DEFAULT_FILE_PATH), self.model.get_in_file_path())

    # If a file path string is passed, then the model should store that file path
    def test_set_in_file_path_string(self):
        self.model.set_in_file_path('')
        self.assertEqual(str(self.model.DEFAULT_FILE_PATH), self.model.get_in_file_path())

    def test_get_in_file_path(self):
        self.assertEqual(self.model.get_in_file_path(), str(self.model.DEFAULT_FILE_PATH))

    def test_in_file_path_is_valid(self):
        self.assertTrue(False)

    def test_set_out_file_path(self):
        self.assertTrue(False)

    def test_get_out_file_path(self):
        self.assertTrue(False)

    def test_out_file_path_is_valid(self):
        self.assertTrue(False)

    def test_set_log_type(self):
        self.assertTrue(False)

    def test_get_log_type(self):
        self.assertTrue(False)

    def test_add_error_listener(self):
        self.assertTrue(False)

    def test_add_success_listener(self):
        self.assertTrue(False)

    def test_get_connections_per_hour(self):
        self.assertTrue(False)

    def test_plot_connections(self):
        self.assertTrue(False)