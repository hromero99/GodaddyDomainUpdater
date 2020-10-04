#!/usr/bin/env python3
from dotenv import load_dotenv
import requests
import logging
import argparse
from domain import Domain

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO, filename="domainUpdater.log")


def get_current_local_ip() -> str:
    r = requests.get(url='https://ifconfig.me')
    if r.status_code == 200:
        logging.info(f"Current ip {r.text}")
        return r.text
    logging.error(f"Error Making request {r.status_code}")


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Update information about domain in Goddady web")
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-c", "--createSubdomain", help="Create given domain if not exits", action='store_true')
    optional.add_argument("-u", "--update", help="Update A register of given Domain to given Ip", action='store_true')
    required.add_argument("--domain", action="store", help="Domain to perform operations", required=True)
    required.add_argument("--ip", action="store", help="Ip Address to update information of DNS A register", required=True)
    optional.add_argument("--subdomain", action="store", help="Ip Address to update information of DNS A register")
    arguments = parser.parse_args()
    domain = Domain(domain_name=arguments.domain)

    if arguments.createSubdomain:
        domain.create_subdomain(subdomain_name=arguments.subdomain, ip_address=arguments.ip)

    if arguments.update:
        domain.update_register(register_name="@", register_new_value=arguments.ip, register_type="A")

