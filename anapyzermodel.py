# Import the pathlib library for cross platform file path abstraction
import pathlib
# Import the re library to support regular expressions
import re

import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd

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
    ACCEPTED_FILE_FORMATS = [('log files', '*.log')]
    FILE_PARSE_MODES = ['Convert to csv', 'Generate graph', 'Count IPs', 'Report Connections Per Hour']
    OUTPUT_FILE_FORMATS = [('CSV (Comma delimited)', '*.csv')]

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
            matchObj = re.match(regex_IP_pattern, line, flags=0)
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

    # this method will analyze the w3c formatted log file currently selected in the GUI
    # and parse it out into a list containing information pertaining to client ip and time of access
    def parse_w3c_to_list(self):
        log_data = {}
        # open log file specified in file_name parameter
        o_file = open(self._in_file_path, 'r')
        log_data['time'] = -1
        log_data['c-ip'] = -1
        log_data['date'] = -1
        # read the current line into a string variable called line
        line = o_file.readline()[:-1]

        i = 0
        # as long as there are lines in the file, loop:
        while line:
            # Split string into list of individual words
            split_line = line.split(' ')

            # this will prevent any lines that are not valid data lines from being moved to the list
            if '#' in split_line[0]:
                log_data[str(split_line[0])] = split_line

                if '#Date' in split_line[0] and log_data['date'] == -1:
                    log_data['date'] = split_line[1]
                    print("Date of record: " + log_data['date'])

                if '#Fields' in split_line[0]:
                    # print("There is a fields line")

                    j = 0
                    for element in split_line:

                        if 'c-ip' in element:
                            log_data['c-ip'] = j - 1
                            # print("c-ip data stored in line "+str(j))

                        if element == 'time':
                            log_data['time'] = j - 1
                            # print("time data stored in line "+str(j))
                        j += 1

            else:
                if log_data['c-ip'] == -1:
                    print("No user IP address information found in header")
                    break
                if log_data['time'] == -1:
                    print("No time information found in header")
                    break

                # print("log_data["+str(i)+"] = "+str(split_line))
                log_data[i] = split_line
                i += 1

            line = o_file.readline()[:-1]
        # close the file once you're done getting all of the line information
        log_data['length'] = i
        o_file.close()
        # return the list containing CSV data
        return log_data

    # get_connections_per_hour takes in a log parsed by the above parse_w3c_tolist method
    # and returns a list containing how many unique ip connections were present during each hour of the day
    # this parsed list can be used with the plot_hourly_connections method
    def get_connections_per_hour(self, parsed_log):
        connections_per_hour_table = {}
        # print("getting connections per hour")
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
        plt.figure()
        plt.xlabel("Hour of Day")
        plt.ylabel("Unique IPs Accessing")
        # plt.legend(title=str(connections_log[0][0]))
        # plot the data in a very ugly chart (figure out how to beautify)

        plt.plot(connections_log.keys(), connections_log.values())
        report_string = ''

        for line in connections_log:
            report_string += str(connections_log[line]) + " unique connections at " + line + ":00 \n"

        # show the newly created data plot.
        plt.show()

