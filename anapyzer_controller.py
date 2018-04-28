# Class definition for the Controller part of the MVC design pattern
class AnaPyzerController():
    # Constructor
    # Takes a view and a model object
    def __init__(self, view, model):
        # Set the controller's reference to the application view object
        self.view = view
        # Set the controller's reference to the application model object
        self.model = model

        # Register listeners
        self.view.add_browse_button_listener(self.browse_file_button_handler)
        self.view.add_open_file_button_listener(self.open_file_button_handler)
        self.view.add_log_type_option_menu_listener(self.log_type_option_menu_handler)
        self.view.add_file_read_option_menu_listener(self.file_read_option_menu_handler)

        self.view.create_widgets()

        # Set the available options for the view's options menu
        self.view.set_log_type_options(self.model.ACCEPTED_LOG_TYPES)
        self.view.set_file_read_options(self.model.FILE_PARSE_MODES)
        self.view.set_file_path(self.model.get_file_path())

    # Start the application
    def run(self):
        self.view.mainloop()

    # Handler for when the log type option menu has an item selected
    def log_type_option_menu_handler(self, value):
        self.model.set_log_type(value)

    # Handler for when the log type option menu has an item selected
    def file_read_option_menu_handler(self, value):
        self.model.set_file_parse_mode(value)

    # Function for handling when the "Browse..." button is pressed
    def browse_file_button_handler(self):
        # Get a new file path by prompting the user with a file selection dialog
        new_file_path = self.view.display_file_select_prompt(self.model.get_file_path(),
                                                             self.model.ACCEPTED_FILE_FORMATS)

        # Update the input file path to the one received from the user via the file dialog
        self.model.set_file_path(new_file_path)
        self.view.set_file_path(self.model.get_file_path())

    # Function for handling when the "Open" button is pressed
    def open_file_button_handler(self):
        # Read the contents of the file
        file_contents = self.model.read_file()

        if file_contents:
            self.view.set_file_output_text(file_contents)
        else:
            self.file_read_error('Could not open file ' + str(self.model.get_file_path()))
            
    def file_read_error(self, message):
        self.view.display_error_message(message)
