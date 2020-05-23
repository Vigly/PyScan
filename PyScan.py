import socket
import sys
import threading
import time
from queue import Queue

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
            print("[+]", port)

        connection.close()
    except:
        pass

def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

q = Queue()

#Use 100 threads
for x in range(100):
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

#Port scan range
for worker in range(1, 65535):
    q.put(worker)

q.join()

#Gets current time after scan runs
time2 = time.time()

#Solve the time difference
total_time = time2 - time1

print("\nScan complete for", remote_ip, "in {:0.2f}".format(total_time), "seconds")