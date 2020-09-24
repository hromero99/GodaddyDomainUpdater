from dotenv import load_dotenv
import os 
import requests
import json
import logging

logging.basicConfig(level=logging.INFO,filename="domainUpdater.log")


def get_current_local_ip() -> str:
    r = requests.get(url='https://ifconfig.me')
    if r.status_code == 200:
        logging.info(f"Current ip {r.text}")
        return r.text
    logging.error(f"Error Making request {r.status_code}")


def update_godaddy_a_register(ip: str, domain: str) -> int:
    data_dict = {
            "data": ip,
            "port": 80,
            "priority": 0,
            "ttl": 3600,
            "weight": 1,
            "protocol": "none",
            "service": "none",
    }
    
    r = requests.put(
        url=f'https://api.godaddy.com/v1/domains/{domain.upper()}/records/A/%40',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"sso-key {os.environ.get('KEY')}:{os.environ.get('SECRET')}",
            "accept": "application/json"
        },
        data=json.dumps([data_dict])
    )
    if r.status_code == 200:
        logging.info(f"{domain}'s IP has been updated to {ip}")
    else:
        logging.error(f"Error {r.status_code} updating {domain}'s IP")
    
    return r.status_code


def verify_change_ip(currentIp: str, domain: str) -> int:
    r = requests.get(
        url=f'https://api.godaddy.com/v1/domains/{domain.upper()}/records/A/%40',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"sso-key {os.environ.get('KEY')}:{os.environ.get('SECRET')}",
            "accept": "application/json"
        }
    )
    if r.status_code == 200:
        body = json.loads(r.text)
        if currentIp == body[0].get("data"):
            return -1
        else:
            return 0
    return r.status_code


if __name__ == "__main__":
    load_dotenv()
    ip = get_current_local_ip()
    domain = os.environ.get("DOMAIN")
    if (os.environ.get("KEY") == "") or (os.environ.get("SECRET") == "") or (domain == ""):
        print("You must set SECRET, KEY and DOMAIN env vars")
        exit(-1)
    if ip:
        ipChanged = verify_change_ip(ip, domain)
        if  ipChanged == 0:
            update_godaddy_a_register(ip, domain)
        elif ipChanged == -1:
            logging.info(f"Domain hromero99.club already has ip {ip}")
        else:
            logging.error(f"UnkownError {ipChanged}")
        