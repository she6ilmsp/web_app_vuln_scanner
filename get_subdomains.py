#!/usr/bin/python3

import requests

class Scanner:
    def __init__(self, target_url, wordlist):
        self.session = requests.Session()
        self.target_url = target_url
        self.wordlist = wordlist
        self.subdomains = []
    def get_subdomain(self):
        with open(self.wordlist, "r") as list_of_subdomains:
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

target_url = ""
wordlist = "subdomain_wordlist.txt"

try:
    find_subdomains = Scanner(target_url, wordlist)
    find_subdomains.get_subdomain()
except KeyboardInterrupt():
    print("\nExiting program.......")
    quit()