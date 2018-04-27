# Import the pathlib library for cross platform file path abstraction
import pathlib
# Import the re library to support regular expressions
import re

# Class definition for the file reader of the application
class AnaPyzerModel():
    # 'constant' for the accepted log file types
    ACCEPTED_LOG_TYPES = ['Apache (access.log)', 'IIS (u_ex*.log)']
    ACCEPTED_FILE_FORMATS = [('log files','*.log')]

    # Constructor
    def __init__(self, controller):
        self.controller = controller

    def set_file_path(self, in_file_path):
        self.in_file_path = in_file_path

    def read_file(self):
        try:
            self.in_file = open(self.in_file_path, 'r')
        except:
            self.controller.fileReadError('Could not open file ' + self.in_file_path)
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
