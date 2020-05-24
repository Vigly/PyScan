import socket
import sys
import threading
import time
import requests
import urllib3
from queue import Queue

urllib3.disable_warnings()

open_ports = []

#Sets socket lockout time for port status accuracy
socket.setdefaulttimeout(0.55)

#Lock thread during port print statement
print_lock = threading.Lock()

#Parameters
remote_ip = sys.argv[1]

#Gets current time before scan runs
time1 = time.time()

print("The following ports are open on", remote_ip)

#Range of ports being scanned
def portscan(port):  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection = sock.connect((remote_ip, port))

        with print_lock:
            open_ports.append(port)

        connection.close()
    except:
        pass

def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

q = Queue()

#Use 200 threads
for x in range(200):
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

#Port scan range
for worker in range(1, 65535):
    q.put(worker)

q.join()

#Enumerate known open ports
for port in open_ports:
    if (port == 22):
        s = socket.socket()
        s.connect((remote_ip, port))
        data = s.recv(1024)
        s.close()
        banner = data.decode('utf-8')
        print("[+] 22:", banner.rstrip())
        open_ports.remove(port)
    if (port == 80):
        url = "http://" + remote_ip
        r = requests.head(url)
        print("[+] 80:", r.headers['Server'])
        open_ports.remove(port)
    if (port == 443):
        url = "https://" + remote_ip
        r = requests.head(url, verify=False)
        print("[+] 443:", r.headers['Server'])
        open_ports.remove(port)

print("\nOpen ports that need manual enumeration:")
print(*open_ports, sep = "\n")

#Gets current time after scan runs
time2 = time.time()

#Solve the time difference
total_time = time2 - time1

print("\nScan complete for", remote_ip, "in {:0.2f}".format(total_time), "seconds")