# Import the enum class for better readability
import enum
# Import the pathlib library for cross platform file path abstraction
import pathlib
# Import the re library to support regular expressions
import re

import matplotlib.pyplot


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
    def __init__(self):
        self.DEFAULT_FILE_PATH = pathlib.Path.home()
        self._in_file_path = pathlib.Path('')
        self._out_file_path = pathlib.Path('')
        self._log_type = AcceptedLogTypes.DEFAULT
        self._file_parse_mode = FileParseModes.DEFAULT
        self._graph_mode = GraphModes.DEFAULT

        self._error_listener = None
        self._success_listener = None

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

    # Internal methods to call external listener methods
    # Method to call when a file IO error occurs
    def _on_error(self, error):
        if self._error_listener:
            self._error_listener(error)

    # Method to call when a file was sucessfully read
    def _on_success(self, status_message):
        if self._success_listener:
            self._success_listener(status_message)

    # Methods to add listener methods for the internal listener methods to call outside of this class
    def add_error_listener(self, listener):
        self._error_listener = listener

    def add_success_listener(self, listener):
        self._error_listener = listener

    """
    parse_w3c_to_list will parse all information from an IIS/W3C format log into a list
    With the locations of each field denoted in the parsed_log['parameter'] field
    For instance, if c-ip is parsed into the 2 index of each line, requesting parsed_log['c-ip'] will return 2
    This also works in reverse, so if you need the c-ip from each line, you request parsed_log[parsed_log['c-ip']]
    For information on what each tag means refer to:
    https://stackify.com/how-to-interpret-iis-logs/
    """

    def parse_w3c_to_list(self):
        log_data = {}
        # open log file specified in file_name parameter
        o_file = open(self._in_file_path, 'r')
        # o_file = open('LWTech_auth.log')
        potential_parameters = ['date', 'time', 's-sitename', 's-computername', 's-ip', 'cs-method', 'cs-uri-stem',
                                'cs-uri-query', 's-port', 'cs-username', 'c-ip', 'cs(UserAgent)', 'cs(Cookie)',
                                'cs(Referrer)', 'cs-host', 'sc-status', 'sc-substatus', 'sc-win32-status', 'sc-bytes',
                                'cs-bytes', 'time-taken']

        # initialize placeholder variables in log_data array representing each of the w3c format parameters
        for parameter in potential_parameters:
            log_data[parameter] = -1

        # read the current line into a string variable called line
        line = o_file.readline()[:-1]

        i = 0
        # as long as there are lines in the file, loop:
        while line:
            # Split string into list of individual words with space as delimiter
            split_line = line.split(' ')

            # Every header line at the top of the log will start with a #, making it
            # easy to differentiate between data and the header
            if '#' in split_line[0]:
                log_data[str(split_line[0])] = split_line

                if '#Date' in split_line[0] and log_data['date'] == -1:
                    log_data['date'] = split_line[1]
                    # print("Date of record: " + log_data['date'])

                if '#Fields' in split_line[0]:
                    # Check the fields line for all available data being logged
                    j = 0
                    for element in split_line:
                        for parameter in potential_parameters:

                            if element == parameter:
                                log_data[parameter] = j - 1
                        j += 1
            else:
                print(split_line[log_data['c-ip']])
                log_data[i] = split_line
                i += 1

            line = o_file.readline()[:-1]
        # close the file once you're done getting all of the line information
        log_data['length'] = i
        o_file.close()
        # return the list containing CSV data
        return log_data


    """
    requested parameters list can consist of the following, using the official IIS naming convention found in header
    For information on what each tag means refer to:
    https://stackify.com/how-to-interpret-iis-logs/
    """
    def parse_w3c_fields_to_list(self, requested_parameters):
        log_data = {}
        # open log file specified in file_name parameter
        o_file = open(self._in_file_path, 'r')
        # o_file = open('LWTech_auth.log')
        potential_parameters = ['date', 'time', 's-sitename', 's-computername', 's-ip', 'cs-method', 'cs-uri-stem',
                                'cs-uri-query', 's-port', 'cs-username', 'c-ip', 'cs(UserAgent)', 'cs(Cookie)',
                                'cs(Referrer)', 'cs-host', 'sc-status', 'sc-substatus', 'sc-win32-status', 'sc-bytes',
                                'cs-bytes', 'time-taken']

        log_data['header'] = False
        # initialize placeholder variables in log_data array representing each of the w3c format parameters
        for parameter in potential_parameters:
            log_data[parameter] = -1

        # read the current line into a string variable called line
        line = o_file.readline()[:-1]

        i = 0
        # as long as there are lines in the file, loop:
        while line:
            # Split string into list of individual words with space as delimiter
            split_line = line.split(' ')

            # Every header line at the top of the log will start with a #, making it
            # easy to differentiate between data and the header
            if '#' in split_line[0]:
                log_data[str(split_line[0])] = split_line
                log_data['header'] = True
                if '#Date' in split_line[0] and log_data['date'] == -1:
                    log_data['date'] = split_line[1]
                    # print("Date of record: " + log_data['date'])

                if '#Fields' in split_line[0]:
                    # Check the fields line for all available data being logged
                    # j keeps count of the placement of each parameter in the split line
                    j = 0
                    for element in split_line:
                        # iterate through list of potential parameters
                        for parameter in potential_parameters:
                            # mark the location of each parameter present in relation to the list to be created
                            if element == parameter:
                                log_data[parameter] = j
                                j += 1
            else:
                if log_data['header'] == False:
                    return None

                # initialize log_data[i] as a blank list to allow for use of append method
                log_data[i] = []

                # iterate through array of requested_parameters and add the information requested to the parsed list
                for parameter in requested_parameters:
                    if log_data.get(parameter):
                        log_data[i].append(split_line[log_data[parameter]])
                    else:
                        # print("Requested parameter "+ parameter + " not found")
                        pass

                i += 1
            # read next line
            line = o_file.readline()[:-1]

        # once log file is parsed, assign the new positions of each requested parameter in the log_data list to
        # prevent issues when using methods that rely on tagged element values representing element placement in array
        k = 0
        for parameter in requested_parameters:
            log_data[parameter] = k
            k += 1
        # length represents the number of lines of DATA present in returned parsed list
        log_data['length'] = i
        # close the file once you're done getting all of the line information
        o_file.close()
        # return the list containing w3c data
        return log_data

    # get_connections_per_hour takes in a log parsed by the above parse_w3c_tolist method
    # and returns a list containing how many unique ip connections were present during each hour of the day
    # this parsed list can be used with the plot_hourly_connections method
    def get_connections_per_hour(self, parsed_log):
        connections_per_hour_table = {}

        if parsed_log == None:
            return None

        time_place = parsed_log['time']
        cip_place = parsed_log['c-ip']

        i = 0
        while i < parsed_log['length']:
            # iterate through the ip addresses recorded
            time_string = parsed_log[i][time_place]
            user_ip_address = parsed_log[i][cip_place]

            time_string = str(time_string)
            user_ip_address = str(user_ip_address)
            # print("Time string = " + time_string)
            # print("IP address = "+ user_ip_address)
            hours = time_string[:2]

            i += 1
            if connections_per_hour_table.get(hours):
                connections_per_hour_table[hours] += [user_ip_address]
            else:
                connections_per_hour_table[hours] = [user_ip_address]

        for time in connections_per_hour_table:
            ip_count = len(set(connections_per_hour_table[time]))
            connections_per_hour_table[time] = ip_count

        # print("connections per hour report complete")
        # for time in connections_per_hour_table:
        #     print(str(connections_per_hour_table[time]) + " unique connections at "+ time)
        return connections_per_hour_table

    # The plot_connections method take a log formatted by the get_connections_per_hour method
    def announce_connections(self, connections_log):
        for log in connections_log:
            print(str(connections_log[log]) + " unique connections found at " + log + ":00")

    # The plot_connections method will take in a log formatted by the above method
    def plot_connections(self, connections_log):
        if connections_log != None:
            matplotlib.pyplot.figure()
            matplotlib.pyplot.xlabel("Hour of Day")
            matplotlib.pyplot.ylabel("Unique IPs Accessing")
            # plt.legend(title=str(connections_log[0][0]))
            # plot the data in a very ugly chart (figure out how to beautify)

            matplotlib.pyplot.plot(connections_log.keys(), connections_log.values())
            report_string = ''

            for line in connections_log:
                report_string += str(connections_log[line]) + " unique connections at " + line + ":00 \n"

            # show the newly created data plot.
            matplotlib.pyplot.show()
