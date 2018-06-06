import unittest
import unittest.mock
# Import the AnaPyzerView class
from anapyzerview import AnaPyzerView

class TestAnaPyzerViewMethods(unittest.TestCase):
    def setUp(self):
        self.view = AnaPyzerView()
        self.controller_mock = unittest.mock.Mock()

    def test_log_type_option_changed_listener_is_called(self):
        self.view.add_log_type_option_changed_listener(self.controller_mock.log_type_option_changed)
        self.view._log_type_option_menu['menu'].invoke(0)
        self.controller_mock.log_type_option_changed.assert_called_once()

    def test_in_file_browse_button_clicked_listener_is_called(self):
        self.view.add_in_file_browse_button_clicked_listener(self.controller_mock.in_file_browse_button_clicked)
        self.view._in_file_browse_button.invoke()
        self.controller_mock.in_file_browse_button_clicked.assert_called_once()

    def test_file_read_option_changed_listener_is_called(self):
        self.view.add_file_read_option_changed_listener(self.controller_mock.file_read_option_changed)
        self.view._file_read_option_menu['menu'].invoke(0)
        self.controller_mock.file_read_option_changed.assert_called_once()

    def test_graph_mode_option_changed_listener_is_called(self):
        self.view.add_graph_mode_option_changed_listener(self.controller_mock.graph_mode_option_changed)
        self.view._graph_mode_option_menu['menu'].invoke(0)
        self.controller_mock.graph_mode_option_changed.assert_called_once()

    def test_out_file_browse_button_clicked_listener_is_called(self):
        self.view.add_out_file_browse_button_clicked_listener(self.controller_mock.out_file_browse_button_clicked)
        self.view._out_file_browse_button.invoke()
        self.controller_mock.out_file_browse_button_clicked.assert_called_once()

    def test_open_file_button_clicked_listener_is_called(self):
        self.view.add_open_file_button_clicked_listener(self.controller_mock.open_file_button_clicked)
        self.view._open_file_button.invoke()
        self.controller_mock.open_file_button_clicked.assert_called_once()