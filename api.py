import requests
import os
import json
import logging


class GodaddyApi(object):
    def __init__(self):
        self.url = "https://api.godaddy.com/v1/domains/"
        self.key = os.getenv("KEY")
        self.secret = os.getenv("SECRET")
        if (os.environ.get("KEY") == "") or (os.environ.get("SECRET") == ""):
            Exception("You must set SECRET, KEY and DOMAIN env vars")
            exit(-1)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"sso-key {self.key}:{self.secret}",
            "accept": "application/json"
        }

    def update_godaddy_a_register(self, ip: str, domain: str) -> int:
        # Update A register from domain for given ip
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
            url=f'{self.url}{domain.upper()}/records/A/%40',
            headers={
                "Content-Type": "application/json",
                "Authorization": f"sso-key {self.key}:{self.secret}",
                "accept": "application/json"
            },
            data=json.dumps([data_dict])
        )
        if r.status_code == 200:
            logging.info(f"{domain}'s IP has been updated to {ip}")
        else:
            logging.error(f"Error {r.status_code} updating {domain}'s IP")
        return r.status_code

    def verify_change_ip(self, current_ip: str, domain: str) -> int:
        r = requests.get(
            url=f'https://api.godaddy.com/v1/domains/{domain.upper()}/records/A/%40',
            headers=self.headers
        )
        if r.status_code == 200:
            body = json.loads(r.text)
            if current_ip == body[0].get("data"):
                return -1
            else:
                return 0
        return r.status_code

    def create_subdomain(self, domain: str, subdomain: str, ip: str):
        # Create A register inside Given domain to create a new subdomain
        data_dict = {
            "type": 'A',
            "name": subdomain,
            "data": ip,
            "ttl": 3600,
        }
        r = requests.patch(
            url=f"{self.url}{domain.upper()}/records",
            headers=self.headers,
            data=json.dumps([data_dict])
        )
        if r.status_code == 200:
            logging.info(f"Created subdomain {subdomain} for domain {domain} with ip {ip}")
        else:
            logging.error(f"Error creating subdomain {subdomain} {r.text}")

    def get_domain_info(self, domain: str):
        r = requests.get(
            url=f"{self.url}/{domain}/records",
            headers=self.headers
        )
        if r.status_code != 200:
            return None
        else:
            return r.text