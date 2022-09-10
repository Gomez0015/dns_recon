#!/usr/bin/env python

# Script for DNS enumeration

import dns.resolver
import sys
import time
import socket

if len(sys.argv) < 2:
    print('Usage: dns_recon target.com')
    exit(11)
else:
    try:
        target=socket.gethostbyaddr(sys.argv[1])[0]
    except socket.herror:
        target=sys.argv[1]

dnsIP='8.8.8.8'

my_resolver = dns.resolver.Resolver()
my_resolver.nameservers = [dnsIP]

def main():
    print(f'Starting dump on: {target}')
    print('-' * 20)
    records_scan(['A', 'TXT', 'MX', 'CNAME', 'AAAA'])
    print('-' * 20)
    enum_subdomains()
    print('-' * 20)

def records_scan(queries):
    print(f'- DNS Server: {dnsIP}')
    print('\n')

    for query in queries:
        try:
            result = dns.resolver.resolve(target, query)
            for exdata in result:
                print(f'- {query} Record:', exdata)
        except:
            print(f'- No {query} Records')

        print('\n')

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

def enum_subdomains():
    try:
        wordlist = open("./dicts/subdomains.txt", "r")
    except:
        wordlist = open("/usr/share/dns_recon/dicts/subdomains.txt", "r")

    queries = ['A', 'TXT']
    total = wordlist.readline().replace('\n', '')
    index = 0

    print("Starting subdomains search")

    for word in wordlist:
        found = False

        word = word.replace('\n', '')
        print(f"Trying {index}/{total} {word}")
        print(LINE_UP, end=LINE_CLEAR)

        for query in queries:
            try:
                dns.resolver.resolve(f'{word}.{target}', query)
                found = True
            except Exception:
                pass

        if found:
            print(f'- {word}.{target}')

        index += 1

try:
    main()
except KeyboardInterrupt:
    print('\nKeyboard Interrupt /!\ \n')