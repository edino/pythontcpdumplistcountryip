import subprocess
from collections import defaultdict

def get_unique_ips():
    # Run tcpdump and collect IP addresses
    tcpdump_command = ['sudo', 'tcpdump', '-n', '-c', '1000']
    tcpdump_output = subprocess.run(tcpdump_command, capture_output=True, text=True)
    
    ip_addresses = set()
    lines = tcpdump_output.stdout.split('\n')
    
    for line in lines:
        if 'IP' in line:
            ip = line.split()[2].split('.')[0]
            ip_addresses.add(ip)
    
    return list(ip_addresses)

def get_countries(ip_addresses):
    # Get countries for each IP address
    countries = defaultdict(str)
    for ip in ip_addresses:
        command = ['geoiplookup', ip]
        result = subprocess.run(command, capture_output=True, text=True)
        country = result.stdout.split()[-1]
        countries[ip] = country

    return countries

if __name__ == "__main__":
    unique_ips = get_unique_ips()
    ip_countries = get_countries(unique_ips)
    
    for ip, country in ip_countries.items():
        print("IP: %s | Country: %s" % (ip, country))
