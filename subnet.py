#!/usr/bin/env python3
# CLI tool to determine various information
# of a given IPv4 address in CIDR format
# Developed by Marco Cetica (c) 2023 <email@marcocetica.com>
#
import sys
import ipaddress

class IP:
    """Extract various information from an IPv4 in CIDR format"""
    cidr: str = ""
    ip_addr: str = ""
    mask: str = ""
    mask_bin: str = ""
    network_prefix: str = ""
    network_bin: str = ""
    host_prefix: str = ""
    host_bin: str = ""
    usable_hosts: str = ""

    def __init__(self, cidr):
        # Check if CIDR is properly formatted
        if '/' not in cidr:
            raise ValueError("Invalid CIDR('xxx.xxx.xxx.xxx/xx')")

        # Check if IP address is valid
        ip_addr, mask = cidr.split('/')
        octets = ip_addr.split('.')
        if len(octets) != 4:
            raise ValueError("Invalid IP address")

        for v in octets:
            if int(v) > 255 or int(v) < 0:
                raise ValueError("IP address out of range")

        # Check if subnet mask is in range
        if int(mask) > 32 or int(mask) < 1:
            raise ValueError("Subnet mask out of range")

        # Otherwise set cidr
        self.cidr = cidr

    def extract_data(self) -> None:
        # Get IP and subnet mask
        self.ip_addr = self.cidr.split('/')[0]
        self.mask = ipaddress.IPv4Network(self.cidr, strict=False).netmask

        # Convert both of them to int
        network = ipaddress.IPv4Network(self.ip_addr)
        ip_addr_int = int(network.network_address)
        mask_int = int(self.mask)

        # Get network and host prefix
        network_prefix_int = (ip_addr_int & mask_int)
        host_prefix_int = (ip_addr_int & ~mask_int)

        # Convert network and host prefix back to dot notation
        self.network_prefix = str(ipaddress.IPv4Network(network_prefix_int)).split('/')[0]
        self.host_prefix = str(ipaddress.IPv4Network(int(host_prefix_int))).split('/')[0]

        # Get binary representation of ip address, mask and prefixes
        self.ip_bin = ' '.join(format(int(x), '08b') for x in self.ip_addr.split('.'))
        self.mask_bin = ' '.join(format(int(x), '08b') for x in str(self.mask).split('.'))
        self.network_bin = ' '.join(format(int(x), '08b') for x in self.network_prefix.split('.'))
        self.host_bin = ' '.join(format(int(x), '08b') for x in self.host_prefix.split('.'))

        # Compute usable hosts
        mask_complement = (~mask_int & (2 ** mask_int.bit_length() - 1))
        bit_count = bin(mask_complement).count('1')
        self.usable_hosts = (2 ** bit_count - 2) if bit_count > 0 else 0

def main():
    if len(sys.argv) < 2:
        print(f"Usage {sys.argv[0]} <CIDR>")
        sys.exit(1)

    # Get the CIRD
    cidr = sys.argv[1]

    # Extract info from IP
    try:
        ip = IP(cidr)
        ip.extract_data()
        print(f"IP Address: {ip.ip_addr} ({ip.ip_bin})")
        print(f"Subnet Mask: {ip.mask} ({ip.mask_bin})")
        print(f"Network Prefix: {ip.network_prefix} ({ip.network_bin})")
        print(f"Host Prefix: {ip.host_prefix} ({ip.host_bin})")
        print(f"Usable Hosts: {ip.usable_hosts}")
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
