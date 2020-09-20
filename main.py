from dotenv import load_dotenv
import os 
import requests
import json


def getMyCurrentIP() -> str:
    r = requests.get(url='https://ifconfig.me')
    if r.status_code == 200:
        return r.text
    Exception(f"Error Making request {r.status_code}")


def updateGoDaddyIpDomain(ip: str, domain: str) -> int:
    data_dict = {
            "data":ip,
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
    return r.status_code

def verifyChangeIP(currentIp:str, domain: str) -> int:
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
    ip = getMyCurrentIP()
    if ip:
        ipChanged = verifyChangeIP(ip,"hromero99.club")
        if  ipChanged == 0:
            updateGoDaddyIpDomain(ip,"hromero99.club")
        elif ipChanged == -1:
            print(f"Domain hromero99.club already has ip {ip}")
        else:
            print(f"UnkownError {ipChanged}")
        