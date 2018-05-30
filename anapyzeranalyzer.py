# Import the re library to support regular expressions
import re
import pathlib

"""
The AnaPyzerAnalyzer class contains all methods that are used to process information into a displayable form
from logs created by AnaPyzerParser object methods.
"""
class AnaPyzerAnalyzer:
    def __init__(self):
        self.DEFAULT_FILE_PATH = pathlib.Path.home()
        self._in_file_path = pathlib.Path('')
        self._error_listener = None
        self._success_listener = None

    def is_malicious(self, timestamps, urls):
        malicious = False
        attempts = 0
        counter = 0
        current_timestamp = 0
        current_url = 1
        for timestamp in timestamps:
            temp = ""
            for c in timestamp:
                if (c.isdigit()):
                    temp += c
            timestamps[timestamps.index(timestamp)] = temp
        timestamps.sort()
        urls.sort()
        for url in urls:
            try:
                if (url == urls[current_url]):
                    malicious = True
                    attempts += 1
                    current_url += 1
                else:
                    current_url += 1

            except IndexError:
                break
        if (attempts > 0):
            attempts += 1
        for timestamp in timestamps:
            if (int(timestamp) - int(timestamps[
                                         current_timestamp])) < 11:  # goes forward lookin for timestamps within ten seconds of current
                counter += 1
            else:
                current_timestamp = timestamps.index(timestamp)
                counter = 0
                for i in range(1, 10):
                    try:
                        if (int(timestamps[current_timestamp]) - int(timestamps[current_timestamp - i])) < 11:
                            counter += 1
                    except IndexError:
                        break
            if counter > 100:
                malicious = True
        return malicious

    def parse_apache(self):
        try:
            self.file = open(self.in_file_path, 'r')
        except:
            print('Could not open file ' + self.in_file_path)

        regex_IP_pattern = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)?\s*" (\d{3}) (\S+)'
        # retrieved from https://stackoverflow.com/questions/30956820/log-parsing-with-regex
        parsed_log = {}

        for line in self.file:
            matchObj = re.match(regex_IP_pattern, line, flags=0)
                                                         # Creates a dictionary with the IP address as the key, and a list of lists
            if matchObj:  # Group 1 is ip address       #pertaing to the 8 other groups as the value
                if parsed_log.get(matchObj.group(1)):  # for our purposes, i believe only group 1, 4, 6 are necessary
                    parsed_log[matchObj.group(1)][0].append(matchObj.group(2))  # Client Identity
                    parsed_log[matchObj.group(1)][1].append(matchObj.group(3))  # user ID
                    parsed_log[matchObj.group(1)][2].append(matchObj.group(4))  # date and time
                    parsed_log[matchObj.group(1)][3].append(matchObj.group(5))  # method
                    parsed_log[matchObj.group(1)][4].append(matchObj.group(6))  # endpoint (url)
                    parsed_log[matchObj.group(1)][5].append(matchObj.group(7))  # protocol
                    parsed_log[matchObj.group(1)][6].append(matchObj.group(8))  # response code
                    parsed_log[matchObj.group(1)][7].append(matchObj.group(9))  # content size
                else:  # some of these groups are often blank
                    parsed_log[matchObj.group(1)] = [[matchObj.group(2)], [matchObj.group(3)], [matchObj.group(4)],
                                                     [matchObj.group(5)], [matchObj.group(6)], [], [matchObj.group(7)],
                                                     [matchObj.group(8)], [matchObj.group(9)]]
        self.file.close()
        return parsed_log


    # get_connections_per_hour takes in a log parsed by the above parse_w3c_tolist method
    # and returns a list containing how many unique ip connections were present during each hour of the day
    # this parsed list can be used with the plot_hourly_connections method
    @staticmethod
    def get_connections_per_hour(parsed_log):
        connections_per_hour_table = {}

        if parsed_log is None:
            return None

        time_place = parsed_log['timestamp']
        cip_place = parsed_log['client-ip']


        i = 0
        date = parsed_log[i][parsed_log['date']]
        connections_per_hour_table[date] = {}
        while i < parsed_log['length']:
            # iterate through the ip addresses recorded
            if parsed_log[i][parsed_log['date']] != date:
                date = parsed_log[i][parsed_log['date']]
                connections_per_hour_table[date] = {}

            time_string = str(parsed_log[i][parsed_log['timestamp']])
            user_ip_address = str(parsed_log[i][parsed_log['client-ip']])

            # time_string = str(time_string)
            # user_ip_address = str(user_ip_address)
            # print("Time string = " + time_string)
            # print("IP address = "+ user_ip_address)
            hours = time_string[:2]

            if connections_per_hour_table[date].get(hours):
                connections_per_hour_table[date][hours] += [user_ip_address]
            else:
                connections_per_hour_table[date][hours] = [user_ip_address]
            i += 1

        for date in connections_per_hour_table:
            for time in connections_per_hour_table[date]:
                ip_count = len(set(connections_per_hour_table[date][time]))
                connections_per_hour_table[date][time] = ip_count

        # print("connections per hour report complete")
        # for time in connections_per_hour_table:
        #     print(str(connections_per_hour_table[time]) + " unique connections at "+ time)
        return connections_per_hour_table

    # The plot_connections method take a log formatted by the get_connections_per_hour method
    @staticmethod
    def announce_connections(connections_log):
        for date in connections_log:
            print(date)
            for log in connections_log[date]:
                print(str(connections_log[date][log]) + " unique connections found at " + log + ":00")

    @staticmethod
    def get_connection_length_report(parsed_log):

        ip_connection_time = {}
        i = 0
        connection_time = 0
        current_IP = ''

        while i < parsed_log['length']:

            # Check that the IP address hasn't changed
            if current_IP == parsed_log[i][parsed_log['client-ip']]:
                connection_time += 1

            else:
                if i > 0:
                    connection_time += 1
                    IP_end_time = parsed_log[i - 1][parsed_log['timestamp']]
                    info_array = [connection_time, IP_end_time]

                    if ip_connection_time.get(current_IP):
                        ip_connection_time[current_IP].append(info_array)

                    else:
                        ip_connection_time[current_IP] = [info_array]

                current_IP = parsed_log[i][parsed_log['client-ip']]

                # reset connection_time if ip has changed
                connection_time = 0

            i += 1

        for ip in ip_connection_time:
            time_sum = 0
            for info in ip_connection_time[ip]:
                print("New info:  Requests:" + str(info[0]) + " IP Address: " + ip + " Time disconnected: " + str(
                    info[1]))