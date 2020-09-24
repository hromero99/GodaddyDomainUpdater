import requests
import os
from main import logger
import json


class GodaddyApi(object):
    def __init__(self):
        self.key = os.get_exec_path("KEY")
        self.secret = os.getenv("SECRET")

    def update_godaddy_a_register(self, ip: str, domain: str) -> int:
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
                "Authorization": f"sso-key {self.key}:{self.secret}",
                "accept": "application/json"
            },
            data=json.dumps([data_dict])
        )
        if r.status_code == 200:
            logger.info(f"{domain}'s IP has been updated to {ip}")
        else:
            logger.error(f"Error {r.status_code} updating {domain}'s IP")
        return r.status_code

    def verify_change_ip(self, currentIp: str, domain: str) -> int:
        r = requests.get(
            url=f'https://api.godaddy.com/v1/domains/{domain.upper()}/records/A/%40',
            headers={
                "Content-Type": "application/json",
                "Authorization": f"sso-key {self.key}:{self.secret}",
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
