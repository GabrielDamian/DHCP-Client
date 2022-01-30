from datetime import datetime
from typing import Dict, Optional, List
from ipaddress import IPv4Address, IPv4Network


class AddressTable:
    def __init__(self, network_address: IPv4Network):
        # ip_address: MAC, client_id, lease, is_used

        self._network_address = network_address
        self._table: Dict[IPv4Address, List[Optional[str], Optional[str], Optional[datetime], Optional[bool]]] = {}
        for address in self._network_address:
            self._table[address] = [None, None, None, False]

    def get_unallocated_address(self) -> Optional[IPv4Address]:
        for address in list(self._table.keys())[1:-1]:
            if not self.is_used(address):
                return address
        return None

    def give_address(self, address: IPv4Address, mac: str, client_id: str, lease: datetime):
        self._table[address][0] = mac
        self._table[address][1] = client_id
        self._table[address][2] = lease
        self._table[address][3] = True

    def revoke_address(self, address: IPv4Address):
        self._table[address][0] = None
        self._table[address][1] = None
        self._table[address][2] = None
        self._table[address][3] = False

    def get_mac(self, address: IPv4Address) -> Optional[str]:
        return self._table[address][0]

    def get_client_identifier(self, address: IPv4Address) -> Optional[str]:
        return self._table[address][1]

    def get_lease(self, address: IPv4Address) -> Optional[datetime]:
        return self._table[address][2]

    def is_used(self, address: IPv4Address) -> Optional[bool]:
        return bool(self._table[address][3])

    def get_subnet_mask(self) -> str:
        return str(self._network_address.netmask)

    def __str__(self):
        output = "IP\t\t\tMAC\t\t\tClient Id\t\t\tLease Time\n"
        for address in self._table.keys():
            mac, id, lease = self.get_mac(address), self.get_client_identifier(address), self.get_lease(address)
            output += f"{address}\t\t\t"
            output += f"{mac}\t\t\t" if mac is not None else "None\t\t\t"
            output += f"{id}\t\t\t" if id is not None else "None\t\t\t"
            output += f"{lease}\n" if lease is not None else "None\n"
        return output
