from datetime import datetime
from typing import Dict, Optional, List
from ipaddress import IPv4Address, IPv4Network


class AddressTable:
    def __init__(self, network_address: IPv4Network):
        """
        :param network_address: network address to manage
        """
        self._network_address = network_address
        # ip_address: MAC, client_id, lease, is_used
        self._table: Dict[IPv4Address, List[Optional[str], Optional[str], Optional[datetime], Optional[bool]]] = {}
        for address in self._network_address:
            self._table[address] = [None, None, None, False]

    def get_unallocated_address(self) -> Optional[IPv4Address]:
        """
        :return: IPv4Address from network that is not used, or None if there are no free addresses
        """
        for address in list(self._table.keys())[1:-1]:
            if not self.is_used(address):
                return address
        return None

    def give_address(self, address: IPv4Address, mac: str, client_id: str, lease: datetime):
        """
        Mark an ip address as taken.
        :param address: address to mark
        :param mac: mac address associated with the ip address
        :param client_id: client id associated with the ip address
        :param lease: lease associated with the ip address
        :return: None if the address is already used 1 otherwise
        """
        if self.is_used(address):
            return None
        else:
            self._table[address][0] = mac
            self._table[address][1] = client_id
            self._table[address][2] = lease
            self._table[address][3] = True
            return 1

    def release_address(self, address: IPv4Address):
        """
        Frees an is address
        :param address: The address to free
        """
        if address in self._table.keys() and self.is_used(address):
            self._table[address][0] = None
            self._table[address][1] = None
            self._table[address][2] = None
            self._table[address][3] = False

    def get_mac(self, address: IPv4Address) -> Optional[str]:
        """
        :return: MAC address associated with the ip address or None if address not in table
        """
        if address in self._table.keys():
            return self._table[address][0]
        else:
            return None

    def get_client_identifier(self, address: IPv4Address) -> Optional[str]:
        """
        :return:  client identifier associated with the ip address or None if address not in table
        """
        if address in self._table.keys():
            return self._table[address][1]
        else:
            return None

    def get_lease(self, address: IPv4Address) -> Optional[datetime]:
        """
        :return: datetime set on the time when lease expires or None if address not in table
        """
        if address in self._table.keys():
            return self._table[address][2]
        else:
            return None

    def is_used(self, address: IPv4Address) -> Optional[bool]:
        """
        :return: 1->address used; 2->address not used; None->address not in table
        """
        if address in self._table.keys():
            return bool(self._table[address][3])
        else:
            return None

    def clear(self):
        """Releases all addresses"""
        for address in self._table.keys():
            if self.is_used(address):
                self.release_address(address)

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
