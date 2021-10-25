import subprocess
import optparse
import re


def get_mac(interface):
    ifconfig_output =subprocess.check_output(["ifconfig",interface], text=True)
    results = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)
    return results.group(0)

def parser_func():
    parser = optparse.OptionParser(
        "Usage: python3 macchanger.py -m 00:11:22:33:44:55 -i eth0, --help to display help menu")
    parser.add_option('-m', dest="new_mac", help="Set the mac")
    parser.add_option('-i', dest="interface", help="Set the interface")
    values, keys = parser.parse_args()
    if values.new_mac and values.interface:
        return values
    else:
        print(parser.usage)
        exit(1)


def change_mac(values):
    new_mac = values.new_mac
    interface = values.interface
    subprocess.call(f'sudo ifconfig {interface} down', shell=True)
    subprocess.call(f'sudo ifconfig {interface} hw ether {new_mac}', shell=True)
    subprocess.call(f'sudo ifconfig {interface} up', shell=True)

values = parser_func()
print("old MAC: " + get_mac(values.interface))
change_mac(values)
print("new MAC: " + get_mac(values.interface))

