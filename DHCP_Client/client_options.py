from enum import IntEnum


class ClientOptions(IntEnum):
    PAD = 0
    HOST_NAME = 12
    ADDRESS_REQUEST = 50
    DHCP_MESSAGE_TYPE = 53
    CLIENT_ID = 61
    END = 255