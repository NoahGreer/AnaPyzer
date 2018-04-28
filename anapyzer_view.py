# Import the tkinter UI library
import tkinter
# Import the tkinter themed UI library
import tkinter.ttk
# Import the filedialog subclass to allow the user to graphically select a log file
import tkinter.filedialog
# Import the tkMessageBox subclass to allow showing system error messages
import tkinter.messagebox

# Class definition for the View part of the MVC design pattern
# Extends the tkinter.ttk.Frame object
class AnaPyzerView(tkinter.ttk.Frame):
    # Class values for the default x-axis and y-axis padding
    WIDGET_X_PAD = 2
    WIDGET_Y_PAD = 2

    def __init__(self, master = None):
        # Call the tkinter ttk Frame base class constructor
        tkinter.ttk.Frame.__init__(self, master)
        # Set the title of the window
        self.master.title("AnaPyzer")
        self.master.resizable(width=False, height=False)
        # Give column 0 more weight so that it uses more space than column 1
        self.grid_columnconfigure(0, # Configure column 0
                                  weight = 1) # Set the scaling weight to 1
        # Set the geometry manager for the main window to use the grid layout
        self.grid()

        # Initialize view instance variables to update the view objects with
        self._log_type_choice = tkinter.StringVar()
        self._in_file_path = tkinter.StringVar()
        self._file_read_choice = tkinter.StringVar()

        self._browse_file_button_listener = None
        self._open_file_button_listener = None
        self._log_type_option_menu_listener = None
        self._file_read_option_menu_listener = None

    # Function for creating all the tkinter UI widgets in the window
    def create_widgets(self):
        # Create a Label object to describe the purpose of the log_type_spinbox Spinbox object to the user
        self._log_type_option_menu_label = tkinter.ttk.Label(self, # Make it a child of the main window object
                                                            text = 'Choose log type') # Set the label text
        self._log_type_option_menu_label.grid(row = 0, column = 0, # Place the label in the UI grid,
                                              padx = AnaPyzerView.WIDGET_X_PAD, pady = AnaPyzerView.WIDGET_Y_PAD, # Give it the global widget padding
                                              sticky='W') # Stick to the left of its cell

        # Create an OptionMenu object for the log type entry
        self._log_type_option_menu = tkinter.ttk.OptionMenu(self, # Make it a child of the main window object
                                                            self._log_type_choice, # Watch the controller's variable
                                                            None, # Set the default value of the OptionMenu
                                                            None, # Set the other values of the OptionMenu
                                                            command = self._log_type_option_menu_listener)

        self._log_type_option_menu.grid(row = 1, column = 0, # Place the Spinbox in the UI grid
                                        columnspan = 3, # Span across two columns in the UI grid
                                        padx = AnaPyzerView.WIDGET_X_PAD, pady = AnaPyzerView.WIDGET_Y_PAD, # Give it the global widget padding
                                        sticky = 'E,W') # Stick to the left and right of its cell

        # Create a Label object to describe the purpose of the file_path_field Entry object to the user
        self._file_path_field_label = tkinter.ttk.Label(self, # Make it a child of the main window object
                                                       text = 'Choose file path') # Set the label text
        self._file_path_field_label.grid(row = 2, column = 0, # Place the Label in the UI grid,
                                         padx = AnaPyzerView.WIDGET_X_PAD, pady = AnaPyzerView.WIDGET_Y_PAD, # Give it the global widget padding
                                         sticky = 'W') # Stick to the left of its cell

        # Create an Entry object for the file path entry
        self._file_path_field = tkinter.ttk.Entry(self, # Make it a child of the main window object
                                                  textvariable = self._in_file_path) # Bind to the self._in_file_path variable for changes
        self._file_path_field.grid(row = 3, column = 0, # Place the entry in the UI grid
                                   padx = AnaPyzerView.WIDGET_X_PAD, pady = AnaPyzerView.WIDGET_Y_PAD, # Give it the global widget padding
                                   sticky = 'E,W') # Stick to the left of its cell

        # Create a Button object to open a file dialog box to allow the user to choose a file
        self._browse_file_button = tkinter.ttk.Button(self, # Make it a child of the main window object
                                                      text = 'Browse...', # Set the button text
                                                      command = self._browse_file_button_listener)
        self._browse_file_button.grid(row = 3, column = 1, # Place the button in the UI grid
                                      columnspan = 2, # Span across two columns in the UI grid
                                      padx = AnaPyzerView.WIDGET_X_PAD, pady = AnaPyzerView.WIDGET_Y_PAD, # Give it the global widget padding
                                      sticky = 'E') # Stick to the right of its cell


        # Create a Label object to describe the purpose of the log_type_spinbox Spinbox object to the user
        self._file_read_option_menu_label = tkinter.ttk.Label(self, # Make it a child of the main window object
                                                             text = 'Choose file read mode') # Set the label text
        self._file_read_option_menu_label.grid(row = 4, column = 0, # Place the label in the UI grid,
                                              padx = AnaPyzerView.WIDGET_X_PAD, pady = AnaPyzerView.WIDGET_Y_PAD, # Give it the global widget padding
                                              sticky='W') # Stick to the left of its cell

        # Create an OptionMenu object for the log type entry
        self._file_read_option_menu = tkinter.ttk.OptionMenu(self, # Make it a child of the main window object
                                                            self._file_read_choice, # Watch the controller's variable
                                                            None, # Set the default value of the OptionMenu
                                                            None, # Set the other values of the OptionMenu
                                                            command = self._file_read_option_menu_listener)

        self._file_read_option_menu.grid(row = 5, column = 0, # Place the Spinbox in the UI grid
                                        columnspan = 3, # Span across two columns in the UI grid
                                        padx = AnaPyzerView.WIDGET_X_PAD, pady = AnaPyzerView.WIDGET_Y_PAD, # Give it the global widget padding
                                        sticky = 'E,W') # Stick to the left and right of its cell

        # Create a Button object to open the file specified in the file_path_field entry box
        self._open_file_button = tkinter.ttk.Button(self, # Make it a child of the main window object
                                                   text = 'Open', # Set the button text
                                                   command = self._open_file_button_listener)
        self._open_file_button.grid(row = 6, column = 0, # Place the button in the UI grid
                                    columnspan = 3, # Span across two columns in the UI grid
                                    padx = AnaPyzerView.WIDGET_X_PAD, pady = AnaPyzerView.WIDGET_Y_PAD) # Give it the global widget padding

        # Create a ScrolledText object to open the file specified in the file_path_field entry box
        self._file_output_text = tkinter.Text(self) # Make it a child of the main window object
        #self._file_output_text.grid(row = 7, column = 0, # Place the ScrolledText in the UI grid
        #                            columnspan = 2) # Span across two columns in the UI grid

        # Create a Scrollbar object to control the text box
        self._file_output_text_scrollbar = tkinter.ttk.Scrollbar(self, # Make it a child of the main window object
                                                                command = self._file_output_text.yview) # Update the scroll position of the text box when the scroll bar is moved
        #self._file_output_text_scrollbar.grid(row = 7, column = 2, # Place the ScrolledText in the UI grid
        #                                      pady = AnaPyzerView.WIDGET_Y_PAD, # Give it the global widget padding
        #                                      sticky = 'N,W,S') # Stick to the top, left, and bottom of the cell
        self._file_output_text.config(yscrollcommand = self._file_output_text_scrollbar.set) # Update the scroll bar position when the text is scrolled

    # Method to tell the view to display an error message
    # Takes a string for the message to be displayed
    def display_error_message(self, message):
        tkinter.messagebox.showerror("Error", message)

    # Method to tell the view to prompt the user to select a file
    # Takes a string for the starting directory,
    # and an array of tuples for the allowed file types
    # Returns a string with the selected file path
    def display_file_select_prompt(self, start_dir, file_formats):
        selected_file_path = tkinter.filedialog.askopenfilename(parent = self, # Make it a child of the main window object
                                                                initialdir = start_dir, # Start in the current working directory
                                                                title = 'Select file', # Set the title of the open file window
                                                                filetypes = file_formats) # Only allow certain files to be selected

        return selected_file_path

    # Method to set the log types in the log type options menu
    def set_log_type_options(self, log_types):
        # Set new options
        self._log_type_option_menu.set_menu(log_types[0], *log_types)

    # Method to set the log types in the log type options menu
    def set_file_read_options(self, file_read_options):
        # Set new options
        self._file_read_option_menu.set_menu(file_read_options[0], *file_read_options)

    def set_file_path(self, file_path):
        self._in_file_path.set(file_path)

    def get_file_path(self):
        return self._in_file_path.get()

    def set_file_output_text(self, text):
        self._file_output_text.delete(1.0, tkinter.END)

        if text:
            self._file_output_text.insert(tkinter.END, text)

    def get_file_output_text(self):
        return self._file_output_text.get(1.0, tkinter.END)

    def add_log_type_option_menu_listener(self, listener):
        self._log_type_option_menu_listener = listener

    def add_browse_button_listener(self, listener):
        self._browse_file_button_listener = listener

    def add_file_read_option_menu_listener(self, listener):
        self._file_read_option_menu_listener = listener

    def add_open_file_button_listener(self, listener):
        self._open_file_button_listener = listener
