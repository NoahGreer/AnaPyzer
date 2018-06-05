# Import the tkinter UI library
import tkinter
# Import the tkinter themed UI library
import tkinter.ttk
# Import the tkinter font library
import tkinter.font
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
    LABEL_WIDTH = 20
    DEFAULT_STICKY_DIRECTION = tkinter.W
    DEFAULT_FONT_SIZE = 12

    def __init__(self, master=None):
        # Call the tkinter ttk Frame base class constructor
        tkinter.ttk.Frame.__init__(self, master)

        # Configure the default font size
        default_font = tkinter.font.nametofont("TkDefaultFont")
        default_font.configure(size=AnaPyzerView.DEFAULT_FONT_SIZE)
        master.option_add("*Font", default_font)

        # Set the geometry manager for the main window to use the grid layout
        self.grid()

        # Tell the view to create the widgets and populate the window with them
        self._create_widgets()

    # Function for creating all the tkinter UI widgets in the window
    def _create_widgets(self):
        # Create the widgets for the log type menu
        self._log_type_menu_widgets = AnaPyzerView.OptionMenuWidgetGroup(
            'Choose log type',
            self)
        self._log_type_menu_widgets.grid(sticky=AnaPyzerView.DEFAULT_STICKY_DIRECTION)

        # Create the widgets for the input file path
        self._in_file_path_field_widgets = AnaPyzerView.FilePathWidgetGroup(
            'Choose input file path',
            'Browse...',
            self)
        self._in_file_path_field_widgets.grid(sticky=AnaPyzerView.DEFAULT_STICKY_DIRECTION)

        # Create the widgets for the file read options menu
        self._file_read_option_menu_widgets = AnaPyzerView.OptionMenuWidgetGroup(
            'Choose file read mode',
            self)
        self._file_read_option_menu_widgets.grid(sticky=AnaPyzerView.DEFAULT_STICKY_DIRECTION)

        # Create the widgets for the graph mode options menu
        self._graph_mode_option_menu_widgets = AnaPyzerView.OptionMenuWidgetGroup(
            'Choose graph mode',
            self)
        self._graph_mode_option_menu_widgets.grid(sticky=AnaPyzerView.DEFAULT_STICKY_DIRECTION)

        # Create the widgets for the report mode options menu
        self._report_mode_option_menu_widgets = AnaPyzerView.OptionMenuWidgetGroup(
            'Choose report mode',
            self)
        self._report_mode_option_menu_widgets.grid(sticky=AnaPyzerView.DEFAULT_STICKY_DIRECTION)

        # Create the widgets for the output file path
        self._out_file_path_field_widgets = AnaPyzerView.FilePathWidgetGroup(
            'Choose output file path',
            'Browse...',
            self)
        self._out_file_path_field_widgets.grid(sticky=AnaPyzerView.DEFAULT_STICKY_DIRECTION)
        # Create a Button object to open the file specified in the file_path_field entry box
        self._open_file_button = AnaPyzerView.Button(
            'Open',
            self)
        self._open_file_button.grid(
            padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
        )

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
        self._graph_view = AnaPyzerView.GraphView(self)
        self._graph_view.configure_graph(x_data, y_data, x_label, y_label, title)

    # Method to create a new graph view from x and y plot data
    def display_report_view(self, report_text):
        self._report_view = AnaPyzerView.ReportView(self)
        self._report_view.set_text(report_text)

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
        self._log_type_menu_widgets.set_menu(log_type_options)

    # Method to set the file read mode options in the file read options menu
    def set_file_read_options(self, file_read_options):
        # Set new options
        self._file_read_option_menu_widgets.set_menu(file_read_options)

    # Method to set the graph options in the graph options menu
    def set_graph_mode_options(self, graph_mode_options):
        # Set new options
        self._graph_mode_option_menu_widgets.set_menu(graph_mode_options)

    # Method to set the report options in the report options menu
    def set_report_mode_options(self, report_mode_options):
        # Set new options
        self._report_mode_option_menu_widgets.set_menu(report_mode_options)

    # Method to set the in file path text
    def set_in_file_path(self, in_file_path):
        self._in_file_path_field_widgets.set_path(in_file_path)

    # Method to set the out file path text
    def set_out_file_path(self, out_file_path):
        self._out_file_path_field_widgets.set_path(out_file_path)

    # Method to enable the open file button to be clicked
    def enable_open_file_button(self):
        self._open_file_button.enable()

    # Method to disable the open file button from being clicked
    def disable_open_file_button(self):
        self._open_file_button.disable()

    # Method to show the graph options menu widgets
    def show_graph_mode_option_menu_widgets(self):
        self._graph_mode_option_menu_widgets.grid()

    # Method to hide the graph options menu widgets
    def hide_graph_mode_option_menu_widgets(self):
        self._graph_mode_option_menu_widgets.grid_remove()

    # Method to show the report options menu widgets
    def show_report_mode_option_menu_widgets(self):
        self._report_mode_option_menu_widgets.grid()

    # Method to hide the report options menu widgets
    def hide_report_mode_option_menu_widgets(self):
        self._report_mode_option_menu_widgets.grid_remove()

    # Method to show the output file path widgets
    def show_out_file_path_widgets(self):
        self._out_file_path_field_widgets.grid()

    # Method to hide the output file path widgets
    def hide_out_file_path_widgets(self):
        self._out_file_path_field_widgets.grid_remove()

    # Methods to add listener methods for the internal listener methods to call outside of this class
    def set_log_type_option_changed_listener(self, listener):
        self._log_type_menu_widgets.set_menu_selection_changed_listener(listener)

    def set_in_file_browse_button_clicked_listener(self, listener):
        self._in_file_path_field_widgets.set_button_clicked_listener(listener)

    def set_file_read_option_changed_listener(self, listener):
        self._file_read_option_menu_widgets.set_menu_selection_changed_listener(listener)

    def set_graph_mode_option_changed_listener(self, listener):
        self._graph_mode_option_menu_widgets.set_menu_selection_changed_listener(listener)

    def set_report_mode_option_changed_listener(self, listener):
        self._report_mode_option_menu_widgets.set_menu_selection_changed_listener(listener)

    def set_out_file_browse_button_clicked_listener(self, listener):
        self._out_file_path_field_widgets.set_button_clicked_listener(listener)

    def set_open_file_button_clicked_listener(self, listener):
        self._open_file_button.set_on_button_clicked_action(listener)

    class OptionMenuWidgetGroup(tkinter.ttk.Frame):
        def __init__(self, label_text, master=None):
            tkinter.ttk.Frame.__init__(self, master)

            self._menu_selection = tkinter.StringVar()
            self._menu_selection_changed_action = None

            # Create a Label object to describe the purpose of the log_type_spinbox Spinbox object to the user
            self._label = tkinter.ttk.Label(
                self,  # Make it a child of this frame
                text=label_text,  # Set the label text
                width=AnaPyzerView.LABEL_WIDTH)
            self._label.pack(
                anchor=tkinter.W,
                padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
                side=tkinter.LEFT)

            # Create an OptionMenu object for the log type entry
            self._menu = tkinter.ttk.OptionMenu(
                self,  # Make it a child of this frame
                self._menu_selection,  # Watch the string variable
                None,  # Set the default value of the OptionMenu
                None,  # Set the other values of the OptionMenu
                command=self._on_menu_selection_changed_action)
            self._menu.pack(
                padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
                side=tkinter.LEFT)

        def _on_menu_selection_changed_action(self, value):
            if self._menu_selection_changed_action:
                self._menu_selection_changed_action(value)

        def set_menu_selection_changed_listener(self, action):
            self._menu_selection_changed_action = action

        def set_menu(self, menu_options):
            self._menu.set_menu(menu_options[0], *menu_options)
            self._on_menu_selection_changed_action(menu_options[0])

    class FilePathWidgetGroup(tkinter.ttk.Frame):
        def __init__(self, label_text, button_text, master=None):
            tkinter.ttk.Frame.__init__(self, master)

            self._file_path = tkinter.StringVar()
            self._button_clicked_action = None

            # Create a Label object to describe the purpose of the in_file_path_field Entry object to the user
            self._label = tkinter.ttk.Label(
                self,  # Make it a child of this frame
                text=label_text)  # Set the label text
            self._label.pack(
                anchor=tkinter.W,
                padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
                side=tkinter.TOP)

            # Create an Entry object for the file path entry
            self._entry = tkinter.ttk.Entry(
                self,  # Make it a child of this frame
                width=AnaPyzerView.DEFAULT_ENTRY_WIDTH,
                textvariable=self._file_path,  # Bind to the self._in_file_path variable for changes
                state=tkinter.DISABLED)  # Disable the text field so that the user cannot enter arbitrary file paths
            self._entry.pack(
                padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
                side=tkinter.LEFT)

            # Create a Button object to open a file dialog box to allow the user to choose a file
            self._button = tkinter.ttk.Button(
                self,  # Make it a child of this frame
                text=button_text,  # Set the button text
                command=self._on_button_clicked_action)
            self._button.pack(
                padx=AnaPyzerView.WIDGET_X_PAD, pady=AnaPyzerView.WIDGET_Y_PAD,  # Give it the global widget padding
                side=tkinter.LEFT)

        def _on_button_clicked_action(self):
            if self._button_clicked_action:
                self._button_clicked_action()

        def set_button_clicked_listener(self, action):
            self._button_clicked_action = action

        def set_path(self, path_text):
            self._file_path.set(path_text)
            self._entry.xview_moveto(1)

    class Button(tkinter.ttk.Button):
        def __init__(self, button_text, master=None):
            # Call the tkinter ttk Button base class constructor
            tkinter.ttk.Button.__init__(
                self,
                master,
                text=button_text,
                command=self._on_button_clicked_action)

            self._button_clicked_action = None

        def _on_button_clicked_action(self):
            if self._button_clicked_action:
                self._button_clicked_action()

        def set_on_button_clicked_action(self, action):
            self._button_clicked_action = action

        # Method to enable the button to be clicked
        def enable(self):
            self.configure(state=tkinter.NORMAL)

        # Method to disable the button from being clicked
        def disable(self):
            self.configure(state=tkinter.DISABLED)

    # Class definition for the Graph View child window class
    # Extends the tkinter.ttk.Frame object
    class GraphView(tkinter.Toplevel):
        CANVAS_W, CANVAS_H = 300, 300

        def __init__(self, master=None):
            # Call the tkinter ttk Toplevel base class constructor
            tkinter.Toplevel.__init__(self, master)

            # Set the title of the window
            self.title("AnaPyzer Graph View")

            # Create the figure
            self._figure = matplotlib.figure.Figure(figsize=(6, 6), dpi=100)
            self._axes = self._figure.add_axes([0.15, 0.15, 0.75, 0.75])
            self._canvas = FigureCanvasTkAgg(self._figure, self)
            self._canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.TRUE)

        def configure_graph(self, x_data, y_data, x_label, y_label, title):
            self._axes.plot(x_data, y_data)
            self._axes.set_xlabel(x_label)
            self._axes.set_ylabel(y_label)
            self._figure.legend(title=title)
            self._canvas.draw()

    # Class definition for the Report View child window class
    # Extends the tkinter.ttk.Frame object
    class ReportView(tkinter.Toplevel):
        def __init__(self, master=None):
            # Call the tkinter ttk Toplevel base class constructor
            tkinter.Toplevel.__init__(self, master)

            # Set the title of the window
            self.title("AnaPyzer Report View")

            # Create a ScrolledText object to open the file specified in the  entry box
            self._text_box = tkinter.Text(self) # Make it a child of the main window object
            self._text_box.pack(side=tkinter.LEFT)

            self._text_box_scrollbar = tkinter.ttk.Scrollbar(self, command=self._text_box.yview)
            self._text_box_scrollbar.pack(side=tkinter.LEFT, fill=tkinter.Y)
            self._text_box.config(yscrollcommand=self._text_box_scrollbar.set)

        def set_text(self, text):
            # Clear the text field
            self._text_box.delete(1.0, tkinter.END)
            # Insert the new text in the text field
            self._text_box.insert(tkinter.END, text)