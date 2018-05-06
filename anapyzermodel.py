# Import the pathlib library for cross platform file path abstraction
import pathlib
# Import the re library to support regular expressions
import re

# Class definition for the file reader of the application
class AnaPyzerModel():

    # 'constant' for the accepted log file types
    ACCEPTED_LOG_TYPES = ['Apache (access.log)'] # TODO add 'IIS (u_ex*.log)' later
    ACCEPTED_FILE_FORMATS = [('log files','*.log')]
    FILE_PARSE_MODES = ['Convert to csv', 'Generate graph']
    GRAPH_MODES = ['Connections per minute', 'Simultaneous connections']
    OUTPUT_FILE_FORMATS = [('CSV (Comma delimited)','*.csv')]

    # Constructor
    def __init__(self):
        self.DEFAULT_FILE_PATH = pathlib.Path.home()
        self._in_file_path = pathlib.Path('')
        self._out_file_path = pathlib.Path('')
        self._log_type = AnaPyzerModel.ACCEPTED_LOG_TYPES[0]
        self._file_parse_mode = AnaPyzerModel.FILE_PARSE_MODES[0]

        self._error_listener = None

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
        if (in_file_path == '.'):
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
            if self._file_parse_mode == AnaPyzerModel.FILE_PARSE_MODES[0]: # CSV
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
        if (out_file_path == '.'):
            out_file_path = ''
        return out_file_path

    # Validation method that determines whether the output file path that is currently set in the model is valid
    def out_file_path_is_valid(self):
        is_valid = False

        out_file_path = pathlib.PurePath(self._out_file_path)
        out_file_path_parent = pathlib.Path(str(out_file_path.parent))

        if (self.get_out_file_path() != '' and out_file_path_parent.is_dir()):
            is_valid = True

        return is_valid

    # Setter for the type of input log file that will be read
    def set_log_type(self, log_type):
        self._log_type = log_type

    # Getter for the model's file type of the expected input log type
    # Returns a string representing the expected input log type
    def get_log_type(self):
        return self._log_type

    # Setter for how the input file will be parsed
    def set_file_parse_mode(self, file_parse_mode):
        self._file_parse_mode = file_parse_mode

    # Setter for how the input file will be parsed
    def get_file_parse_mode(self):
        return self._file_parse_mode

    # Read the input file that is currently set in the model.
    def read_file(self):
        try:
            in_file = open(self.in_file_path, 'r')
        except:
            return None

        # Regex pattern for IPv4 addresses retrieved from https://www.regular-expressions.info/ip.html
        regex_IP_pattern = r'\b(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b'
        # Create the 'IP_address_counts' dictionary to count the IP addresses
        IP_address_counts = {}

        for line in in_file:
            matchObj = re.match(regex_IP_pattern, line, flags = 0)
            if matchObj:
                if IP_address_counts.get(matchObj.group()):
                    IP_address_counts[matchObj.group()] += 1
                else:
                    IP_address_counts[matchObj.group()] = 1

        in_file.close()

        output_string = ''

        for IP_address, count in IP_address_counts.items():
            output_string += '{} : {}\n'.format(IP_address, count)

        return output_string

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

        return True

    def add_error_listener(self, listener):
        self._error_listener = listener

    def _on_error(self, error):
        if (self._error_listener):
            self._error_listener(error)