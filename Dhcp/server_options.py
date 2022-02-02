from enum import IntEnum


class ServerOptions(IntEnum):
    SUBNET_MASK = 1
    ROUTER = 3
    DOMAIN_SERVER = 6
    BROADCAST_ADDRESS = 28
    LEASE_TIME = 51
    SERVER_IDENTIFIER = 54
    RENEWAL_TIME = 58
