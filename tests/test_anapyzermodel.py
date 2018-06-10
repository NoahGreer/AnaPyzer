import unittest
import unittest.mock
# Import the AnaPyzerModel class
from anapyzermodel import AnaPyzerModel
# Import the pathlib library for cross platform file path abstraction
import pathlib

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
        path = pathlib.Path.home()
        self.model.set_in_file_path(path)
        self.assertEqual(str(path), self.model.get_in_file_path())

    # If a blank string is passed, then the model should just set the path to the default path
    def test_set_out_file_path_blank(self):
        self.model.set_out_file_path('')
        self.assertEqual(str(self.model.DEFAULT_FILE_PATH), self.model.get_out_file_path())

    # If a file path string is passed, then the model should store that file path
    def test_set_out_file_path_string(self):
        path = pathlib.Path.home()
        self.model.set_out_file_path(path)
        self.assertEqual(str(path), self.model.get_out_file_path())