import csv
import os
import zipfile
    
filepath = os.path.dirname(os.path.realpath(__file__))


def ip_file_parse(ip_list):

    parsed_ips = {}
    #This will parse an array of ip addresses into an array of four ints

    for item in ip_list:
        #get representation of array item as string, for easier parsing
        item_string = ""
        #Look for ipv4 using ###.###.###.### notation
        if '.' in str(item):
            item_string = "ipv4"
            #split string into 4 strings
            ip_starting_split = item[0].split('.')
            i = 0
            #ip_starting_split represents the first ip address in a particular group belonging to a country
            #parse each string into an int for mathematical comparison with collected ips
            for ip in ip_starting_split:
                ip_starting_split[i] = int(ip)
                i+=1
            #ip_ending_split represents the final ip address in a particular group belonging to a country    
            ip_ending_split = item[1].split('.')
            i = 0
            for ip in ip_ending_split:
                ip_ending_split[i] = int(ip)
                i+=1
                
        #look for ipv6 using ####:####:####:####:####:####:####:####
        if ':' in str(item):
            item_string = "ipv6"
            ip_starting_split = item[0].split(':')
            if len(ip_starting_split) <= 7:
                while len(ip_starting_split) <= 7:
                    ip_starting_split.append('0')
            i = 0

            #account for all ''s in file, make them 0s to allow for int comparison
            for ip in ip_starting_split:
                if ip is not '':
                    ip_starting_split[i] = int(ip,16)
                    i+=1
                if ip is '':
                    ip_starting_split[i] = 0
                    i+=1

            
            ip_ending_split = item[1].split(':')
            i = 0
            for ip in ip_ending_split:
                if ip is not '':
                    ip_ending_split[i] = int(ip,16)
                    i+=1

        newline = []
        for ip in ip_starting_split:
            newline.append(ip)
        
        for ip in ip_ending_split:
            newline.append(ip)
        newline.append(item[2])

        if parsed_ips.get(item_string):
            if parsed_ips[item_string].get(newline[0]):

                parsed_ips[item_string][newline[0]] += [newline]
            else:
                parsed_ips[item_string][newline[0]] = [newline]
        else:
            parsed_ips[item_string] = {}
            parsed_ips[item_string][newline[0]] = [newline]

    return parsed_ips

def unzip_database():
    
    try:
        with zipfile.ZipFile("ips.zip","r") as zip_ref:
            zip_ref.extractall(str(filepath))
        print("ips.zip found.  Extracting to /ips")
        return False
    except:
        print("IP database zip file not found.  Attemping to create from CSV file.")
        return True

def create_database_from_ip_file():

    print("Checking for database file.")

    try:
        with open('ips.csv','r') as ip_db:
            reader = csv.reader(ip_db)
            
            ip_db_list = list(reader)
        print("ips.csv file found.")
        ip_db.close()
    except IOError:
        
        
        print("ips.csv file not found.  Make sure the IP/country code csv file downloaded from https://db-ip.com/db/download/country is renamed 'ips.csv' before running this script.")
        return

    if os.path.isdir(str(filepath)+"/ips"):
        print("IP directory found.")
    else:
        print("IP directory does not exist.  Creating ./ips now.")
        os.makedirs(str(filepath)+"/ips")

    print("Parsing data from ips.csv into database files.")
    parsed_ips = ip_file_parse(ip_db_list)


    for ip in parsed_ips['ipv4']:
        csvfile = "ips/ipv4"+str(parsed_ips['ipv4'][ip][0][0]) + ".csv"
    # #Assuming res is a list of lists
        with open(csvfile, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(parsed_ips['ipv4'][ip])

    print("Database creation complete.  Enjoy using AnaPyzer.")

if unzip_database():
    create_database_from_ip_file()

print("Press any key to exit")
input()