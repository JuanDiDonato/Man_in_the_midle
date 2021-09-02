import subprocess #permite correr comandos
import optparse #crea comandos para nuestro programa
import re #expresiones regulares

def get_arguments():

    #creo comandos
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest = 'interface', help= 'interface a la que le cambiara la direccion MAC') #creo el comando, y a lo que hace referencia
    parser.add_option('-m', '--mac', dest = 'new_mac', help= 'Nueva direccion MAC')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Por favor indique una interfaz. Para ayuda use --help')
    elif not options.new_mac:
        parser.error('[-] Por favor indique una direccion MAC. Para ayuda use --help')  
    return options

def change_mac(interface, new_mac):
    print("[+] Cambiando direccion MAC para " + interface )
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])

def get_current_MAC(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', options.interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w" , ifconfig_result.decode()) #Busca en ifconfig_result, el valor de ether

    if mac_address_search_result:
        return mac_address_search_result.group(0) #Group obtiene el primer resultado
    else:
        print('[-] No pudimos leer la direccion MAC')


options = get_arguments()

current_mac = get_current_MAC(options.interface)
print('Current MAC: ' + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_MAC(options.interface)
if current_mac == options.new_mac:
    print('[+] MAC cambio correctamente a ' + str(current_mac))
else:
    print('[-] No se cambio la direccion MAC')
