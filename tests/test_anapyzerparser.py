import unittest
import unittest.mock
from anapyzerparser import AnaPyzerParser

class TestAnaPyzerParserMethods(unittest.TestCase):
    def setUp(self):
        # Instantiate the parser object
        self.parser = AnaPyzerParser()
        self.log_file_mock = unittest.mock.Mock()

    def test_parse_w3c_to_list_sample1(self):
        input = ["#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status time-taken",
                 "2016-05-16 00:00:00 51.48.162.235 GET /_Things/pictures/favicon-32x32.png - 80 - 52.232.212.188 Mozilla/5.0+(Windows+NT+6.1;+WOW64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/52.232.2662.102+Safari/537.36 http://www.campus.edu/ 200 0 0 315"]

        expected_output = {
            0: ['2016-05-16',
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
        'bytes-received': -1,
        'bytes-sent': -1,
        'c-ip': 8,
        'client-ip': 8,
        'cookie': -1,
        'cs(Cookie)': -1,
        'cs(Referer)': 10,
        'cs(UserAgent)': -1,
        'cs-bytes': -1,
        'cs-host': -1,
        'cs-method': 3,
        'cs-uri-query': 5,
        'cs-uri-stem': 4,
        'cs-username': 7,
        'date': 0,
        'fields': 1,
        'host': -1,
        'http-status': 11,
        'length': 1,
        'method': 3,
        'protocol-substatus': 12,
        'referer': 10,
        's-computername': -1,
        's-ip': 2,
        's-port': 6,
        's-sitename': -1,
        'sc-bytes': -1,
        'sc-status': 11,
        'sc-substatus': 12,
        'sc-win32-status': 13,
        'server-ip': 2,
        'server-name': -1,
        'server-port': 6,
        'service-name': -1,
        'time': 1,
        'time-taken': 14,
        'timestamp': 1,
        'uri-query': 5,
        'uri-stem': 4,
        'user-agent': -1,
        'username': 7,
        'win32-status': 13}

        self.log_file_mock.return_value = input

        output = self.parser.parse_w3c_to_list(self.log_file_mock())
        self.assertEqual(expected_output, output)

    def test_parse_w3c_to_list_sample2(self):
        input = ["#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status time-taken",
                 "2016-05-16 00:00:00 51.48.162.235 GET /_Things/pictures/favicon-32x32.png - 80 - 52.232.212.188 Mozilla/5.0+(Windows+NT+6.1;+WOW64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/52.232.2662.102+Safari/537.36 http://www.campus.edu/ 200 0 0 315",
                 "2016-05-16 00:00:00 51.48.162.235 GET /_Things/revolution/stuff/videos/home/home.mp4 - 80 - 26.25.144.84 Mozilla/5.0+(Windows+NT+10.0;+WOW64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/52.232.2662.102+Safari/537.36 http://www.campus.edu/ 206 0 0 41556"]
        expected_output = {
            0: ['2016-05-16',
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
            1: ['2016-05-16',
                '00:00:00',
                '51.48.162.235',
                'GET',
                '/_Things/revolution/stuff/videos/home/home.mp4',
                '-',
                '80',
                '-',
                '26.25.144.84',
                'Mozilla/5.0+(Windows+NT+10.0;+WOW64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/52.232.2662.102+Safari/537.36',
                'http://www.campus.edu/',
                '206',
                '0',
                '0',
                '41556'],
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
            'bytes-received': -1,
            'bytes-sent': -1,
            'c-ip': 8,
            'client-ip': 8,
            'cookie': -1,
            'cs(Cookie)': -1,
            'cs(Referer)': 10,
            'cs(UserAgent)': -1,
            'cs-bytes': -1,
            'cs-host': -1,
            'cs-method': 3,
            'cs-uri-query': 5,
            'cs-uri-stem': 4,
            'cs-username': 7,
            'date': 0,
            'fields': 1,
            'host': -1,
            'http-status': 11,
            'length': 2,
            'method': 3,
            'protocol-substatus': 12,
            'referer': 10,
            's-computername': -1,
            's-ip': 2,
            's-port': 6,
            's-sitename': -1,
            'sc-bytes': -1,
            'sc-status': 11,
            'sc-substatus': 12,
            'sc-win32-status': 13,
            'server-ip': 2,
            'server-name': -1,
            'server-port': 6,
            'service-name': -1,
            'time': 1,
            'time-taken': 14,
            'timestamp': 1,
            'uri-query': 5,
            'uri-stem': 4,
            'user-agent': -1,
            'username': 7,
            'win32-status': 13}

        self.log_file_mock.return_value = input

        output = self.parser.parse_w3c_to_list(self.log_file_mock())
        self.assertEqual(expected_output, output)

    def test_parse_w3c_to_list_bad_file(self):
        input = [""]
        self.log_file_mock.return_value = input
        self.assertRaises(IndexError, self.parser.parse_w3c_to_list, self.log_file_mock())

    def test_parse_common_apache_to_list_sample1(self):
        input = ["73.83.18.52 - - [04/Apr/2018:19:30:50 +0000] \"GET / HTTP/1.1\" 200 1108 \"-\" \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36\""]

        expected_output = {0: ['04/Apr/2018', '19:30:50', '73.83.18.52', 'GET ', '/', '200', '1108', '-'],
                             'bytes-sent': 6,
                             'client-ip': 2,
                             'date': 0,
                             'length': 1,
                             'method': 3,
                             'referer': 7,
                             'sc-status': 5,
                             'timestamp': 1,
                             'uri-stem': 4}

        self.log_file_mock.return_value = input

        output = self.parser.parse_common_apache_to_list(self.log_file_mock())
        self.assertEqual(expected_output, output)

    def test_parse_common_apache_to_list_sample2(self):
        input = ["73.83.18.52 - - [04/Apr/2018:19:30:50 +0000] \"GET / HTTP/1.1\" 200 1108 \"-\" \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36\"",
                 "73.83.18.52 - - [04/Apr/2018:19:30:50 +0000] \"GET /css/style.css HTTP/1.1\" 200 1209 \"http://www.avsift.com/\" \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36\""]
        expected_output = {
            0: ['04/Apr/2018', '19:30:50', '73.83.18.52', 'GET ', '/', '200', '1108', '-'],
            1: ['04/Apr/2018', '19:30:50', '73.83.18.52', 'GET ', '/css/style.css', '200', '1209', '-'],
             'bytes-sent': 6,
             'client-ip': 2,
             'date': 0,
             'length': 2,
             'method': 3,
             'referer': 7,
             'sc-status': 5,
             'timestamp': 1,
             'uri-stem': 4}

        self.log_file_mock.return_value = input

        output = self.parser.parse_common_apache_to_list(self.log_file_mock())
        self.assertEqual(expected_output, output)

    def test_parse_common_apache_to_list_bad_file(self):
        input = [""]
        self.log_file_mock.return_value = input
        self.assertRaises(IndexError, self.parser.parse_common_apache_to_list, self.log_file_mock())