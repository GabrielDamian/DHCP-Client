from uuid import getnode


class Computer:
    @staticmethod
    def get_mac() -> str:
        """
        :return: The MAC address of the computer
        """
        return ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))