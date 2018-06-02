# Import the re library to support regular expressions
import re
import pathlib
import csv

# The AnaPyzerAnalyzer class contains all methods that are used to process information into a displayable form
# from logs created by AnaPyzerParser object methods.


class AnaPyzerAnalyzer:
    def __init__(self):
        self.DEFAULT_FILE_PATH = pathlib.Path.home()
        self._in_file_path = pathlib.Path('')
        self.file = self._in_file_path
        self._error_listener = None
        self._success_listener = None
        self._known_ips = {}


    @staticmethod
    def is_malicious(timestamps, urls):
        malicious = False
        attempts = 0
        counter = 0
        current_timestamp = 0
        current_url = 1
        for timestamp in timestamps:
            temp = ""
            for c in timestamp:
                if c.isdigit():
                    temp += c
            timestamps[timestamps.index(timestamp)] = temp
        timestamps.sort()
        urls.sort()
        for url in urls:
            try:
                if url == urls[current_url]:
                    malicious = True
                    attempts += 1
                    current_url += 1
                else:
                    current_url += 1

            except IndexError:
                break
        if attempts > 0:
            attempts += 1
        for timestamp in timestamps:
            if (int(timestamp) - int(timestamps[
                                         current_timestamp])) < 11:  # go forward looking for timestamps within 10 secs
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

    def parse_apache(self, in_file_path):
        try:
            self.file = open(in_file_path, 'r')
        except:
            print('Could not open file ' + in_file_path)

        regex_ip_pattern = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)?\s*" (\d{3}) (\S+)'
        # retrieved from https://stackoverflow.com/questions/30956820/log-parsing-with-regex
        parsed_log = {}
        for line in self.file:
            matchobj = re.match(regex_ip_pattern, line, flags=0)
            # Creates a dictionary with the IP address as the key, and
            # a list of lists pertaining to the 8 other groups as the value
            # Group 1 is the ip address
            # for our purposes, i believe only group 1, 4, 6 are necessary
            if matchobj:
                if parsed_log.get(matchobj.group(1)):
                    parsed_log[matchobj.group(1)][0].append(matchobj.group(2))  # Client Identity
                    parsed_log[matchobj.group(1)][1].append(matchobj.group(3))  # user ID
                    parsed_log[matchobj.group(1)][2].append(matchobj.group(4))  # date and time
                    parsed_log[matchobj.group(1)][3].append(matchobj.group(5))  # method
                    parsed_log[matchobj.group(1)][4].append(matchobj.group(6))  # endpoint (url)
                    parsed_log[matchobj.group(1)][5].append(matchobj.group(7))  # protocol
                    parsed_log[matchobj.group(1)][6].append(matchobj.group(8))  # response code
                    parsed_log[matchobj.group(1)][7].append(matchobj.group(9))  # content size
                else:  # some of these groups are often blank
                    parsed_log[matchobj.group(1)] = [[matchobj.group(2)], [matchobj.group(3)], [matchobj.group(4)],
                                                     [matchobj.group(5)], [matchobj.group(6)], [], [matchobj.group(7)],
                                                     [matchobj.group(8)], [matchobj.group(9)]]
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

        # time_place = parsed_log['timestamp']  Dan unused variable
        # cip_place = parsed_log['client-ip']   Dan unused variable

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

        connections_per_hour_table['xlabel'] = "Hour of Day"
        connections_per_hour_table['ylabel'] = "Unique IPs Recorded"
        connections_per_hour_table['title'] = "Connections Per Hour"
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
        current_ip = ''

        while i < parsed_log['length']:

            # Check that the IP address hasn't changed
            if current_ip == parsed_log[i][parsed_log['client-ip']]:
                connection_time += 1

            else:
                if i > 0:
                    connection_time += 1
                    ip_end_time = parsed_log[i - 1][parsed_log['timestamp']]
                    info_array = [connection_time, ip_end_time]

                    if ip_connection_time.get(current_ip):
                        ip_connection_time[current_ip].append(info_array)

                    else:
                        ip_connection_time[current_ip] = [info_array]

                current_ip = parsed_log[i][parsed_log['client-ip']]

                # reset connection_time if ip has changed
                connection_time = 0

            i += 1

        for ip in ip_connection_time:
            # time_sum = 0  Dan unused variable
            for info in ip_connection_time[ip]:
                print("New info:  Requests:" + str(info[0]) + " IP Address: " + ip + " Time disconnected: "
                      + str(info[1]))



    def lookup_ipv4(self, ip):

        ip_split = ip.split(".")
        try:
            ip_1 = int(ip_split[0])
            ip_2 = int(ip_split[1])
            ip_3 = int(ip_split[2])
            ip_4 = int(ip_split[3])
        except ValueError:
            self._known_ips[ip] = "INV"
            return None

        if ip_1 > 255 or ip_1 < 0:
            self._known_ips[ip] = "INV"
            return None
        if ip_2 > 255 or ip_2 < 0:
            self._known_ips[ip] = "INV"
            return None
        if ip_3 > 255 or ip_3 < 0:
            self._known_ips[ip] = "INV"
            return None
        if ip_4 > 255 or ip_4 < 0:
            self._known_ips[ip] = "INV"
            return None

        if self._known_ips.get(ip):
            return self._known_ips[ip]
        else:
            filename = 'ips/ipv4' + str(ip_1) + ".csv"

            try:
                with open(filename, 'r') as ip_db:
                    reader = csv.reader(ip_db)
                    ipv4 = list(reader)
            except:
                if ip_1 >= 225:
                    return "ZZ"
                else:
                    return "INV"
            ip_db.close()

            # format of each line =
            # [0] = starting limit ip_1 [1] = starting limit ip_2 [2] = starting limit ip_3  [3] =starting limit ip_4
            # [4] = ending limit ip_1   [5] = ending limit ip_2   [6] = ending limit ip_3    [7] = ending limit ip_4
            # [8]= Country Code

            i = 0
            # if the starting ip has a number less than the ending ip
            # the entire range of ips starting with ip_1 belongs to the country code in [8]

            if int(ipv4[i][0]) <= ip_1 and int(ipv4[i][4]) > ip_1:
                self._known_ips[ip] = ipv4[i][8]
                return ipv4[i][8]

            while i < len(ipv4):
                if int(ipv4[i][1]) <= ip_2 and int(ipv4[i][5]) > ip_2:
                    self._known_ips[ip] = ipv4[i][8]
                    return ipv4[i][8]

                if int(ipv4[i][2]) <= ip_3 and int(ipv4[i][6]) > ip_3:
                    self._known_ips[ip] = ipv4[i][8]
                    return ipv4[i][8]

                if int(ipv4[i][3]) <= ip_4 and int(ipv4[i][7]) > ip_4:
                    self._known_ips[ip] = ipv4[i][8]
                    return ipv4[i][8]
                i += 1
            # Just in case something doesn't work out, provide a default case of 'unknown'
            self._known_ips[ip] = "INV"
            return "INV"

    def ip_connection_report(self, parsed_log):
        ip_connections = {}

        i = 0
        date = parsed_log[i][parsed_log['date']]
        ip_connections[date] = {}
        # iterate through data of each date recorded
        while i < parsed_log['length']:
            # iterate through the ip addresses recorded
            if parsed_log[i][parsed_log['date']] != date:
                date = parsed_log[i][parsed_log['date']]
                ip_connections[date] = {}

            user_ip_address = str(parsed_log[i][parsed_log['client-ip']])

            # ip_country_code = self.lookup_ipv4(user_ip_address)

            # if ip_country_code is not None:
            #     if ip_connections[date].get(ip_country_code):
            #         ip_connections[date][ip_country_code] += 1
            #     else:
            #         ip_connections[date][ip_country_code] = 1

            if ip_connections[date].get(user_ip_address):
                ip_connections[date][user_ip_address] += 1
            else:
                ip_connections[date][user_ip_address] = 1

            print(ip_connections[date])
            i += 1
        cc_report = {}
        for date in ip_connections:
            cc_report[date] = {}
            for ip_address in ip_connections[date]:
                ip_country_code = self.lookup_ipv4(ip_address)
                if ip_country_code is not None:
                    if cc_report[date].get(ip_country_code):
                        cc_report[date][ip_country_code] += 1
                    else:
                        cc_report[date][ip_country_code] = 1

        cc_report['xlabel'] = "Country Code"
        cc_report['ylabel'] = "Unique Connections"
        cc_report['title'] = "Connections by Country"

        return cc_report