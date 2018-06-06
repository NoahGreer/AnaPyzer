# Import the re library to support regular expressions
import re
import pathlib
import csv

# The AnaPyzerAnalyzer class contains all methods that are used to process information into a displayable form
# from logs created by AnaPyzerParser object methods.
class AnaPyzerAnalyzer:
    def __init__(self):
        self._known_ips = {}

    @staticmethod
    def malicious_activity_report(parsed_log):
        ip_address_log_info_dict = {}

        for entry in range(0, parsed_log['length']):
            log_entry_ip = parsed_log[entry][parsed_log['client-ip']]
            if log_entry_ip in ip_address_log_info_dict:
                ip_address_log_info_dict[log_entry_ip]['dates'].append(parsed_log[entry][parsed_log['date']])
                ip_address_log_info_dict[log_entry_ip]['timestamps'].append(parsed_log[entry][parsed_log['timestamp']])
                ip_address_log_info_dict[log_entry_ip]['urls'].append(parsed_log[entry][parsed_log['uri-stem']])
            else:
                ip_address_log_info_dict[log_entry_ip] = {
                    'dates': [parsed_log[entry][parsed_log['date']]],
                    'timestamps': [parsed_log[entry][parsed_log['timestamp']]],
                    'urls': [parsed_log[entry][parsed_log['uri-stem']]]
                }
        report_output = ""

        for ip in ip_address_log_info_dict:
            malicious = False
            attempts = 1
            counter = 0
            current_timestamp = 0
            current_url = 1
            current_index = 0

            timestamps = ip_address_log_info_dict[ip]['timestamps']
            urls = ip_address_log_info_dict[ip]['urls']

            for timestamp in timestamps:
                temp = ""
                for c in timestamp:
                    if c.isdigit():
                        temp += c
                timestamps[timestamps.index(timestamp)] = temp
            timestamps.sort()
            urls.sort()
            url_attempts = []
            for url in urls:
                try:
                    if url == urls[current_url]:
                        attempts += 1
                        current_url += 1
                        if attempts > 3 and url not in url_attempts:
                            url_attempts.append(url)
                            malicious = True
                    else:
                        current_url += 1
                        attempts = 1

                except IndexError:
                    break
                current_index = 0
            for timestamp in timestamps:
                if (int(timestamp) - int(timestamps[current_timestamp])) < 11:  # go forward looking for timestamps within 10 secs
                    counter += 1
                else:
                    current_timestamp = current_index
                    counter = 0
                    for i in range(1, 10):
                        try:
                            if (int(timestamps[current_timestamp]) - int(timestamps[current_timestamp - i])) < 11:
                                counter += 1
                        except IndexError:
                            break
                if counter >= 10 and malicious:
                    report_output += "Malicious activity detected from " + ip + "\n"
                    for url in url_attempts:
                        report_output += url + "  was accessed more than three times within ten seconds by " + ip + "\n"
                    malicious = False
                current_index += 1
        return report_output


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


    def _lookup_ipv4(self, ip):

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

            #print(ip_connections[date])
            i += 1
        cc_report = {}
        for date in ip_connections:
            cc_report[date] = {}
            for ip_address in ip_connections[date]:
                ip_country_code = self._lookup_ipv4(ip_address)
                if ip_country_code is not None:
                    if cc_report[date].get(ip_country_code):
                        cc_report[date][ip_country_code] += 1
                    else:
                        cc_report[date][ip_country_code] = 1

        cc_report['xlabel'] = "Country Code"
        cc_report['ylabel'] = "Unique Connections"
        cc_report['title'] = "Connections by Country"

        return cc_report
