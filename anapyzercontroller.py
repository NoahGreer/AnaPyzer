# Import the AnaPyzerModel class
from anapyzermodel import *

# Class definition for the Controller part of the MVC design pattern


class AnaPyzerController:
    # Constructor
    # Takes a view and a model object
    def __init__(self, model, view):
        # Set the controller's reference to the application model object
        self.model = model
        # Set the controller's reference to the application view object
        self.view = view

    # Start the application
    def run(self):
        self.init_view()
        self.update_view()
        self.view.mainloop()

    # Function for initializing the view with values from the model and registering listeners
    def init_view(self):
        # Set the available options for the view's options menu
        self.view.set_log_type_options([log_type.value for log_type in AcceptedLogTypes])
        self.view.set_file_read_options([parse_mode.value for parse_mode in FileParseModes])
        self.view.set_graph_mode_options([graph_mode.value for graph_mode in GraphModes])
        self.view.set_report_mode_options([report_mode.value for report_mode in ReportModes])
        self.view.set_in_file_path(self.model.get_in_file_path())
        self.view.set_out_file_path(self.model.get_out_file_path())

        # Register listeners in the view
        self.view.set_in_file_browse_button_clicked_listener(self.in_file_browse_button_clicked)
        self.view.set_out_file_browse_button_clicked_listener(self.out_file_browse_button_clicked)
        self.view.set_open_file_button_clicked_listener(self.open_file_button_clicked)
        self.view.set_log_type_option_changed_listener(self.log_type_option_changed)
        self.view.set_file_read_option_changed_listener(self.file_read_option_changed)
        self.view.set_graph_mode_option_changed_listener(self.graph_mode_option_changed)
        self.view.set_report_mode_option_changed_listener(self.report_mode_option_changed)

    # Function for updating the state of the view based on what has been set in the model
    def update_view(self):
        # Set the input and output file paths to those set in the model
        self.view.set_in_file_path(str(self.model.get_in_file_path()))
        self.view.set_out_file_path(str(self.model.get_out_file_path()))

        # Hide all optional widgets by default
        self.view.hide_graph_mode_option_menu_widgets()
        self.view.hide_report_mode_option_menu_widgets()
        self.view.hide_out_file_path_widgets()
        self.view.disable_open_file_button()

        # Show only the widgets that pertain to the current parse mode
        if self.model.get_file_parse_mode() == FileParseModes.GRAPH:
            self.view.show_graph_mode_option_menu_widgets()
            if self.model.in_file_path_is_valid():
                self.view.enable_open_file_button()
        elif self.model.get_file_parse_mode() == FileParseModes.REPORT:
            self.view.show_report_mode_option_menu_widgets()
            if self.model.in_file_path_is_valid():
                self.view.enable_open_file_button()
        elif self.model.get_file_parse_mode() == FileParseModes.CSV:
            self.view.show_out_file_path_widgets()
            if self.model.in_file_path_is_valid() and self.model.out_file_path_is_valid():
                self.view.enable_open_file_button()
        
    # Listener for when the log type option menu has an item selected
    def log_type_option_changed(self, value):
        self.model.set_log_type(value)
        self.update_view()

    # Handler for when the log type option menu has an item selected
    def file_read_option_changed(self, value):
        self.model.set_file_parse_mode(value)
        self.update_view()

    # Handler for when the graph mode option menu has an item selected
    def graph_mode_option_changed(self, value):
        self.model.set_graph_mode(value)
        self.update_view()

    # Handler for when the report mode option menu has an item selected
    def report_mode_option_changed(self, value):
        self.model.set_report_mode(value)
        self.update_view()

    # Function for handling when the in file "Browse..." button is pressed
    def in_file_browse_button_clicked(self):
        # Get a new file path by prompting the user with a file selection dialog
        in_file_path = self.view.display_in_file_select_prompt(
            self.model.get_in_file_path(),
            [file_format.value for file_format in AcceptedFileFormats])

        # Update the input file path to the one received from the user via the file dialog
        self.model.set_in_file_path(in_file_path)
        self.update_view()

    # Function for handling when the out file "Browse..." button is pressed
    def out_file_browse_button_clicked(self):
        # Get a new file path by prompting the user with a file selection dialog
        out_file_path = self.view.display_out_file_select_prompt(
            self.model.get_out_file_path(),
            [file_format.value for file_format in OutputFileFormats])

        # Update the input file path to the one received from the user via the file dialog
        self.model.set_out_file_path(out_file_path)
        self.update_view()

    # Function for handling when the "Open" button is pressed
    def open_file_button_clicked(self):
        parse_mode = self.model.get_file_parse_mode()

        if parse_mode == FileParseModes.GRAPH:
            try:
                self.model.create_graph_data()
            except AnaPyzerModelError as e:
                self._on_error(e.message)
                return False

            # model.get_graph_data_split will check whether the graph data is split by date/time/any other delimiter
            # and allow multiple graphs to be created if it is
            # print(self.model.get_graph_data_split())
            if len(self.model.get_graph_data_split()) > 0:
                for value in self.model.get_graph_data_split():
                    self.view.display_graph_view(self.model.get_graph_data_split_keys(value),
                                                 self.model.get_graph_data_split_values(value),
                                                 self.model.get_graph_data_x_label(),
                                                 self.model.get_graph_data_y_label(),
                                                 value)
            else:
                self.view.display_graph_view(self.model.get_graph_data_keys(),
                                             self.model.get_graph_data_values(),
                                             self.model.get_graph_data_x_label(),
                                             self.model.get_graph_data_y_label(),
                                             self.model.get_graph_data_title())

        elif parse_mode == FileParseModes.REPORT:
            try:
                self.model.create_report_data()
            except AnaPyzerModelError as e:
                self._on_error(e.message)
                return False

            self.view.display_report_view(self.model.get_report_data())

        elif parse_mode == FileParseModes.CSV:
            try:
                if self.model.export_log_to_csv():
                    self._on_success("Converted to csv successfully.")
            except AnaPyzerModelError as e:
                self._on_error(e.message)
                return False

    # Method to call when an error occurs
    def _on_error(self, message):
        self.view.display_error_message(message)

    # Method to call when an action completed successfully
    def _on_success(self, message):
        self.view.display_success_message(message)
