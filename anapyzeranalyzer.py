# Import the re library to support regular expressions
import re


class analyzer(object):
    def __init__(self, in_file_path):
        self.in_file_path = in_file_path

    def is_malicious(self, timestamps):
        timestamps.sort()
        malicious = False
        counter = 0
        current = 0
        for timestamp in timestamps:
            if (int(timestamp) - int(timestamps[current])) < 11:   #goes forward lookin for timestamps within ten seconds of current
                counter += 1
            else:
                current = timestamps.index(timestamp)
                counter = 0
                for i in range(1, 10):
                    try:
                        if (int(timestamps[current]) - int(timestamps[current - i])) < 11:
                            counter += 1
                    except IndexError:
                        break
            if counter > 100:
                malicious = True
        return malicious

    def parse_apache(self):
        try:
            self.in_file = open(self.in_file_path, 'r')
        except:
            # TODO change this to a GUI message window
            print('Could not open file ' + self.in_file_path)

        regex_IP_pattern = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)?\s*" (\d{3}) (\S+)'
        # retrieved from https://stackoverflow.com/questions/30956820/log-parsing-with-regex
        parsed_log = {}

        for line in self.in_file:
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
        self.in_file.close()
        return parsed_log