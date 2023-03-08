import ipaddress
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from dataclasses import dataclass

@dataclass
class Host:
    ip: str

    def __repr__(self):
        return f"{self.ip}"

def scan_hosts(network) -> list[Host]:
    # Generate a list of all IP addresses within the network
    network = ipaddress.IPv4Network(network)
    ip_list = [str(ip) for ip in network.hosts()]

    # Create an ARP request for each address in the list
    arp_request = ARP(pdst=ip_list)
    broadcast_ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast_ether/arp_request

    # Send the ARP request and receive the responsesz
    response, _ = srp(arp_request_broadcast, timeout=2, verbose=False)

    # Extract the host addresses from the response
    hosts = []
    for _, recv in response:
        hosts.append(Host(recv[ARP].psrc))
    return hosts

network = "192.168.116.0/24"
hosts = scan_hosts(network)
print(hosts)
