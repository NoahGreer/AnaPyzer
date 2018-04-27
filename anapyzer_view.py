# Import the tkinter UI library
import tkinter
# Import the tkinter themed UI library
import tkinter.ttk
# Import the filedialog subclass to allow the user to graphically select a log file
import tkinter.filedialog
# Import the tkMessageBox subclass to allow showing system error messages
import tkinter.messagebox

# Global 'constants' for the default x-axis and y-axis padding
WIDGET_X_PAD = 2
WIDGET_Y_PAD = 2

# Class definition for the UI class of the application
class AnaPyzerView():
    def __init__(self, master, controller):
        self.controller = controller
        self.frame = tkinter.ttk.Frame(master)
        master.title("AnaPyzer")
        master.resizable(width=False, height=False)
        # Give column 0 more weight so that it uses more space than column 1
        self.frame.grid_columnconfigure(0, # Configure column 0
                                         weight = 1) # Set the scaling weight to 1
        # Set the padding for the main application window
        self.frame.grid()
        self.createWidgets()

    # Function for creating all the tkinter UI widgets in the window
    def createWidgets(self):
        # Create a Label object to describe the purpose of the log_type_spinbox Spinbox object to the user
        self.log_type_spinbox_label = tkinter.ttk.Label(self.frame, # Make it a child of the main window object
                                                        text = 'Log type:') # Set the label text
        self.log_type_spinbox_label.grid(row = 0, column = 0, # Place the label in the UI grid,
                                         padx = WIDGET_X_PAD, pady = WIDGET_Y_PAD, # Give it the global widget padding
                                         sticky='W') # Stick to the left of its cell

        # Create an OptionMenu object for the log type entry
        self.log_type_option_menu = tkinter.ttk.OptionMenu(self.frame, # Make it a child of the main window object
                                                           self.controller.log_type_option, # Watch the controller's variable
                                                           self.controller.model.ACCEPTED_LOG_TYPES[0], # Set the default value of the OptionMenu
                                                           *self.controller.model.ACCEPTED_LOG_TYPES) # Set the other values of the OptionMenu

        self.log_type_option_menu.grid(row = 1, column = 0, # Place the Spinbox in the UI grid
                                       columnspan = 2, # Span across two columns in the UI grid
                                       padx = WIDGET_X_PAD, pady = WIDGET_Y_PAD, # Give it the global widget padding
                                       sticky = 'E,W') # Stick to the left and right of its cell

        # Create a Label object to describe the purpose of the file_path_field Entry object to the user
        self.file_path_field_label = tkinter.ttk.Label(self.frame, # Make it a child of the main window object
                                                       text = 'File path:') # Set the label text
        self.file_path_field_label.grid(row = 2, column = 0, # Place the Label in the UI grid,
                                        padx = WIDGET_X_PAD, pady = WIDGET_Y_PAD, # Give it the global widget padding
                                        sticky = 'W') # Stick to the left of its cell

        # Create an Entry object for the file path entry
        self.file_path_field = tkinter.ttk.Entry(self.frame) # Make it a child of the main window object
        self.file_path_field.grid(row = 3, column = 0, # Place the entry in the UI grid
                                  padx = WIDGET_X_PAD, pady = WIDGET_Y_PAD, # Give it the global widget padding
                                  sticky = 'E,W') # Stick to the left of its cell

        # Create a Button object to open a file dialog box to allow the user to choose a file
        self.browse_file_button = tkinter.ttk.Button(self.frame, # Make it a child of the main window object
                                                     text = 'Browse...') # Set the button text
        self.browse_file_button.grid(row = 3, column = 1, # Place the button in the UI grid
                                     padx = WIDGET_X_PAD, pady = WIDGET_Y_PAD, # Give it the global widget padding
                                     sticky = 'E') # Stick to the right of its cell

        # Create a Button object to open the file specified in the file_path_field entry box
        self.open_file_button = tkinter.ttk.Button(self.frame, # Make it a child of the main window object
                                                   text = 'Open') # Set the button text
        self.open_file_button.grid(row = 4, column = 0, # Place the button in the UI grid
                                   columnspan = 2, # Span across two columns in the UI grid
                                   padx = WIDGET_X_PAD, pady = WIDGET_Y_PAD) # Give it the global widget padding

        # Create a ScrolledText object to open the file specified in the file_path_field entry box
        self.file_output_text = tkinter.Text(self.frame) # Make it a child of the main window object
        self.file_output_text.grid(row = 5, column = 0, # Place the ScrolledText in the UI grid
                                   columnspan = 2) # Span across two columns in the UI grid

        # Create a Scrollbar object to control the text box
        self.file_output_text_scrollbar = tkinter.ttk.Scrollbar(self.frame, # Make it a child of the main window object
                                                                command = self.file_output_text.yview) # Update the scroll position of the text box when the scroll bar is moved
        self.file_output_text_scrollbar.grid(row = 5, column = 2, # Place the ScrolledText in the UI grid
                                             pady = WIDGET_Y_PAD, # Give it the global widget padding
                                             sticky = 'N,W,S') # Stick to the top, left, and bottom of the cell
        self.file_output_text.config(yscrollcommand = self.file_output_text_scrollbar.set) # Update the scroll bar position when the text is scrolled

    def displayErrorMessage(self, message):
        tkinter.messagebox.showerror("Error", message)
