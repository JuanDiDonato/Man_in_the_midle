import scapy.all as scapy

def scan(ip): #ip que vamos a escanear
    arp_request = scapy.ARP(pdst = ip) #¿quien tiene este ip? -> ese ip nos va a responder
    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff') #campo de MAC (DESTINO DE BUSQUEDA DE IP; su formato)
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #Recorre la subred, y pregunta a todos los conectados sus ip
    
    clients_list = []
    for element in answered_list: #muestra todos los ips conectados a la red, y sus MACs
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc} #creo un diccionario donde guardo el ip y el mac
        clients_list.append(client_dict)
    return (clients_list)

#pdst = ip --> p es ip
#hwdst = mac --> hw es mac
#psrc = ip del moden (route -n, pa)


def results(results_list):
    print("IP\t\t\tMAC address\n------------------------------------------------")
    for client in results_list:
        print(client['ip'] + '\t\t' + client['mac'])

scan_result = scan('192.168.1.1/24') #/24 para identificar a todos los usuarios en la subred
results(scan_result)