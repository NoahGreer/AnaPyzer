import unittest
import unittest.mock
# Import the AnaPyzerModel class
from anapyzermodel import AnaPyzerModel

class TestAnaPyzerModelMethods(unittest.TestCase):
    def setUp(self):
        # Instantiate the mock parser object to be passed to the model
        self.parserMock = unittest.mock.Mock()
        # Instantiate the mock analyzer object to be passed to the model
        self.analyzerMock = unittest.mock.Mock()
        self.model = AnaPyzerModel(self.parserMock, self.analyzerMock)
        self.log_file_mock = unittest.mock.Mock()

    # If a blank string is passed, then the model should just set the path to the default path
    def test_set_in_file_path_blank(self):
        self.model.set_in_file_path('')
        self.assertEqual(str(self.model.DEFAULT_FILE_PATH), self.model.get_in_file_path())

    # If a file path string is passed, then the model should store that file path
    def test_set_in_file_path_string(self):
        self.model.set_in_file_path('')
        self.assertEqual(str(self.model.DEFAULT_FILE_PATH), self.model.get_in_file_path())

    def test_get_connections_per_hour(self):
        self.assertTrue(False)

    def test_plot_connections(self):
        self.assertTrue(False)