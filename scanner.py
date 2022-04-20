#!/usr/bin/python3

import requests
import re
from urllib.parse import urljoin


class Crawler:
    def __init__(self, url):
        self.target_url = url
        self.session = requests.Session()
    def get_subdomain(self, wordlist):
        with open(wordlist, "r") as list_of_subdomains:
            for word in list_of_subdomains:
                word = word.strip()
                test_url = word + "." + self.target_url
                try:
                    response = self.session.get("https://" + test_url)
                    if response:
                        return test_url
                except requests.exceptions.ConnectionError:
                    pass
    def get_directories(url=None):
        if url == None:
            url = self.target_url
        response = self.session.get(url)
        href_links = re.findall('(?:href=")(.*?)"', str(response.content))
        for link in href_links:
            test_url = urljoin(url,link)
            if "#" in test_url:
                test_url = test_url.split("#")[0]
            if url in test_url and test_url not in directories:
                return test_url
                self.get_directories(test_url)

