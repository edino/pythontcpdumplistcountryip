import subprocess
import re

def get_unique_ips():
    tcpdump_cmd = "sudo tcpdump -veni -s0 -Q in -c 10 'not (host 54.228.158.66)' | awk '/IP/{print $3}' | sort -u"
    process = subprocess.Popen(tcpdump_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error}")
        return []
    return output.splitlines()

def get_country(ip):
    try:
        # Construct the curl command to retrieve data
        curl_cmd = f"curl -s 'http://ip-api.com/json/{ip}'"

        # Execute the curl command
        process = subprocess.Popen(curl_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        if error:
            print(f"Error: {error}")
            return "Unknown"
        
        # Extract country from the output
        country_data = re.search(r'"country":"([^"]+)"', output)
        if country_data:
            country_name = country_data.group(1)
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
