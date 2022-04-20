#!/usr/bin/python3

import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url):
        self.session = requests.Session()
        self.target_url = url
        self.payload = "<ScrIpT>alert('poda');</scRiPt>"
        self.directories = []

    def get_directories(self, url=None):
        if url == None:
            url = self.target_url
        response = self.session.get(url)
        href_links = re.findall('(?:href=")(.*?)"', str(response.content))
        for link in href_links:
            test_url = urljoin(url,link)
            if "#" in test_url:
                test_url = test_url.split("#")[0]
            if self.target_url in test_url and test_url not in self.directories and "logout" not in test_url:
                self.directories.append(test_url)
                print("[+] " + test_url)
                self.get_directories(test_url)

    def get_forms(self, url=None):
        if url == None:
            url = self.target_url
        response = self.session.get(url)
        parsed_html = BeautifulSoup(str(response.content), features="lxml")
        return parsed_html.find_all("form")

    def post_form(self, form, value, url):
        action = form.get("action")
        post_url = urljoin(url, action)
        method = form.get("method")
        input_lists = form.find_all("input")
        post_data = {}
        for input in input_lists:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value
            post_data[input_name] = input_value
        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    def run_scanner(self):
        for directory in self.directories:
            forms = self.get_forms(directory)
            for form in forms:
                print("Testing form in " + directory)
                is_vulnerable_to_xss = self.test_xss_vuln_in_post(form, directory)
                if is_vulnerable_to_xss:
                    print("\n\n[+++++] XSS Vulnerability found in form\n\n")
            
            if "=" in directory:
                print("\nTesting parameter in " + directory)
                is_vulnerable_to_xss = self.test_xss_vuln_in_get(directory)
                if is_vulnerable_to_xss:
                    print("\n\n[+++++] XSS Vulnerability found in parameter\n\n")

    def test_xss_vuln_in_get(self, url):
        url = url.replace("=", "=" + self.payload)
        response = self.session.get(url)
        return self.payload in str(response.content)

    def test_xss_vuln_in_post(self, form, url):
        response = self.post_form(form, self.payload, url)
        return self.payload in str(response.content)


target_url = ""

try:
    vuln_scanner = Scanner(target_url)
    print("All directories belongs to this website are...\n")
    vuln_scanner.get_directories()
    if vuln_scanner.directories != None:
        print("\nFound all directories\n")
    else:
        print("\nOops! didn't find any directories\n")

    print("\nTesting directories if there is any vulnerability..\n")
    vuln_scanner.run_scanner()
    print("\nTesting finished.")
except KeyboardInterrupt:
    print("\nExiting program.......")
    quit()