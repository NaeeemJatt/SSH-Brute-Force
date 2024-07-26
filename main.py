import ipaddress
import platform
import subprocess
from pwn import *

def is_valid_ip(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False


def ping_ip(ip_address):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = f"ping {param} 1 {ip_address}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output = stdout.decode('utf-8')
    if "unreachable" in output or "timed out" in output or process.returncode != 0:
        print(f"The IP address {ip_address} is not active.")
    else:
        print(f"The IP address {ip_address} is active.")


ip_address = input("Enter the IP address to check: ")
if is_valid_ip(ip_address):
    ping_ip(ip_address)
else:
    print(f"The IP address {ip_address} is not valid.")
