from dotenv import load_dotenv
import os 
import requests
import logging
from api import GodaddyApi
import argparse

logging.basicConfig(level=logging.INFO, filename="domainUpdater.log")


def get_current_local_ip() -> str:
    r = requests.get(url='https://ifconfig.me')
    if r.status_code == 200:
        logging.info(f"Current ip {r.text}")
        return r.text
    logging.error(f"Error Making request {r.status_code}")


if __name__ == "__main__":
    load_dotenv()
    domain = os.environ.get("DOMAIN")
    api_controller = GodaddyApi()
    parser = argparse.ArgumentParser(description="Update information about domain in Goddady web")
    parser.add_argument(dest="domain", type=str, help="Domain to perform operations")
    parser.add_argument(dest="ip", type=str, help="Ip Address to update information of DNS A register")
    parser.add_argument(dest="subdomain", type=str, help="Ip Address to update information of DNS A register")
    parser.add_argument("-c", "--createSubdomain", help="Create given domain if not exits", action='store_true')
    parser.add_argument("-u", "--update", help="Update A register of given Domain to given Ip", action='store_true')

    arguments = parser.parse_args()

    if arguments.createSubdomain:
        api_controller.create_subdomain(
            domain=arguments.domain,
            subdomain=arguments.subdomain,
            ip=arguments.ip
        )

