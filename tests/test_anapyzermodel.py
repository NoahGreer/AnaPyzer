import unittest
import unittest.mock
# Import the AnaPyzerModel class
from anapyzermodel import AnaPyzerModel

class TestAnaPyzerModelMethods(unittest.TestCase):
    def setUp(self):
        self.model = AnaPyzerModel()
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
        input = ["#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status time-taken",
                 "2016-05-16 00:00:00 51.48.162.235 GET /_Things/pictures/favicon-32x32.png - 80 - 52.232.212.188 Mozilla/5.0+(Windows+NT+6.1;+WOW64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/52.232.2662.102+Safari/537.36 http://www.campus.edu/ 200 0 0 315"]
        expected_output = {0: ['2016-05-16',
                                 '00:00:00',
                                 '51.48.162.235',
                                 'GET',
                                 '/_Things/pictures/favicon-32x32.png',
                                 '-',
                                 '80',
                                 '-',
                                 '52.232.212.188',
                                 'Mozilla/5.0+(Windows+NT+6.1;+WOW64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/52.232.2662.102+Safari/537.36',
                                 'http://www.campus.edu/',
                                 '200',
                                 '0',
                                 '0',
                                 '315'],
                             '#Fields:': ['#Fields:',
                                          'date',
                                          'time',
                                          's-ip',
                                          'cs-method',
                                          'cs-uri-stem',
                                          'cs-uri-query',
                                          's-port',
                                          'cs-username',
                                          'c-ip',
                                          'cs(User-Agent)',
                                          'cs(Referer)',
                                          'sc-status',
                                          'sc-substatus',
                                          'sc-win32-status',
                                          'time-taken'],
                             'c-ip': 8,
                             'cs(Cookie)': -1,
                             'cs(Referrer)': -1,
                             'cs(UserAgent)': -1,
                             'cs-bytes': -1,
                             'cs-host': -1,
                             'cs-method': 3,
                             'cs-uri-query': 5,
                             'cs-uri-stem': 4,
                             'cs-username': 7,
                             'date': 0,
                             'length': 1,
                             's-computername': -1,
                             's-ip': 2,
                             's-port': 6,
                             's-sitename': -1,
                             'sc-bytes': -1,
                             'sc-status': 11,
                             'sc-substatus': 12,
                             'sc-win32-status': 13,
                             'time': 1,
                             'time-taken': 14}

        self.log_file_mock.return_value = input

        output = self.model.parse_w3c_to_list(self.log_file_mock())
        self.assertEqual(output, expected_output)

    def test_get_connections_per_hour(self):
        self.assertTrue(False)

    def test_plot_connections(self):
        self.assertTrue(False)