# Import the AnaPyzerModel class
from anapyzer_model import *
# Import the AnaPyzerView class
from anapyzer_view import *

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
        self.view.set_file_path(self.model.get_file_path())

        # Register listeners in the view before creating the widgets because the
        # widgets do not allow changing the callback method after they have been created
        self.view.add_browse_file_button_clicked_listener(self.browse_file_button_clicked)
        self.view.add_open_file_button_clicked_listener(self.open_file_button_clicked)
        self.view.add_log_type_option_changed_listener(self.log_type_option_changed)
        self.view.add_file_read_option_changed_listener(self.file_read_option_changed)

    # Start the application
    def run(self):
        self.view.mainloop()

    # Listener for when the log type option menu has an item selected
    def log_type_option_changed(self, value):
        self.model.set_log_type(value)

    # Handler for when the log type option menu has an item selected
    def file_read_option_changed(self, value):
        self.model.set_file_parse_mode(value)

    # Function for handling when the "Browse..." button is pressed
    def browse_file_button_clicked(self):
        # Get a new file path by prompting the user with a file selection dialog
        new_file_path = self.view.display_file_select_prompt(self.model.get_file_path(),
                                                             self.model.ACCEPTED_FILE_FORMATS)

        # Update the input file path to the one received from the user via the file dialog
        self.model.set_file_path(new_file_path)
        self.view.set_file_path(self.model.get_file_path())

    # Function for handling when the "Open" button is pressed
    def open_file_button_clicked(self):
        if (self.model.file_parse_mode == self.model.FILE_PARSE_MODES[0]):
                save_location = self.view.display_file_save_prompt(self.model.get_file_path(),
                                                                   self.model.OUTPUT_FILE_FORMATS)

                try:
                    self.model.read_file_to_csv(save_location)
                    self.success_event_listener("Converted to csv successfully. " + save_location)
                except AnaPyzerFileException as e:
                    if e.file_mode == 'r':
                        self.error_event_listener("Could not read from file: " + e.file)
                    elif e.file_mode == 'w':
                        self.error_event_listener("Could not write to file: " + e.file)
                    else:
                        self.error_event_listener("Unknown file I/O error.")

        # If the file was read sucessfully
        #if file_contents:
            # Update the view with the output
        #    self.view.set_file_output_text(file_contents)
        #else:
        #    self.error_event_listener('Could not open file ' + str(self.model.get_file_path()))

    # Function for displaying an error message in the view
    def error_event_listener(self, message):
        self.view.display_error_message(message)

    # Function for displaying a success message in the view
    def success_event_listener(self, message):
        self.view.display_success_message(message)
