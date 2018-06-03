# Import the enum class for better readability
import enum
# Import the pathlib library for cross platform file path abstraction
import pathlib

# Enumeration for the accepted log types
class AcceptedLogTypes(enum.Enum):
    APACHE = 'Apache (access.log)'
    IIS = 'IIS (u_ex*.log)'
    DEFAULT = APACHE


# Enumeration for the accepted file formats
class AcceptedFileFormats(enum.Enum):
    LOG = ('log files', '*.log')
    DEFAULT = LOG


# Enumeration for the output file formats
class OutputFileFormats(enum.Enum):
    CSV = ('CSV (Comma delimited)', '*.csv')
    DEFAULT = CSV


# Enumeration for the file parse modes
class FileParseModes(enum.Enum):
    GRAPH = 'Generate graph'
    REPORT = 'Generate report'
    CSV = 'Convert to csv'
    DEFAULT = GRAPH


# Enumeration for the graph output modes
class GraphModes(enum.Enum):
    CON_PER_HOUR = 'Connections per hour'
    IP_CONNECTIONS = 'Connections by Country'
    # CON_PER_MIN = 'Connections per minute'
    SIMUL_CON = 'Simultaneous connections'
    DEFAULT = CON_PER_HOUR


# Enumeration for the report output modes
class ReportModes(enum.Enum):
    URL_RPT = 'Website pages'
    SUSP_ACT = 'Suspicious activity report'
    DEFAULT = SUSP_ACT


class AnaPyzerModelError(Exception):
    def __init__(self, message):
        self.message = message


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
        self._report_mode = ReportModes.DEFAULT
        self._parsed_log_data = None
        self._graph_data = None
        self._report_data = None
        self._in_file_path_has_changed = False
        self._analyzer = analyzer
        self._parser = parser

    # Setter for the file path to the input file
    # Takes a string for the file path
    def set_in_file_path(self, in_file_path):
        # If the input file path was set, set the model's file path equal to it
        if in_file_path:
            new_in_file_path = pathlib.Path(in_file_path)
            if self._in_file_path != new_in_file_path:
                self._in_file_path = new_in_file_path
                self._in_file_path_has_changed = True
        # Otherwise set the model's file path equal to the default file path
        else:
            self._in_file_path = pathlib.Path(self.DEFAULT_FILE_PATH)
            self._in_file_path_has_changed = True

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
        # If the output file path was set, set the model's output file path equal to it
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

    # Setter for the type of report to generate
    def set_report_mode(self, report_mode):
        self._report_mode = ReportModes(report_mode)

    # Getter for the type of report to generate
    def get_report_mode(self):
        return self._report_mode

    # Reads from the input file, converts to csv, and writes to the output file
    def convert_file_to_csv(self):
        try:
            in_file = open(self._in_file_path, 'r')
        except IOError as e:
            raise AnaPyzerModelError("Could not read from file:\n" + e.filename + "\n" + e.strerror)

        try:
            out_file = open(self._out_file_path, 'w')
        except IOError as e:
            in_file.close()
            raise AnaPyzerModelError("Could not write to file:\n" + e.filename + "\n" + e.strerror)

        try:
            self._parser.convert_file_to_csv(in_file, out_file)
        except IOError as e:
            raise AnaPyzerModelError("Error encountered with file:\n" + e.filename + "\n" + e.strerror)
        finally:
            in_file.close()
            out_file.close()

        return True

    def create_report_data(self):
        self._parse_log_file_data()
        if self._report_mode == ReportModes.URL_RPT:
            pass
        elif self._report_mode == ReportModes.SUSP_ACT:
            self._report_data = self._analyzer.malicious_activity_report(self._parsed_log_data)
            print(self._report_data)

    def get_report_data(self):
        return self._report_data

    def export_report_data_to_file(self):
        try:
            out_file = open(self.get_out_file_path(), 'w')
        except IOError as e:
            raise AnaPyzerModelError("Could not write to " + e.filename + "\n" + e.strerror)
            out_file.close()
        self._parser.save_report_to_file(self._report_data, out_file)

    # get_parsed_log_file opens the current in_file and attempts to parse it, determining the log type
    # based on the current state of the UI
    def _parse_log_file_data(self):
        if self._in_file_path_has_changed or self._parsed_log_data is None:
            self._in_file_path_has_changed = False
            try:
                log_file = open(self.get_in_file_path(), 'r')
                if self._log_type == AcceptedLogTypes.IIS:
                    # print("parsing IIS")
                    try:
                        parsed_log = self._parser.parse_w3c_to_list(log_file)
                    except IndexError as e:
                        raise AnaPyzerModelError("Log file does not appear to be in IIS / W3C log format")
                elif self._log_type == AcceptedLogTypes.APACHE:
                    # print("parsing Apache")
                    try:
                        parsed_log = self._parser.parse_common_apache_to_list(log_file)
                    except IndexError as e:
                        raise AnaPyzerModelError("Log file does not appear to be in Apache / Common log format")
            except IOError as e:
                raise AnaPyzerModelError("Could not read from " + e.filename + "\n" + e.strerror)

            log_file.close()

            if parsed_log is not None:
                self._parsed_log_data = parsed_log
                return True
            else:
                raise AnaPyzerModelError("Log was unable to be parsed.")

    # create_graph_data attempts to extract graphable data from the current report_data dictionary
    def create_graph_data(self):
        self._parse_log_file_data()

        print(self.get_graph_mode())
        if self.get_graph_mode() == GraphModes.CON_PER_HOUR:
            print("Creating Connections Per Hour Report")
            graph_data = self._analyzer.get_connections_per_hour(self._parsed_log_data)

        elif self.get_graph_mode() == GraphModes.IP_CONNECTIONS:
            print("Creating IP Connections Report")
            graph_data = self._analyzer.ip_connection_report(self._parsed_log_data)

        if graph_data is not None:
            self._graph_data = graph_data

    # Print method for testing, outputs current delimited graph data to console
    def print_current_graph_data_split(self):
        for date in self._graph_data:
            print(self._graph_data[date])

    # Print method for testing, outputs current graph data to console
    def print_current_graph_data(self):
        print(self._graph_data)

    # Print method for testing, outputs current report data to console
    def print_current_report_data(self):
        print("printing _report_data")
        print(self._parsed_log_data)
        if self._parsed_log_data['length'] > 0:
            i = 0
            while i < self._parsed_log_data['length']:
                print(self._parsed_log_data[i])
                i+=1

    # Returns an array of the graph data dictionary's keys which contain
    # values that are also dictionaries or arrays.
    def get_graph_data_split(self):
        split = []
        for key in self._graph_data.keys():
            if isinstance(self._graph_data[key], dict):
                split.append(key)

        return split

    # Getter method for graph data keys,
    # used for data structures which contain a layer of abstraction
    # such as each data set being separated by date
    def get_graph_data_split_keys(self,date):
        if self._graph_data.get(date):
            return self._graph_data[date].keys()
        else:
            return None

    # Getter method for graph data values,
    # used for data structures which contain a layer of abstraction
    # such as each data set being separated by date
    def get_graph_data_split_values(self,date):
        if self._graph_data.get(date):
            return self._graph_data[date].values()
        else:
            return None

    # Getter method for graph keys
    # used for graphing of non-delimited data (not separated by date/time/etc)
    def get_graph_data_keys(self):
        return self._graph_data.keys()

    # Getter method for graph values
    # used for graphing of non-delimited data (not separated by date/time/etc)
    def get_graph_data_values(self):
        return self._graph_data.values()

    # Getter method for graph x label
    def get_graph_data_x_label(self):
        if 'xlabel' in self._graph_data.keys():
            return self._graph_data['xlabel']
        else:
            return 'X Axis'

    # Getter method for graph y label
    def get_graph_data_y_label(self):
        if 'ylabel' in self._graph_data.keys():
            return self._graph_data['ylabel']
        else:
            return 'Y Axis'

    # Getter method for graph title
    def get_graph_data_title(self):
        if self._graph_data.get('title'):
            return self._graph_data['title']
        else:
            return 'Title'