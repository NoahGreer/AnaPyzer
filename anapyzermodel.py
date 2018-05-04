# Import the pathlib library for cross platform file path abstraction
import pathlib
# Import the re library to support regular expressions
import re

class AnaPyzerModelException(Exception): pass

class AnaPyzerFileException(AnaPyzerModelException):
    def __init__(self, file=None, file_mode=None, *args, **kwargs):
        self.file = file
        self.file_mode = file_mode

    def __repr__(self):
        return u"AnaPyzerFileException(file={0!r}, file_mode={1!r})".format(self.file, self.file_mode)

    __str__ = __repr__

# Class definition for the file reader of the application
class AnaPyzerModel():

    # 'constant' for the accepted log file types
    ACCEPTED_LOG_TYPES = ['Apache (access.log)', 'IIS (u_ex*.log)']
    ACCEPTED_FILE_FORMATS = [('log files','*.log')]
    FILE_PARSE_MODES = ['Convert to csv', 'Generate graph', 'Count IPs']
    OUTPUT_FILE_FORMATS = [('CSV (Comma delimited)','*.csv')]

    # Constructor
    def __init__(self):
        self.DEFAULT_FILE_PATH = pathlib.Path.home()
        self._in_file_path = pathlib.Path('')
        self._out_file_path = pathlib.Path('')
        self._log_type = AnaPyzerModel.ACCEPTED_LOG_TYPES[0]
        self._file_parse_mode = AnaPyzerModel.FILE_PARSE_MODES[0]

    # Setter for the file path to the input file
    # Takes a string for the file path
    def set_in_file_path(self, in_file_path):
        # If the input file path was set, set the model's file path equal to it
        if in_file_path:
            self._in_file_path = pathlib.Path(in_file_path)
        # Otherwise set the model's file path equal to the current working directory
        else:
            self._in_file_path = pathlib.Path(self.DEFAULT_FILE_PATH)

    # Getter for the model's file path to the input file
    # Returns a string representing the file path
    def get_in_file_path(self):
        in_file_path = str(self._in_file_path)
        if (in_file_path == '.'):
            in_file_path = ''
        return in_file_path

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

    def out_file_path_is_valid(self):
        is_valid = False

        out_file_path = pathlib.PurePath(self._out_file_path)
        out_file_path_parent = pathlib.Path(str(out_file_path.parent))

        if (self.get_out_file_path() != '' and out_file_path_parent.is_dir()):
            is_valid = True

        return is_valid

    def set_log_type(self, log_type):
        self._log_type = log_type

    # Getter for the model's file type of the expected input log type
    # Returns a string representing the expected input log type
    def get_log_type(self):
        return self._log_type

    def set_file_parse_mode(self, file_parse_mode):
        self._file_parse_mode = file_parse_mode

    def get_file_parse_mode(self):
        return self._file_parse_mode

    # Read the file
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
        except:
            raise AnaPyzerFileException(file = self._in_file_path, file_mode = 'r')

        try:
            out_file = open(self._out_file_path, 'w')
        except:
            in_file.close()
            raise AnaPyzerFileException(file = self._out_file_path, file_mode = 'w')

        for line in in_file:
            converted_line = re.sub("\s+", ",", line.strip())
            out_file.write(converted_line + '\n')

        in_file.close()
        out_file.close()

        return True
