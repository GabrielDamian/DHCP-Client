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

    def give_address(self, address: IPv4Address, mac: str, client_id: str, lease: datetime):
        self._table[address][0] = mac
        self._table[address][1] = client_id
        self._table[address][2] = lease

    def get_mac(self, address: IPv4Address) -> Optional[str]:
        return self._table[address][0]

    def get_client_identifier(self, address: IPv4Address) -> Optional[str]:
        return self._table[address][1]

    def get_lease(self, address: IPv4Address) -> Optional[datetime]:
        return self._table[address][2]

    def is_used(self, address: IPv4Address) -> Optional[bool]:
        return bool(self._table[address][3])
