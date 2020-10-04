from api import GodaddyApi
import json


class Register(object):
    def __init__(self, register_name: str, register_type:str, register_value: str, register_ttl: int):
        self.name = register_name
        self.value = register_value
        self.type = register_type
        self.ttl= register_ttl

    def __str__(self):
        return f"{self.name} -> {self.value}"


class Domain(object):

    def __init__(self, domain_name: str):
        self.name = domain_name
        self.registers = []
        self.godaddy_api = GodaddyApi()
        self._get_domain_registers()

    def _get_domain_registers(self):
        raw_registers = self.godaddy_api.get_domain_info(domain=self.name)
        if raw_registers:
            raw_registers = json.loads(raw_registers)
            for register in raw_registers:
                self.registers.append(
                    Register(
                        register_name=register["name"],
                        register_value=register["data"],
                        register_type=register["type"],
                        register_ttl=register["ttl"]
                    )
                )

    def _dump_domain_information(self):
        register_serializers = [register.__dict__ for register in self.registers]
        filename = self.name.replace(".", "-") + ".json"
        with open(filename, 'w') as domain_information:
            json.dump(register_serializers, domain_information,  ensure_ascii=False, indent=4)
            domain_information.close()

    def search_for_existing_register(self, register_name: str, register_value: str) -> list:
        for register in self.registers:
            if register.name == register_name and register.value == register_value:
                return [register]
        return []

    def add_register(self, register_name: str, type: str, register_value: str, register_ttl: int):
        self.registers.append(Register(register_name,type, register_value, register_ttl))

    def update_register(self, register_name: str, register_type: str, register_new_value: str):
        for register in self.registers:
            if register.name == register_name and register.type == register_type:
                register = register
                self.registers.remove(register)
                register.value = register_new_value
                self.registers.append(register)
        self._dump_domain_information()

    def create_subdomain(self, subdomain_name: str, ip_address: str):
        for register in self.registers:
            if register.name == subdomain_name and register.type == "A":
                self.update_register(
                    register_name=subdomain_name,
                    register_type="A",
                    register_new_value=ip_address
                )
        self.godaddy_api.create_subdomain(
            domain=self.name,
            subdomain=subdomain_name,
            ip=ip_address
        )

    def update_domain_ip(self, new_ip_address: str):
        self.godaddy_api.update_godaddy_a_register(ip=new_ip_address, domain=self.name)
        self.update_register(register_type="A", register_name="@", register_new_value=new_ip_address)
