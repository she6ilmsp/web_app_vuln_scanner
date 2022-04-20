#!/usr/bin/python3

import scanner

wordlist = "worldlists/sample.txt"
target_url = "johnnys-fresh-site-1b1b85.webflow.io/"
subdomains=[]
directories=[]

vuln_scanner = scanner.Crawler(target_url)
subdomains.append(vuln_scanner.get_subdomain(wordlist))
directories.append(vuln_scanner.get_directories())

for x in subdomains:
    print(x)

for y in directories:
    print(y)