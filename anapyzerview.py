# Import the tkinter UI library
import tkinter
# Import the tkinter themed UI library
import tkinter.ttk
# Import the filedialog subclass to allow the user to graphically select a log file
import tkinter.filedialog
# Import the tkMessageBox subclass to allow showing system error messages
import tkinter.messagebox
# Import matplotlib to use it to generate graphs
import matplotlib
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Class definition for the View part of the MVC design pattern
# Extends the tkinter.ttk.Frame object
class AnaPyzerView(tkinter.ttk.Frame):
    # Class values for the default x-axis and y-axis padding
    WIDGET_X_PAD = 2
    WIDGET_Y_PAD = 2
    DEFAULT_ENTRY_WIDTH = 100

    def __init__(self, master=None):
        # Call the tkinter ttk Frame base class constructor
        tkinter.ttk.Frame.__init__(self, master)
        # Set the title of the window
        self.master.title("AnaPyzer")
        self.master.resizable(width=False, height=False)
        # Give the last two columns more weight so they expand when the window expands
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        # Set the geometry manager for the main window to use the grid layout
        self.grid()

        # Initialize view instance variables to update the view objects with
        self._log_type_choice = tkinter.StringVar()
        self._in_file_path = tkinter.StringVar()
        self._out_file_path = tkinter.StringVar()
        self._file_read_choice = tkinter.StringVar()
        self._graph_mode_choice = tkinter.StringVar()
        self._report_mode_choice = tkinter.StringVar()

        # Tell the view to create the widgets and populate the window with them
        self._create_widgets()

        # Initialize the listener method variable values
        self._log_type_option_changed = None
        self._in_file_browse_button_clicked = None
        self._file_read_option_changed = None
        self._graph_mode_option_changed = None
        self._report_mode_option_changed = None
        self._out_file_browse_button_clicked = None
        self._open_file_button_clicked = None

        # Initialize the graph view
        self.graph_view_window = None
        self.graph_view = None

    # Function for creating all the tkinter UI widgets in the window
    def _create_widgets(self):
        # Create a Label object to describe the purpose of the log_type_spinbox Spinbox object to the user
        self._log_type_option_menu_label = tkinter.ttk.Label(
            self,  # Make it a child of the main window object
            text='Choose log type', font=("arial", "12", "normal"))  # Set the label text & font
        self._log_type_option_menu_label.grid(
            row=0, column=0,  # Place the label in the UI grid,
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.W)  # Stick to the left of its cell

        # Create an OptionMenu object for the log type entry
        self._log_type_option_menu = tkinter.ttk.OptionMenu(
            self,  # Make it a child of the main window object
            self._log_type_choice,  # Watch the controller's variable
            None,  # Set the default value of the OptionMenu
            None,  # Set the other values of the OptionMenu
            command=self._on_log_type_option_changed)

        self._log_type_option_menu.grid(
            row=0, column=1,  # Place the OptionMenu in the UI grid
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.E + tkinter.W)  # Stick to the left

        # Create a Label object to describe the purpose of the in_file_path_field Entry object to the user
        self._in_file_path_field_label = tkinter.ttk.Label(
            self,  # Make it a child of the main window object
            text='Choose input file path', font=("arial", "12", "normal"))  # Set the label text & font
        self._in_file_path_field_label.grid(
            row=1, column=0,  # Place the Label in the UI grid,
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.W)  # Stick to the left of its cell

        # Create an Entry object for the file path entry
        self._in_file_path_field = tkinter.ttk.Entry(
            self,  # Make it a child of the main window object
            width=AnaPyzerView.DEFAULT_ENTRY_WIDTH,
            textvariable=self._in_file_path,  # Bind to the self._in_file_path variable for changes)
            state=tkinter.DISABLED)  # Disable the text field so that the user cannot enter arbitrary file paths
        self._in_file_path_field.grid(
            row=2, column=0,  # Place the entry in the UI grid
            columnspan=3,  # Span across multiple columns in the UI grid
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.E + tkinter.W)  # Stick to the left of its cell

        # Create a Button object to open a file dialog box to allow the user to choose a file
        self._in_file_browse_button = tkinter.ttk.Button(
            self,  # Make it a child of the main window object
            text='Browse...',  # Set the button text
            command=self._on_in_file_browse_button_clicked)
        self._in_file_browse_button.grid(
            row=2, column=3,  # Place the button in the UI grid
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.E)  # Stick to the right of its cell

        # Create a Label object to describe the purpose of the log_type_spinbox Spinbox object to the user
        self._file_read_option_menu_label = tkinter.ttk.Label(
            self,  # Make it a child of the main window object
            text='Choose file read mode', font=("arial", "12", "normal"))  # Set the label text & font
        self._file_read_option_menu_label.grid(
            row=3, column=0,  # Place the label in the UI grid,
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.W)  # Stick to the left of its cell

        # Create an OptionMenu object for the read option menu
        self._file_read_option_menu = tkinter.ttk.OptionMenu(
            self,  # Make it a child of the main window object
            self._file_read_choice,  # Watch the controller's variable
            None,  # Set the default value of the OptionMenu
            None,  # Set the other values of the OptionMenu
            command=self._on_file_read_option_changed)
        self._file_read_option_menu.grid(
            row=3, column=1,  # Place the Spinbox in the UI grid
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.E + tkinter.W)  # Stick to the left and right of its cell

        # Create a Label object to describe the purpose of the graph mode option menu to the user
        self._graph_mode_option_menu_label = tkinter.ttk.Label(
            self,  # Make it a child of the main window object
            text='Choose graph mode', font=("arial", "12", "normal"))  # Set the label text & font
        self._graph_mode_option_menu_label.grid(
            row=4, column=0,  # Place the label in the UI grid,
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.W)  # Stick to the left of its cell

        # Create an OptionMenu object for the read option menu
        self._graph_mode_option_menu = tkinter.ttk.OptionMenu(
            self,  # Make it a child of the main window object
            self._graph_mode_choice,  # Watch the controller's variable
            None,  # Set the default value of the OptionMenu
            None,  # Set the other values of the OptionMenu
            command=self._on_graph_mode_option_changed)
        self._graph_mode_option_menu.grid(
            row=4, column=1,  # Place the Spinbox in the UI grid
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.E + tkinter.W)  # Stick to the left and right of its cell

        # Create a Label object to describe the purpose of the out_file_path_field Entry object to the user
        self._out_file_path_field_label = tkinter.ttk.Label(
            self,  # Make it a child of the main window object
            text='Choose output file path', font=("arial", "12", "normal"))  # Set the label text & font
        self._out_file_path_field_label.grid(
            row=5, column=0,  # Place the Label in the UI grid,
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.W)  # Stick to the left of its cell

        # Create a Label object to describe the purpose of the report mode option menu to the user
        self._report_mode_option_menu_label = tkinter.ttk.Label(
            self,  # Make it a child of the main window object
            text='Choose report mode', font=("arial", "12", "normal"))  # Set the label text & font
        self._report_mode_option_menu_label.grid(
            row=4, column=0,  # Place the label in the UI grid,
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.W)  # Stick to the left of its cell

        # Create an OptionMenu object for the read option menu
        self._report_mode_option_menu = tkinter.ttk.OptionMenu(
            self,  # Make it a child of the main window object
            self._report_mode_choice,  # Watch the controller's variable
            None,  # Set the default value of the OptionMenu
            None,  # Set the other values of the OptionMenu
            command=self._on_report_mode_option_changed)
        self._report_mode_option_menu.grid(
            row=4, column=1,  # Place the Spinbox in the UI grid
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.E + tkinter.W)  # Stick to the left and right of its cell

        # Create a Label object to describe the purpose of the out_file_path_field Entry object to the user
        self._out_file_path_field_label = tkinter.ttk.Label(
            self,  # Make it a child of the main window object
            text='Choose output file path', font=("arial", "12", "normal"))  # Set the label text & font
        self._out_file_path_field_label.grid(
            row=5, column=0,  # Place the Label in the UI grid,
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.W)  # Stick to the left of its cell

        # Create an Entry object for the file path entry
        self._out_file_path_field = tkinter.ttk.Entry(
            self,  # Make it a child of the main window object
            width=AnaPyzerView.DEFAULT_ENTRY_WIDTH,
            textvariable=self._out_file_path,  # Bind to the self._out_file_path variable for changes
            state=tkinter.DISABLED)  # Disable the text field so that the user cannot enter arbitrary file paths
        self._out_file_path_field.grid(
            row=6, column=0,  # Place the entry in the UI grid
            columnspan=3,  # Span across multiple columns in the UI grid
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.E + tkinter.W)  # Stick to the left of its cell

        # Create a Button object to open a file dialog box to allow the user to choose a file
        self._out_file_browse_button = tkinter.ttk.Button(
            self,  # Make it a child of the main window object
            text='Browse...',  # Set the button text
            command=self._on_out_file_browse_button_clicked)
        self._out_file_browse_button.grid(
            row=6, column=3,  # Place the button in the UI grid
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
            sticky=tkinter.E)  # Stick to the right of its cell

        # Create a Button object to open the file specified in the file_path_field entry box
        self._open_file_button = tkinter.ttk.Button(
            self,  # Make it a child of the main window object
            text='Open',  # Set the button text
            command=self._on_open_file_button_clicked)
        self._open_file_button.grid(
            row=7, column=0,  # Place the button in the UI grid
            columnspan=4,  # Span across multiple columns in the UI grid
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD)  # Give it the global widget padding

    # Method to tell the view to display an error message
    # Takes a string for the message to be displayed
    @staticmethod
    def display_error_message(message):
        tkinter.messagebox.showerror("Error", message)

    # Method to tell the view to display a success message
    # Takes a string for the message to be displayed
    @staticmethod
    def display_success_message(message):
        tkinter.messagebox.showinfo("Success", message)

    # Method to create a new graph view from x and y plot data
    def display_graph_view(self, x_data, y_data, x_label, y_label, title):
        self.graph_view_window = tkinter.Toplevel(self)
        self.graph_view = AnaPyzerGraphView(self.graph_view_window)
        self.graph_view.configure_graph(x_data, y_data, x_label, y_label, title)

    # Method to tell the view to prompt the user to select a file
    # Takes a string for the starting directory,
    # and an array of tuples for the allowed file types
    # Returns a string with the selected file path
    def display_in_file_select_prompt(self, start_dir, file_formats):
        in_file_path = tkinter.filedialog.askopenfilename(
            parent=self,  # Make it a child of the main window object
            initialdir=start_dir,  # Start in the current working directory
            title='Select file',  # Set the title of the open file window
            filetypes=file_formats)  # Only allow certain files to be selected
        return in_file_path

    # Method to tell the view to prompt the user for a file save location
    # Takes a string for the starting directory,
    # and an array of tuples for the allowed file types
    # Returns a string with the file save location
    def display_out_file_select_prompt(self, start_dir, file_formats):
        out_file_path = tkinter.filedialog.asksaveasfilename(
            parent=self,  # Make it a child of the main window object
            initialdir=start_dir,  # Start in the current working directory
            title='Select file',  # Set the title of the open file window
            filetypes=file_formats)  # Only allow certain files to be selected
        return out_file_path

    # Method to set the log type options in the log type options menu
    def set_log_type_options(self, log_type_options):
        # Set new options
        self._log_type_option_menu.set_menu(log_type_options[0], *log_type_options)
        self._on_log_type_option_changed(log_type_options[0])

    # Method to set the file read mode options in the file read options menu
    def set_file_read_options(self, file_read_options):
        # Set new options
        self._file_read_option_menu.set_menu(file_read_options[0], *file_read_options)
        self._on_file_read_option_changed(file_read_options[0])

    # Method to set the graph options in the graph options menu
    def set_graph_mode_options(self, graph_mode_options):
        # Set new options
        self._graph_mode_option_menu.set_menu(graph_mode_options[0], *graph_mode_options)
        self._on_graph_mode_option_changed(graph_mode_options[0])

    # Method to set the graph options in the report options menu
    def set_report_mode_options(self, report_mode_options):
        # Set new options
        self._graph_mode_option_menu.set_menu(report_mode_options[0], *report_mode_options)
        self._on_graph_mode_option_changed(report_mode_options[0])

    # Method to set the in file path text
    def set_in_file_path(self, in_file_path):
        self.resize_entry_field(self._in_file_path_field, len(in_file_path))
        self._in_file_path.set(in_file_path)

    # Method to set the out file path text
    def set_out_file_path(self, out_file_path):
        self.resize_entry_field(self._out_file_path_field, len(out_file_path))
        self._out_file_path.set(out_file_path)

    @staticmethod
    def resize_entry_field(field, width):
        if width < AnaPyzerView.DEFAULT_ENTRY_WIDTH:
            field.config(width=AnaPyzerView.DEFAULT_ENTRY_WIDTH)
        else:
            field.config(width=width)

    # Method to enable the open file button to be clicked
    def enable_open_file_button(self):
        self._open_file_button.configure(state=tkinter.NORMAL)

    # Method to disable the open file button from being clicked
    def disable_open_file_button(self):
        self._open_file_button.configure(state=tkinter.DISABLED)

    # Method to show the graph options menu widgets
    def show_graph_mode_option_menu_widgets(self):
        self._graph_mode_option_menu_label.grid()
        self._graph_mode_option_menu.grid()

    # Method to hide the graph options menu widgets
    def hide_graph_mode_option_menu_widgets(self):
        self._graph_mode_option_menu_label.grid_remove()
        self._graph_mode_option_menu.grid_remove()

    # Method to show the output file path widgets
    def show_out_file_path_widgets(self):
        self._out_file_path_field_label.grid()
        self._out_file_path_field.grid()
        self._out_file_browse_button.grid()

    # Method to hide the output file path widgets
    def hide_out_file_path_widgets(self):
        self._out_file_path_field_label.grid_remove()
        self._out_file_path_field.grid_remove()
        self._out_file_browse_button.grid_remove()

    # Internal methods to call external listener methods
    # Needed because the TkInter UI widgets cannot have their 'command' redefined after being instantiated
    # So the widgets are instantiated pointing at these methods which will call the external listener methods
    def _on_log_type_option_changed(self, value):
        if self._log_type_option_changed:
            self._log_type_option_changed(value)

    def _on_in_file_browse_button_clicked(self):
        if self._in_file_browse_button_clicked:
            self._in_file_browse_button_clicked()

    def _on_file_read_option_changed(self, value):
        if self._file_read_option_changed:
            self._file_read_option_changed(value)

    def _on_graph_mode_option_changed(self, value):
        if self._graph_mode_option_changed:
            self._graph_mode_option_changed(value)

    def _on_report_mode_option_changed(self, value):
        if self._report_mode_option_changed:
            self._report_mode_option_changed(value)

    def _on_out_file_browse_button_clicked(self):
        if self._out_file_browse_button_clicked:
            self._out_file_browse_button_clicked()

    def _on_open_file_button_clicked(self):
        if self._open_file_button_clicked:
            self._open_file_button_clicked()

    # Methods to add listener methods for the internal listener methods to call outside of this class
    def add_log_type_option_changed_listener(self, listener):
        self._log_type_option_changed = listener

    def add_in_file_browse_button_clicked_listener(self, listener):
        self._in_file_browse_button_clicked = listener

    def add_file_read_option_changed_listener(self, listener):
        self._file_read_option_changed = listener

    def add_graph_mode_option_changed_listener(self, listener):
        self._graph_mode_option_changed = listener

    def add_report_mode_option_changed_listener(self, listener):
        self._report_mode_option_changed = listener

    def add_out_file_browse_button_clicked_listener(self, listener):
        self._out_file_browse_button_clicked = listener

    def add_open_file_button_clicked_listener(self, listener):
        self._open_file_button_clicked = listener


# Class definition for the Graph View child window class
# Extends the tkinter.ttk.Frame object
class AnaPyzerGraphView(tkinter.ttk.Frame):
    CANVAS_W, CANVAS_H = 300, 300

    def __init__(self, master=None):
        # Call the tkinter ttk Frame base class constructor
        tkinter.ttk.Frame.__init__(self, master)
        # Set the title of the window
        self.master.title("AnaPyzer Graph View")
        self.pack()

        # Create the figure
        self._figure = matplotlib.figure.Figure(figsize=(6, 6), dpi=100)
        self._axes = self._figure.add_axes([0.15, 0.15, .75, .75])
        self._canvas = FigureCanvasTkAgg(self._figure, self)
        self._canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.TRUE)

    def configure_graph(self, x_data, y_data, x_label, y_label, title):
        self._axes.plot(x_data, y_data)
        self._axes.set_xlabel(x_label)
        self._axes.set_ylabel(y_label)
        self._figure.legend(title=title)
        self._canvas.draw()
