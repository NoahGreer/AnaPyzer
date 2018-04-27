# Import the AnaPyzerModel class
import anapyzer_model
# Import the AnaPyzerView class
import anapyzer_view

# Import the tkinter UI library
import tkinter
# Import the tkinter themed UI library
import tkinter.ttk
# Import the filedialog subclass to allow the user to graphically select a log file
import tkinter.filedialog

# Import the pathlib library for cross platform file path abstraction
import pathlib

class AnaPyzerController():
    # Constructor
    def __init__(self):
        # Instantiate the tkinter application root object to attach the view to
        self.root = tkinter.Tk()
        # Instantiate the AnaPyzerModel object
        self.model = anapyzer_model.AnaPyzerModel(self)

        # Set in_file_path to a tkinter.StringVar() so that
        # the UI can watch for a change to the value
        self.log_type_option = tkinter.StringVar()
        self.log_type_option.set(self.model.ACCEPTED_LOG_TYPES[0])
        self.in_file_path = tkinter.StringVar()
        self.in_file_path.set(pathlib.Path.cwd())

        # Instantiate the AnaPyzerView object as child of the root
        self.view = anapyzer_view.AnaPyzerView(self.root, self)

        # Bind to the self.in_file_path variable for changes
        self.view.file_path_field.config(textvariable = self.in_file_path)

        # Register button left mouse click callbacks
        self.view.open_file_button.config(command = self.open_file_button_handler)
        self.view.browse_file_button.config(command = self.browse_file_button_handler)

    # Start the application
    def run(self):
        self.root.mainloop()


    # Function for handling when the "Browse..." button is pressed
    def browse_file_button_handler(self):
        # Get a new file path by prompting the user with a file selection dialog
        new_file_path = tkinter.filedialog.askopenfilename(parent = self.root, # Make it a child of the main window object
                                                           initialdir = pathlib.Path.cwd(), # Start in the current working directory
                                                           title = 'Select file', # Set the title of the open file window
                                                           filetypes = self.model.ACCEPTED_FILE_FORMATS) # Only allow certain files to be selected

        # Update the input file path to the one received from the user via the file dialog
        self.in_file_path.set(new_file_path)

    # Function for handling when the "Open" button is pressed
    def open_file_button_handler(self):
        # Set the file path in the model
        self.model.set_file_path(self.in_file_path.get())
        # Read the contents of the file
        file_contents = self.model.read_file()

        self.view.file_output_text.delete(1.0, tkinter.END)
        if file_contents:
            self.view.file_output_text.insert(tkinter.END, file_contents)

    def fileReadError(self, message):
        self.view.displayErrorMessage(message)

# Entry point
# If the application is being run directly, rather than from another script
if __name__ == '__main__':
    # Instantiate the main application controller object
    anapyzer = AnaPyzerController()
    # Run the main application
    anapyzer.run()
