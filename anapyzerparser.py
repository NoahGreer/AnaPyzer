# Import the pathlib library for cross platform file path abstraction
import pathlib

# The AnaPyzerParser class contains all methods involved in parsing information from a text or log file.


class AnaPyzerParser:

    # Constructor
    def __init__(self):
        self.DEFAULT_FILE_PATH = pathlib.Path.home()
        self._in_file_path = pathlib.Path('')
        self._error_listener = None
        self._success_listener = None

    # parse_common_apache_to_list() parses an apache log that has been exported in the common, default format by an
    #  apache web server. This method is in need of additional work that will make it functional with logs
    # that have custom configurations
    # Reference for Common Log Format:
    # https://httpd.apache.org/docs/1.3/logs.html#common

    @staticmethod
    def parse_common_apache_to_list(in_file):
        if not in_file:
            return None
        log_data = {}

        # universal_names = ['date', 'timestamp', 'service-name', 'server-name', 'server-ip', 'method', 'uri-stem',
        #                   'uri-query', 'server-port', 'username', 'client-ip', 'user-agent', 'cookie',
        #                   'referrer', 'host', 'http-status', 'protocol-substatus', 'win32-status', 'bytes-sent',
        #                   'bytes-received', 'time-taken'] - Dan unused variable

        # initialize placeholder variables in log_data array representing each of the w3c format parameters

        i = 0
        # as long as there are lines in the log
        # Split string into list of individual words with space as delimiter lines in the file, loop:
        for line in in_file:
            # Use split to cut date/timestamp combined line out of data line
            date_ts = line.split('[', 1)
            # Use split to separate date and timestamp
            date_ts = date_ts[1].split(":", 1)
            # Isolate timestamp from remaining information in line
            date_ts[1] = date_ts[1].split(' ', 1)[0]

            # Create new split line for extracting other data
            split_line = line.split(' ')

            # client_ip = split_line[0]   -  Dan unused variable
            request_info = line.split('"', 2)[1]

            method = request_info.split('/', 1)[0]
            # if the request was a GET method, then uri-stem server-client status and bytes received data should exist
            if "GET" in method:
                uri_stem = request_info.split(' ')[1]
                sc_status = split_line[8]
                bytes_received = split_line[9]

            else:
                uri_stem = '-'
                sc_status = '-'
                bytes_received = '-'

            client_ip = split_line[0]

            data = [date_ts[0], date_ts[1], client_ip, method, uri_stem, sc_status, bytes_received]

            log_data[i] = data

            i += 1

        # length represents the number of lines of DATA present in returned parsed list
        log_data['length'] = i
        log_data['date'] = 0
        log_data['timestamp'] = 1
        log_data['client-ip'] = 2
        log_data['method'] = 3
        log_data['uri-stem'] = 4
        log_data['sc-status'] = 5
        log_data['bytes-received'] = 6

        # return the list containing data
        return log_data

    # parse_w3c_to_list will parse all information from an IIS/W3C format log into a list
    # With the locations of each field denoted in the parsed_log['parameter'] field
    # For instance, if c-ip is parsed into the 2 index of each line, requesting parsed_log['c-ip'] will return 2
    # This also works in reverse, so if you need the c-ip from each line, you request parsed_log[parsed_log['c-ip']]
    # For information on what each tag means refer to:
    # https://stackify.com/how-to-interpret-iis-logs/

    @classmethod
    def parse_w3c_to_list(cls, in_file):
        if not in_file:
            return None
        log_data = {}
        potential_parameters = ['date', 'time', 's-sitename', 's-computername', 's-ip', 'cs-method', 'cs-uri-stem',
                                'cs-uri-query', 's-port', 'cs-username', 'c-ip', 'cs(UserAgent)', 'cs(Cookie)',
                                'cs(Referrer)', 'cs-host', 'sc-status', 'sc-substatus', 'sc-win32-status', 'sc-bytes',
                                'cs-bytes', 'time-taken']
        universal_names = ['date', 'timestamp', 'service-name', 'server-name', 'server-ip', 'method', 'uri-stem',
                           'uri-query', 'server-port', 'username', 'client-ip', 'user-agent', 'cookie',
                           'referrer', 'host', 'http-status', 'protocol-substatus', 'win32-status', 'bytes-sent',
                           'bytes-received', 'time-taken']

        log_data['fields'] = -1
        # initialize placeholder variables in log_data array representing each of the w3c format parameters
        for parameter in potential_parameters:
            log_data[parameter] = -1

        i = 0
        # as long as there are lines in the file, loop:
        for line in in_file:
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
                    log_data['fields'] = 1
                    j = 0
                    for element in split_line:
                        for parameter in potential_parameters:

                            if element == parameter:
                                log_data[parameter] = j - 1
                        j += 1
            else:
                if log_data['fields'] == -1:
                    return None
                # print(split_line[log_data['c-ip']])
                log_data[i] = split_line
                i += 1
        # close the file once you're done getting all of the line information
        # once log file is parsed, assign the new positions of each requested parameter in the log_data list
        # this will prevent issues when using methods that rely on tagged element values representing element
        #  placement in array

        k = 0
        for parameter in potential_parameters:
            # add an index in the log_data array representing the universal name for each field
            log_data[universal_names[k]] = log_data[parameter]

            k += 1
        # length represents the number of lines of DATA present in returned parsed list
        log_data['length'] = i
        # return the list containing CSV data
        return log_data

    # requested parameters list can consist of the following, using the official IIS naming convention found in header
    # For information on what each tag means refer to:
    # https://stackify.com/how-to-interpret-iis-logs/

    @classmethod
    def parse_w3c_requested_to_list(cls, in_file, requested_parameters):
        if not in_file:
            return None

        log_data = {}
        # in_file = open('LWTech_auth.log')
        potential_parameters = ['date', 'time', 's-sitename', 's-computername', 's-ip', 'cs-method', 'cs-uri-stem',
                                'cs-uri-query', 's-port', 'cs-username', 'c-ip', 'cs(UserAgent)', 'cs(Cookie)',
                                'cs(Referrer)', 'cs-host', 'sc-status', 'sc-substatus', 'sc-win32-status', 'sc-bytes',
                                'cs-bytes', 'time-taken']

        log_data['header'] = False
        # initialize placeholder variables in log_data array representing each of the w3c format parameters
        for parameter in potential_parameters:
            log_data[parameter] = -1

        i = 0
        # as long as there are lines in the file, loop:
        for line in in_file:
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
                if not log_data['header']:
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

        # once log file is parsed, assign the new positions of each requested parameter in the log_data list to
        # prevent issues when using methods that rely on tagged element values representing element placement in array
        k = 0
        for parameter in requested_parameters:
            log_data[parameter] = k
            k += 1
        # length represents the number of lines of DATA present in returned parsed list
        log_data['length'] = i
        # return the list containing w3c data
        return log_data
