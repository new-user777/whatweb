import requests
from bs4 import BeautifulSoup
from termcolor import colored
import socket
from urllib.parse import urlparse

class WhatWeb:
    def __init__(self, target_url):
        self.target_url = target_url
        self.headers = {'User-Agent': 'WhatWebScanner'}

    def scan(self):
        try:
            response = requests.get(self.target_url, headers=self.headers, allow_redirects=False)
            response.raise_for_status()

            self.analyze_response(response)
            self.scan_ports()
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def analyze_response(self, response):
        print("""
        Response Headers:
        """)
        for header, value in response.headers.items():
            if header.lower() == 'location' and value.startswith('http'):
                print(colored(f"{header}: {value}", 'blue'))
            else:
                print(f"{header}: {value}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information from headers
        server_header = response.headers.get('Server', 'N/A')
        x_powered_by_header = response.headers.get('X-Powered-By', 'N/A')

        print("Server:", server_header)
        print("X-Powered-By:", x_powered_by_header)

        # Analyze HTML content
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if 'name' in tag.attrs and 'content' in tag.attrs:
                print(f"Meta Tag: {tag['name']} - {tag['content']}")

    def scan_ports(self):
        open_ports = []
        target_host = urlparse(self.target_url).hostname

        for port in range(1, 65536):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()

        print("Open Ports:")
        for port in open_ports:
            print(f"Port: {port}")

if __name__ == "__main__":
    target_url = input("Enter the target URL:[include http/https] ")
    scanner = WhatWeb(target_url)
    scanner.scan()
