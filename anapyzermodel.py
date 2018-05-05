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
        return u"FileException(file={0!r}, file_mode={1!r})".format(self.file, self.file_mode)

    __str__ = __repr__

# Class definition for the file reader of the application
class AnaPyzerModel():
    # 'constant' for the accepted log file types
    ACCEPTED_LOG_TYPES = ['Apache (access.log)', 'IIS (u_ex*.log)']
    ACCEPTED_FILE_FORMATS = [('log files', '*.log')]
    FILE_PARSE_MODES = ['Convert to csv', 'Generate graph', 'Count IPs']
    OUTPUT_FILE_FORMATS = [('CSV (Comma delimited)', '*.csv')]

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

    # Getter for the model's file type of the expected input log type
    # Returns a string representing the expected input log type
    def get_log_type(self):
        return self.log_type

    def set_file_parse_mode(self, file_parse_mode):
        self.file_parse_mode = file_parse_mode

    def get_file_parse_mode(self):
        return self.file_parse_mode

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

    def read_file_to_csv(self, output_path):
        try:
            in_file = open(self.in_file_path, 'r')
        except:
            raise AnaPyzerFileException(file=self.in_file_path, file_mode='r')

        try:
            out_file = open(output_path, 'w')
        except:
            in_file.close()
            raise AnaPyzerFileException(file=output_path, file_mode='w')

        for line in in_file:
            converted_line = re.sub("\s+", ",", line.strip())
            out_file.write(converted_line + '\n')

        in_file.close()
        out_file.close()

        return True

    # parse_W3C_to_list takes in the LWTechauth.txt file and parses it into a list.
    # This method is going to be extensively rewritten so that it will be able to
    def parse_W3C_to_list(file_name):
        log_data = []
        # open log file specified in file_name parameter
        oFile = open(file_name, 'r')

        # read the current line into a string variable called line
        line = oFile.readline()[:-1]

        # as long as there are lines in the file, loop:
        while line:
            # Split string into list of individual words
            split_line = line.split(' ')
            # this will prevent any lines that are not valid data lines from being moved to the list
            if '#' not in split_line[0]:
                log_data.append(split_line)

            line = oFile.readline()[:-1]
        # close the file once you're done getting all of the line information
        oFile.close()
        # return the list

    def get_connections_per_hour(log):
        connections_per_hour_table = {}
        for data in log:
            # iterate through the ip addresses recorded
            time_string = str(data[1])
            hours = time_string[:2]
            user_ip_address = str(data[8])

            if connections_per_hour_table.get(hours):
                connections_per_hour_table[hours] += [user_ip_address]
            else:
                connections_per_hour_table[hours] = [user_ip_address]

        for time in connections_per_hour_table:
            ip_count = len(set(connections_per_hour_table[time]))
            connections_per_hour_table[time] = ip_count

        # for time in connections_per_hour_table:
        #     print(str(connections_per_hour_table[time]) + " unique connections at "+ time)
        return connections_per_hour_table

    containing CSV data
        return log_data

    # The plot_connections method will take in a log formatted by the above method

    def announce_connections(connections_log):
        for log in connections_log:
            print(str(connections_log[log]) + " unique connections found at " + log)

    # The plot_connections method will take in a log formatted by the above method
    def plot_connections(connections_log):
        plt.xlabel("Hour of Day")
        plt.ylabel("Unique IPs Accessing")
        # plt.legend(title=str(connections_log[0][0]))
        # plot the data in a very ugly chart (figure out how to beautify)
        plt.plot(connections_log.keys(), connections_log.values())

        # show the newly created data plot.
        plt.show()
