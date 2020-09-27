from dotenv import load_dotenv
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
    api_controller = GodaddyApi()
    parser = argparse.ArgumentParser(description="Update information about domain in Goddady web")
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-c", "--createSubdomain", help="Create given domain if not exits", action='store_true')
    optional.add_argument("-u", "--update", help="Update A register of given Domain to given Ip", action='store_true')
    required.add_argument("--domain", action="store", help="Domain to perform operations", required=True)
    required.add_argument("--ip", action="store", help="Ip Address to update information of DNS A register", required=True)
    optional.add_argument("--subdomain", action="store", help="Ip Address to update information of DNS A register")

    arguments = parser.parse_args()

    if arguments.createSubdomain:
        api_controller.create_subdomain(
            domain=arguments.domain,
            subdomain=arguments.subdomain,
            ip=arguments.ip
        )
    if arguments.update:
        api_controller.update_godaddy_a_register(
            ip=arguments.ip,
            domain=arguments.domain
        )

