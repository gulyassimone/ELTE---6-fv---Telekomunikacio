import  subprocess
from datetime import datetime
import platform
import json
import threading
import sys

a_file = open(sys.argv[1], "r")
lines = a_file.readlines()
last_lines = lines[-10:]
first_lines = lines[:10]

pings = []
traces = []
threads = []

def thread_pings(webpage, command, list):
    if(command == "ping"):
        p = subprocess.Popen(["ping", "-n", "10", webpage], stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(["tracert", "-h", "30", webpage], stdout=subprocess.PIPE)
    std2_out, std2_err = p.communicate()
    s2 = std2_out.decode(('utf-8'))
    list.append({"target": webpage, "output": s2.rstrip()})


for line in last_lines + first_lines:
     key = line.rstrip().split(',')[1];
     t = threading.Thread(target=thread_pings, args=(key,"ping",pings,))
     threads.append(t)
     k = threading.Thread(target=thread_pings, args=(key,"traces",traces,))
     threads.append(k)

     k.start()
     t.start()

for t in threads:
     t.join() #összevárja a szálakat

ping_dictionary = {"date": datetime.now().strftime("%Y%m%d"), "system": platform.platform().split('-')[0].lower(), "pings": pings}
traceroute_dictionary = {"date": datetime.now().strftime("%Y%m%d"), "system": platform.platform().split('-')[0].lower(), "traces": traces}

with open("ping.json", "w") as out_file:
    json.dump(ping_dictionary, out_file, indent=2, sort_keys=True)
with open("traceroute.json", "w") as out_file:
    json.dump(traceroute_dictionary, out_file, indent=2, sort_keys=True)