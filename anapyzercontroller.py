# Import the AnaPyzerModel class
from anapyzermodel import *
# Import the AnaPyzerView class
from anapyzerview import *
# Import the pathlib library for cross platform file path abstraction
import pathlib


# Class definition for the Controller part of the MVC design pattern
class AnaPyzerController:
    # Constructor
    # Takes a view and a model object
    def __init__(self, view, model):
        # Set the controller's reference to the application view object
        self.view = view
        # Set the controller's reference to the application model object
        self.model = model

        # Set the available options for the view's options menu
        self.view.set_log_type_options([log_type.value for log_type in AcceptedLogTypes])
        self.view.set_file_read_options([parse_mode.value for parse_mode in FileParseModes])
        self.view.set_graph_mode_options([graph_mode.value for graph_mode in GraphModes])
        self.view.set_in_file_path(self.model.get_in_file_path())
        self.view.set_out_file_path(self.model.get_out_file_path())

        # Register listeners in the view
        self.view.add_in_file_browse_button_clicked_listener(self.in_file_browse_button_clicked)
        self.view.add_out_file_browse_button_clicked_listener(self.out_file_browse_button_clicked)
        self.view.add_open_file_button_clicked_listener(self.open_file_button_clicked)
        self.view.add_log_type_option_changed_listener(self.log_type_option_changed)
        self.view.add_file_read_option_changed_listener(self.file_read_option_changed)
        self.view.add_graph_mode_option_changed_listener(self.graph_mode_option_changed)

        # Register listenters in the model
        self.model.add_error_listener(self.error_event_listener)
        self.model.add_success_listener(self.success_event_listener)

    # Start the application
    def run(self):
        self.update_view()
        self.view.mainloop()

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
        # If we are in convert to CSV mode
        if self.model.get_file_parse_mode() == FileParseModes.CSV:
                if self.model.read_file_to_csv():
                    self.success_event_listener("Converted to csv successfully.")
        # Otherwise, if we are in generate graph mode
        elif self.model.get_file_parse_mode() == FileParseModes.GRAPH:
            # If we are in graph connections per hour mode
            if self.model.get_graph_mode() == GraphModes.CON_PER_HOUR:
                # self.success_event_listener(self.model.get_in_file_path())
                connections_list = self.model.parse_w3c_to_list(['time', 'c-ip'])
                if connections_list == None:
                    self.view.display_error_message("Connections list unable to be parsed, please make sure file is IIS format.")
                    return False
                # self.success_event_listener("File parsed to list")
                connections_per_hour_dict = self.model.get_connections_per_hour(connections_list)
                # self.success_event_listener("Connections per hour list created!")
                self.model.plot_connections(connections_per_hour_dict)
                # self.success_event_listener("Finished processing connections list")
            elif self.model.get_graph_mode() == GraphModes.SIMUL_CON:
                self.view.display_graph_view()

    # Function for displaying an error message in the view
    def error_event_listener(self, message):
        self.view.display_error_message(message)

    # Function for displaying a success message in the view
    def success_event_listener(self, message):
        self.view.display_success_message(message)

    # Function for updating the state of the view based on what has been set in the model
    def update_view(self):
        # Set the input and output file paths to those set in the model
        self.view.set_in_file_path(str(self.model.get_in_file_path()))
        self.view.set_out_file_path(str(self.model.get_out_file_path()))

        # If we are in convert to CSV mode
        if self.model.get_file_parse_mode() == FileParseModes.CSV:
            self.view.hide_graph_mode_option_menu_widgets()
            self.view.show_out_file_path_widgets()
            self.view.disable_open_file_button()
            if self.model.in_file_path_is_valid() and self.model.out_file_path_is_valid():
                self.view.enable_open_file_button()
        else:
            self.view.hide_out_file_path_widgets()
            self.view.show_graph_mode_option_menu_widgets()
            self.view.disable_open_file_button()
            if self.model.in_file_path_is_valid():
                self.view.enable_open_file_button()
