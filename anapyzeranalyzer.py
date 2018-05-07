# Import the re library to support regular expressions
import re

class my_class(object):
    def __init__(self, in_file_path):
        self.in_file_path = in_file_path

    def is_malicious(self, timestamps):
        timestamps.sort()
        malicious = False
        counter = 0
        current = 0
        last = timestamps[len(timestamps) - 1]
        if (last - timestamps[current]) < 10:
            return malicious
        for timestamp in timestamps:
            if (timestamp - current) <+ 10:
                counter += 1
            else:
                current = timestamps.index(timestamp)
            if counter > 10:
                malicious = True
        return malicious

    def get_timestamps(self):
        try:
            self.in_file = open(self.in_file_path, 'r')
        except:
            print('Could not open file ' + self.in_file_path)

        # Regex pattern for IPv4 addresses retrieved from https://www.regular-expressions.info/ip.html
        regex_IP_pattern = r'\b(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b'       
        IP_address_timestamps = {}
        for line in self.in_file:            
            matchObj = re.match(regex_IP_pattern, line, flags = 0)
            timestamp = ""
            counter = 0
            for c in line:
                if c == "[":
                    counter += 1
                elif c == "+":
                    counter += 1
                elif counter == 1 and c.isdigit():
                    timestamp += str(c)
                    
            if matchObj:
                if IP_address_timestamps.get(matchObj.group()):
                    IP_address_timestamps[matchObj.group()].append(timestamp)
                else:
                    IP_address_timestamps[matchObj.group()] = [timestamp]
        self.in_file.close()
        num_users = len(IP_address_timestamps)
        output_string = ''
        for IP_address, timestamps in IP_address_timestamps.items():
            output_string += '{} : {}\n'.format(IP_address, timestamps)
        output_string += "Total Number of Users: {}".format(num_users)
        return output_string
        