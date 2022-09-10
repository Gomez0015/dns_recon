#!/usr/bin/env python

# Script for DNS enumeration

import dns.resolver
import sys

if len(sys.argv) < 2:
    print('Usage: dns_recon target.com')
    exit(11)
else:
    target=sys.argv[1]


dnsIP='8.8.8.8'

my_resolver = dns.resolver.Resolver()
my_resolver.nameservers = [dnsIP]

def main():
    print(f'Starting dump on: {target}')
    print('-' * 20)
    records_scan(['A', 'TXT', 'MX', 'CNAME', 'AAAA'])
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

main()