import subprocess
import requests

def get_unique_ips():
    # Run tcpdump to capture packets and extract unique IP addresses
    tcpdump_cmd = "sudo tcpdump -veni PortB -s0 -Q in -c 1000 'not (host 54.228.158.66)' | awk '/IP/{print $3}' | sort -u"
    process = subprocess.Popen(tcpdump_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error}")
        return []
    return output.splitlines()

def get_country(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            country_name = data.get("country", "Unknown")
            return country_name
        else:
            return "Unknown"
    except requests.RequestException as e:
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
