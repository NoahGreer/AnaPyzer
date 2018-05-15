import unittest
import unittest.mock
# Import the AnaPyzerModel class
from anapyzermodel import AnaPyzerModel

class TestAnaPyzerModelMethods(unittest.TestCase):
    def setUp(self):
        self.model = AnaPyzerModel()

    def test_set_in_file_path_blank(self):
        self.model.set_in_file_path('')
        self.assertEqual(str(self.model.DEFAULT_FILE_PATH), self.model.get_in_file_path())

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

    def test_set_file_parse_mode(self):
        self.assertTrue(False)

    def test_get_file_parse_mode(self):
        self.assertTrue(False)

    def test_set_graph_mode(self):
        self.assertTrue(False)

    def test_get_graph_mode(self):
        self.assertTrue(False)

    def test_read_file_to_csv(self):
        self.assertTrue(False)

    def test_add_error_listener(self):
        self.assertTrue(False)

    def test_add_success_listener(self):
        self.assertTrue(False)

    def test_parse_w3c_to_list(self):
        self.assertTrue(False)

    def test_get_connections_per_hour(self):
        self.assertTrue(False)

    def test_announce_connections(self):
        self.assertTrue(False)

    def test_plot_connections(self):
        self.assertTrue(False)