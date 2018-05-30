# Import the enum class for better readability
import enum
# Import the pathlib library for cross platform file path abstraction
import pathlib
# Import the re library to support regular expressions
import re
#from anapyzeranalyzer import AnaPyzerAnalyzer

#analyzer = AnaPyzerAnalyzer()
# Enumeration for the accepted log types
class AcceptedLogTypes(enum.Enum):
    APACHE = 'Apache (access.log)'
    IIS = 'IIS (u_ex*.log)'
    DEFAULT = APACHE


class AcceptedFileFormats(enum.Enum):
    LOG = ('log files', '*.log')
    DEFAULT = LOG


class FileParseModes(enum.Enum):
    GRAPH = 'Generate graph'
    CSV = 'Convert to csv'
    REPORT = "Generate Report"
    DEFAULT = GRAPH


class GraphModes(enum.Enum):
    CON_PER_HOUR = 'Connections per hour'
    # CON_PER_MIN = 'Connections per minute'
    SIMUL_CON = 'Simultaneous connections'
    DEFAULT = CON_PER_HOUR


class OutputFileFormats(enum.Enum):
    CSV = ('CSV (Comma delimited)', '*.csv')
    DEFAULT = CSV


# Class definition for the file reader of the application
class AnaPyzerModel:

    # Constructor
    def __init__(self, parser, analyzer):
        self.DEFAULT_FILE_PATH = pathlib.Path.home()
        self._in_file_path = pathlib.Path('')
        self._out_file_path = pathlib.Path('')
        self._log_type = AcceptedLogTypes.DEFAULT
        self._file_parse_mode = FileParseModes.DEFAULT
        self._graph_mode = GraphModes.DEFAULT
        self._error_listener = None
        self._success_listener = None
        self.analyzer = analyzer
        self.parser = parser

    # Setter for the file path to the input file
    # Takes a string for the file path
    def set_in_file_path(self, in_file_path):
        # If the input file path was set, set the model's file path equal to it
        if in_file_path:
            self._in_file_path = pathlib.Path(in_file_path)
        # Otherwise set the model's file path equal to the default file path
        else:
            self._in_file_path = pathlib.Path(self.DEFAULT_FILE_PATH)

    # Getter for the model's file path to the input file
    # Returns a string representing the file path
    def get_in_file_path(self):
        in_file_path = str(self._in_file_path)
        if in_file_path == '.':
            in_file_path = ''
        return in_file_path

    # Validation method that determines whether the input file path that is currently set in the model is valid
    def in_file_path_is_valid(self):
        return pathlib.Path(self._in_file_path).is_file()

    # Setter for the file path to the input file
    # Takes a string for the file path
    def set_out_file_path(self, out_file_path):
        # If the input file path was set, set the model's file path equal to it
        if out_file_path:
            # If we are in convert to CSV mode
            if self._file_parse_mode == FileParseModes.CSV:
                # Get the suffix of the output file
                out_file_suffix = str(pathlib.PurePath(out_file_path).suffix)
                # If it is not '.csv'
                if out_file_suffix != '.csv':
                    # Change the suffix to '.csv'
                    out_file_path = str(pathlib.PurePath(out_file_path).with_suffix('.csv'))
            # Set the model's out file path to the out file path
            self._out_file_path = pathlib.Path(out_file_path)
        # Otherwise set the model's file path equal to the current working directory
        else:
            self._out_file_path = pathlib.Path(self.DEFAULT_FILE_PATH)

    # Getter for the model's file path to the input file
    # Returns a string representing the file path
    def get_out_file_path(self):
        out_file_path = str(self._out_file_path)
        if out_file_path == '.':
            out_file_path = ''
        return out_file_path

    # Validation method that determines whether the output file path that is currently set in the model is valid
    def out_file_path_is_valid(self):
        is_valid = False

        out_file_path = pathlib.PurePath(self._out_file_path)
        out_file_path_parent = pathlib.Path(str(out_file_path.parent))

        if self.get_out_file_path() != '' and out_file_path_parent.is_dir():
            is_valid = True

        return is_valid

    # Setter for the type of input log file that will be read
    def set_log_type(self, log_type):
        self._log_type = AcceptedLogTypes(log_type)

    # Getter for the model's file type for the expected input log type
    # Returns a string representing the expected input log type
    def get_log_type(self):
        return self._log_type

    # Setter for how the input file will be parsed
    def set_file_parse_mode(self, file_parse_mode):
        self._file_parse_mode = FileParseModes(file_parse_mode)

    # Getter for how the input file will be parsed
    def get_file_parse_mode(self):
        return self._file_parse_mode

    # Setter for the type of graph to generate
    def set_graph_mode(self, graph_mode):
        self._graph_mode = GraphModes(graph_mode)

    # Getter for the type of graph to generate
    def get_graph_mode(self):
        return self._graph_mode

    # Reads from the input file, converts to csv, and writes to the output file
    def read_file_to_csv(self):
        try:
            in_file = open(self._in_file_path, 'r')
        except IOError as e:
            self._on_error("Could not read from file:\n" + e.filename + "\n" + e.strerror)
            return False

        try:
            out_file = open(self._out_file_path, 'w')
        except IOError as e:
            in_file.close()
            self._on_error("Could not write to file:\n" + e.filename + "\n" + e.strerror)
            return False

        for line in in_file:
            converted_line = re.sub("\s+", ",", line.strip())
            out_file.write(converted_line + '\n')

        in_file.close()
        out_file.close()

        self._on_success("Successfully converted log file to csv")
        return True

    def read_file_to_report(self):
        try:
            in_file = open(self._in_file_path, 'r')
        except IOError as e:
            self._on_error("Could not read from file:\n" + e.filename + "\n" + e.strerror)
            return False

        try:
            out_file = open(self._out_file_path, 'w')
        except IOError as e:
            in_file.close()
            self._on_error("Could not write to file:\n" + e.filename + "\n" + e.strerror)
            return False
        if self.get_log_type() == AcceptedLogTypes.APACHE:
            parsed_log = self.analyzer.parse_apache(self._in_file_path)
        elif self.get_log_type() == AcceptedLogTypes.IIS:
            pass
        for key in parsed_log:
            if self.analyzer.is_malicious(parsed_log[key][2], parsed_log[key][4]):
                out_file.write("Malicious activity detected from " + key + "\n\n")

        in_file.close()
        out_file.close()
        self._on_success("Report generated successfully")
        return True

    # Internal methods to call external listener methods
    # Method to call when a file IO error occurs
    def _on_error(self, error):
        if self._error_listener:
            self._error_listener(error)

    # Method to call when a file was successfully read
    def _on_success(self, status_message):
        if self._success_listener:
            self._success_listener(status_message)

    # Methods to add listener methods for the internal listener methods to call outside of this class
    def add_error_listener(self, listener):
        self._error_listener = listener

    def add_success_listener(self, listener):
        self._error_listener = listener
