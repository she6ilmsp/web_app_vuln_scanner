#!/usr/bin/python3

import requests
import re
from urllib.parse import urljoin

subdomains = []
directories = []

def get_subdomain(url):
    with open("worldlists/sample.txt", "r") as list_of_subdomains:
        for word in list_of_subdomains:
            word = word.strip()
            test_url = word + "." + url
            try:
                response = requests.get("https://" + test_url)
                if response:
                    subdomains.append(test_url)
            except requests.exceptions.ConnectionError:
                pass


def get_directories(url):
    response = requests.get(url)
    href_links = re.findall('(?:href=")(.*?)"', str(response.content))
    for link in href_links:
        test_url = urljoin(url,link)
        if "#" in test_url:
            test_url = test_url.split("#")[0]
        if url in test_url and test_url not in directories:
            directories.append(test_url)
            get_directories(test_url)


# get_directories("https://facebook.com")
# get_subdomain("facebook.com")
# print(subdomains)
# print(directories)