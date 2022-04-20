#!/usr/bin/python3

import requests
import re
from urllib.parse import urljoin


class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.subdomains = []
        self.directories = []
        self.links_to_ignore = ignore_links

    def get_subdomain(self, wordlist):
        with open(wordlist, "r") as list_of_subdomains:
            for word in list_of_subdomains:
                word = word.strip()
                test_url = word + "." + self.target_url.split("://")[1]
                try:
                    response = self.session.get("https://" + test_url)
                    if response:
                        self.subdomains.append(test_url)
                        print(test_url)
                except requests.exceptions.ConnectionError:
                    pass

    def get_directories(self, url=None):
        if url == None:
            url = self.target_url
        response = self.session.get(url)
        href_links = re.findall('(?:href=")(.*?)"', str(response.content))
        for link in href_links:
            test_url = urljoin(url,link)
            if "#" in test_url:
                test_url = test_url.split("#")[0]
            if self.target_url in test_url and test_url not in self.directories and test_url not in self.links_to_ignore:
                self.directories.append(test_url)
                print(test_url)
                self.get_directories(test_url)



wordlist = "worldlists/sample.txt"
target_url = "https://silkavenue.pk/"
ignore_links = "logout.php"

vuln_scanner = Scanner(target_url, ignore_links)

vuln_scanner.get_subdomain(wordlist)
vuln_scanner.get_directories()
