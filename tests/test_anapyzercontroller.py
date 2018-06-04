import unittest
import unittest.mock
# Import the AnaPyzerModel class
from anapyzercontroller import AnaPyzerController
from anapyzermodel import *

class TestAnaPyzerControllerMethods(unittest.TestCase):
    def setUp(self):
        self.modelMock = unittest.mock.Mock()
        self.viewMock = unittest.mock.Mock()
        self.controller = AnaPyzerController(self.modelMock, self.viewMock)

    def test_open_file_button_clicked_graph_mode_valid_file_single_day(self):
        self.modelMock.get_file_parse_mode.return_value = FileParseModes.GRAPH
        self.modelMock.get_graph_data_split.return_value = {}
        self.controller.open_file_button_clicked()

        self.modelMock.get_file_parse_mode.assert_called_once()
        self.modelMock.create_graph_data.assert_called_once()
        self.modelMock.get_graph_data_split.assert_called()

    def test_open_file_button_clicked_graph_mode_valid_file_multiple_days(self):
        self.modelMock.get_file_parse_mode.return_value = FileParseModes.GRAPH
        self.modelMock.get_graph_data_split.return_value = [{}, {}]
        self.controller.open_file_button_clicked()

        self.modelMock.get_file_parse_mode.assert_called_once()
        self.modelMock.create_graph_data.assert_called_once()
        self.modelMock.get_graph_data_split.assert_called()

    def test_open_file_button_clicked_graph_mode_invalid_file(self):
        self.modelMock.get_file_parse_mode.return_value = FileParseModes.GRAPH
        self.modelMock.create_graph_data.side_effect = AnaPyzerModelError("Invalid file")
        self.controller.open_file_button_clicked()

        self.modelMock.get_file_parse_mode.assert_called_once()
        self.modelMock.create_graph_data.assert_called_once()
        self.viewMock.display_error_message.assert_called_once()

    def test_open_file_button_clicked_report_mode_valid_file(self):
        self.modelMock.get_file_parse_mode.return_value = FileParseModes.REPORT
        self.controller.open_file_button_clicked()

        self.modelMock.get_file_parse_mode.assert_called_once()
        self.modelMock.create_report_data.assert_called_once()
        self.modelMock.get_report_data.assert_called_once()


    def test_open_file_button_clicked_report_mode_invalid_file(self):
        self.modelMock.get_file_parse_mode.return_value = FileParseModes.REPORT
        self.modelMock.create_report_data.side_effect = AnaPyzerModelError("Invalid file")
        self.controller.open_file_button_clicked()

        self.modelMock.get_file_parse_mode.assert_called_once()
        self.modelMock.create_report_data.assert_called_once()
        self.viewMock.display_error_message.assert_called_once()

    def test_open_file_button_clicked_csv_mode_valid_file(self):
        self.modelMock.get_file_parse_mode.return_value = FileParseModes.CSV
        self.controller.open_file_button_clicked()

        self.modelMock.get_file_parse_mode.assert_called_once()
        self.modelMock.convert_file_to_csv.assert_called_once()