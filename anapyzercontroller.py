# Import the AnaPyzerModel class
from anapyzermodel import *
# Import the AnaPyzerView class
from anapyzerview import *
# Import the pathlib library for cross platform file path abstraction
import pathlib

# Class definition for the Controller part of the MVC design pattern
class AnaPyzerController():
    # Constructor
    # Takes a view and a model object
    def __init__(self, view, model):
        # Set the controller's reference to the application view object
        self.view = view
        # Set the controller's reference to the application model object
        self.model = model

        # Set the available options for the view's options menu
        self.view.set_log_type_options(self.model.ACCEPTED_LOG_TYPES)
        self.view.set_file_read_options(self.model.FILE_PARSE_MODES)
        self.view.set_in_file_path(self.model.get_in_file_path())
        self.view.set_out_file_path(self.model.get_out_file_path())

        # Register listeners in the view before creating the widgets because the
        # widgets do not allow changing the callback method after they have been created
        self.view.add_browse_in_file_button_clicked_listener(self.browse_in_file_button_clicked)
        self.view.add_browse_out_file_button_clicked_listener(self.browse_out_file_button_clicked)
        self.view.add_open_file_button_clicked_listener(self.open_file_button_clicked)
        self.view.add_log_type_option_changed_listener(self.log_type_option_changed)
        self.view.add_file_read_option_changed_listener(self.file_read_option_changed)

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

    # Function for handling when the in file "Browse..." button is pressed
    def browse_in_file_button_clicked(self):
        # Get a new file path by prompting the user with a file selection dialog
        in_file_path = self.view.display_in_file_select_prompt(self.model.get_in_file_path(),
                                                               self.model.ACCEPTED_FILE_FORMATS)

        # Update the input file path to the one received from the user via the file dialog
        self.model.set_in_file_path(in_file_path)
        self.update_view()

    # Function for handling when the out file "Browse..." button is pressed
    def browse_out_file_button_clicked(self):
        # Get a new file path by prompting the user with a file selection dialog
        out_file_path = self.view.display_out_file_select_prompt(self.model.get_out_file_path(),
                                                                 self.model.OUTPUT_FILE_FORMATS)

        # Update the input file path to the one received from the user via the file dialog
        self.model.set_out_file_path(out_file_path)
        self.update_view()

    # Function for handling when the "Open" button is pressed
    def open_file_button_clicked(self):
        if (self.model.get_file_parse_mode() == self.model.FILE_PARSE_MODES[0]):
                try:
                    self.model.read_file_to_csv()
                    self.success_event_listener("Converted to csv successfully.")
                except AnaPyzerFileException as e:
                    if e.file_mode == 'r':
                        self.error_event_listener("Could not read from file: " + e.file)
                    elif e.file_mode == 'w':
                        self.error_event_listener("Could not write to file: " + e.file)
                    else:
                        self.error_event_listener("Unknown file I/O error.")
        
        self.update_view()

    # Function for displaying an error message in the view
    def error_event_listener(self, message):
        self.view.display_error_message(message)

    # Function for displaying a success message in the view
    def success_event_listener(self, message):
        self.view.display_success_message(message)

    def update_view(self):
        self.view.set_in_file_path(self.model.get_in_file_path())
        self.view.set_out_file_path(self.model.get_out_file_path())

        if (self.model.get_file_parse_mode() == AnaPyzerModel.FILE_PARSE_MODES[0]):
            self.view.show_out_file_path_widgets()
            self.view.disable_open_file_button()
            if (pathlib.Path(self.model.get_in_file_path()).is_file() and pathlib.Path(self.model.get_out_file_path()).is_file()):
                self.view.enable_open_file_button()
        else:
            self.view.hide_out_file_path_widgets()
            self.view.enable_open_file_button()

