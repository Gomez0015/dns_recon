#!/usr/bin/env python

# Script for DNS enumeration

from json import load
import dns.zone
import dns.resolver
import sys
import os
import time
import socket
import getopt
from datetime import datetime
startTime = datetime.now()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'

# Print help message
def printHelp():
    print('Usage: dns_recon target.com [Options]')
    print(f'\n{bcolors.UNDERLINE}SCAN SPECIFICATION:{bcolors.ENDC}')
    print(f'	{bcolors.OKBLUE}-d, --dns {bcolors.ENDC}# Define DNS server')
    print(f'	{bcolors.OKBLUE}-s, --subdomain-enum {bcolors.ENDC}# Enumerate subdomains')
    print(f'	{bcolors.OKBLUE}-z, --zone-transfer {bcolors.ENDC}# Attempt a zone transfer')
    print(f'	{bcolors.OKBLUE}-s, --subdomain-enum {bcolors.ENDC}# Enumerate subdomains')
    sys.exit()

dnsIPs=['8.8.8.8', '1.1.1.1']

my_resolver = dns.resolver.Resolver()

subdomainE = False
zoneT = False
port = 53
target=sys.argv[1]

def main(argv):

    print('dns_recon v0.1 ( https://github.com/Gomez0015/dns_recon )\n')

    try:
        opts, args = getopt.getopt(argv,"hszp:d:",["dns=", "port=", "help", "subdomain-enum", "zone-transfer"])
    except getopt.GetoptError:
        printHelp()

	# Check arguments and set variables
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printHelp()

        if opt in ("-s", "--subdomain-enum"):
            global subdomainE
            subdomainE = True

        if opt in ("-z", "--zone-transfer"):
            global zoneT
            zoneT = True

        if opt in ("-p", "--port="):
            global port
            port = arg

        if opt in ("-d", "--dns="):
            global dnsIP
            dnsIPs = [socket.gethostbyname(arg)]

    my_resolver.port = port
    my_resolver.nameservers = dnsIPs

    for ip in dnsIPs:
        my_resolver.nameserver_ports[ip] = port

    print(f'[*] Starting dump on: {target}')
    print('-' * 20)
    records_scan(['A', 'TXT', 'MX', 'CNAME', 'AAAA', 'SOA', 'NS'])
    
    if(zoneT == True):
        print('-' * 20)
        zone_transfer()

    if(subdomainE == True):
        print('-' * 20)
        enum_subdomains()
    
    
    print('-' * 20)

def records_scan(queries):
    print(f'[+] DNS Server/s: {my_resolver.nameservers}')
    print('\n')

    for query in queries:
        try:
            result = my_resolver.resolve(target, query)
            for exdata in result:
                print(f'[+] {query} Record:', exdata)
        except KeyboardInterrupt:
            print('\n\n/!\ Keyboard Interrupt')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except:
            print(f'[-] No {query} Records')

        print('\n')

def enum_subdomains():
    load='-'
    try:
        wordlist = open("./dicts/subdomains.txt", "r")
    except:
        wordlist = open("/usr/share/dns_recon/dicts/subdomains.txt", "r")

    queries = ['A', 'TXT', 'NS']
    total = wordlist.readline().replace('\n', '')
    index = 0

    print("[*] Starting subdomains search")

    for word in wordlist:
        found = False

        word = word.replace('\n', '')
        print(f"[{load}] Trying {index}/{total} {word}")
        print(bcolors.LINE_UP, end=bcolors.LINE_CLEAR)

        if load == '-': 
            load = '\\'
        elif load == '\\':
            load = '|'
        elif load == '|':
            load = '/'
        elif load == '/':
            load = '-'

        for query in queries:
            try:
                my_resolver.resolve(f'{word}.{target}', query)
                found = True
            except Exception:
                pass

        if found:
            print(f'- {word}.{target}')

        index += 1

def zone_transfer():
    print("[*] Starting zone trasnfer")

    ns_servers = []

    try:
        ns_answer = my_resolver.resolve(target, 'NS')

        for server in ns_answer:
            print(f"[+] Found NS: {server}")
            ip_answer = my_resolver.resolve(server.target, 'A')
            for ip in ip_answer:
                print(f"[+] IP for {server} is {ip}")
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(str(ip), target))
                    for host in zone:
                        print(f"[+] Found Host: {host}")
                except Exception as e:
                    print(f"[-] NS {server} refused zone transfer!")
                    continue
    except Exception:
        pass

if __name__ == "__main__":
	try:
		main(sys.argv[2:])
	except KeyboardInterrupt:
		print('\n\n/!\ Keyboard Interrupt')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
	finally:
		print('dns_recon finished in: ' + str(datetime.now() - startTime))