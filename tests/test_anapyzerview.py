import unittest
import unittest.mock
# Import the AnaPyzerView class
from anapyzerview import AnaPyzerView

class TestAnaPyzerViewMethods(unittest.TestCase):
    def setUp(self):
        self.controllerMock = unittest.mock.Mock()
        self.controllerMock.in_file_browse_button_clicked()

    def test_add_in_file_browse_button_clicked_listener_is_called(self):
        view = AnaPyzerView()
        view.add_in_file_browse_button_clicked_listener(self.controllerMock.in_file_browse_button_clicked)
        view._in_file_browse_button.invoke()
        self.controllerMock.in_file_browse_button_clicked.assert_called()

    def test_add_graph_mode_option_changed_listener(self):
        self.assertTrue(False)

    def test_show_graph_mode_option_menu_widgets(self):
        self.assertTrue(False)

    def test_display_error_message(self):
        self.assertTrue(False)

    def test_show_out_file_path_widgets(self):
        self.assertTrue(False)

    def set_file_read_options(self):
        self.assertTrue(False)

    def test_resize_entry_field(self):
        self.assertTrue(False)

    def test_display_in_file_select_prompt(self):
        self.assertTrue(False)

    def test_enable_open_file_button(self):
        self.assertTrue(False)

    def test_add_file_read_option_changed_listener(self):
        self.assertTrue(False)

    def test_disable_open_file_button(self):
        self.assertTrue(False)

    def test_display_out_file_select_prompt(self):
        self.assertTrue(False)

    def test_hide_graph_mode_option_menu_widgets(self):
        self.assertTrue(False)

    def test_set_log_type_options(self):
        self.assertTrue(False)

    def test_display_graph_view(self):
        self.assertTrue(False)

    def test_add_open_file_button_clicked_listener(self):
        self.assertTrue(False)

    def test_add_in_file_browse_button_clicked_listener(self):
        self.assertTrue(False)

    def test_set_graph_mode_options(self):
        self.assertTrue(False)

    def test_set_out_file_path(self):
        self.assertTrue(False)

    def test_add_log_type_option_changed_listener(self):
        self.assertTrue(False)

    def test_add_out_file_browse_button_clicked_listener(self):
        self.assertTrue(False)

    def test_set_in_file_path(self):
        self.assertTrue(False)

    def test_display_success_message(self):
        self.assertTrue(False)

    def test_display_connections_plot(self):
        self.assertTrue(False)

    def test_hide_out_file_path_widgets(self):
        self.assertTrue(False)