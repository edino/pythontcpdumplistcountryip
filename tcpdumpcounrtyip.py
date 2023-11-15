import subprocess
import re
import json
import socket

def get_unique_ips():
    # Run tcpdump to capture packets and extract unique IP addresses
    tcpdump_cmd = "sudo tcpdump -veni PortB -s0 -Q in -c 10 'not (host 54.228.158.66)' | awk '/IP/{print $3}' | sort -u"
    process = subprocess.Popen(tcpdump_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error}")
        return []
    return output.splitlines()

def get_country(ip):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the API endpoint
            s.connect(("ip-api.com", 80))

            # Send GET request
            request = f"GET /json/{ip} HTTP/1.1\r\nHost: ip-api.com\r\nConnection: close\r\n\r\n"
            s.send(request.encode())

            # Receive response data
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data

            # Extract country from response
            country_data = re.search(b'"country":"([^"]+)"', response)
            if country_data:
                country_name = country_data.group(1).decode()
                return country_name
            else:
                return "Unknown"
    except Exception as e:
        print(f"Error fetching data for IP {ip}: {e}")
        return "Unknown"

def main():
    unique_ips = get_unique_ips()
    if unique_ips:
        for ip in unique_ips:
            country = get_country(ip)
            print(f"IP Address: {ip} | Country: {country}")

if __name__ == "__main__":
    main()
