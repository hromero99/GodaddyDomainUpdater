from dotenv import load_dotenv
import os 
import requests
import logging
from api import GodaddyApi

logger = logging.basicConfig(level=logging.INFO,filename="domainUpdater.log")


def get_current_local_ip() -> str:
    r = requests.get(url='https://ifconfig.me')
    if r.status_code == 200:
        logging.info(f"Current ip {r.text}")
        return r.text
    logging.error(f"Error Making request {r.status_code}")


if __name__ == "__main__":
    load_dotenv()
    ip = get_current_local_ip()
    domain = os.environ.get("DOMAIN")
    api_controller = GodaddyApi()
    if (os.environ.get("KEY") == "") or (os.environ.get("SECRET") == "") or (domain == ""):
        print("You must set SECRET, KEY and DOMAIN env vars")
        exit(-1)
    if ip:
        ipChanged = api_controller.verify_change_ip(ip, domain)
        if ipChanged == 0:
            api_controller.update_godaddy_a_register(ip, domain)
        elif ipChanged == -1:
            logging.info(f"Domain hromero99.club already has ip {ip}")
        else:
            logging.error(f"UnkownError {ipChanged}")
