# Import the pathlib library for cross platform file path abstraction
import pathlib
# Import the re library to support regular expressions
import re

# Class definition for the file reader of the application
class AnaPyzerModel():
    # 'constant' for the accepted log file types
    ACCEPTED_LOG_TYPES = ['Apache (access.log)', 'IIS (u_ex*.log)']
    ACCEPTED_FILE_FORMATS = [('log files','*.log')]
    FILE_PARSE_MODES = ['Convert to csv', 'Generate graph', 'Count IPs']

    # Constructor
    def __init__(self):
        self.in_file_path = pathlib.Path.cwd()
        self.log_type = AnaPyzerModel.ACCEPTED_LOG_TYPES[0]
        self.file_parse_mode = AnaPyzerModel.FILE_PARSE_MODES[0]

    # Setter for the file path to the input file
    # Takes a string for the file path
    def set_file_path(self, in_file_path):
        # If the input file path was set, set the model's file path equal to it
        if in_file_path:
            self.in_file_path = in_file_path
        # Otherwise set the model's file path equal to the current working directory
        else:
            self.in_file_path = pathlib.Path.cwd()

    # Getter for the model's file path to the input file
    # Returns a string representing the file path
    def get_file_path(self):
        return self.in_file_path

    def set_log_type(self, log_type):
        self.log_type = log_type

    def get_log_type(self):
        return self.log_type

    def set_file_parse_mode(self, file_parse_mode):
        self.file_parse_mode = file_parse_mode

    def get_file_parse_mode(self):
        return self.file_parse_mode

    # Read the file
    def read_file(self):
        try:
            self.in_file = open(self.in_file_path, 'r')
        except:
            return None

        # Regex pattern for IPv4 addresses retrieved from https://www.regular-expressions.info/ip.html
        regex_IP_pattern = r'\b(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b'
        # Create the 'IP_address_counts' dictionary to count the IP addresses
        IP_address_counts = {}

        for line in self.in_file:
            matchObj = re.match(regex_IP_pattern, line, flags = 0)
            if matchObj:
                if IP_address_counts.get(matchObj.group()):
                    IP_address_counts[matchObj.group()] += 1
                else:
                    IP_address_counts[matchObj.group()] = 1

        self.in_file.close()

        output_string = ''

        for IP_address, count in IP_address_counts.items():
            output_string += '{} : {}\n'.format(IP_address, count)

        return output_string
