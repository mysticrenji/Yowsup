import os, subprocess, yowsup, logging

from wasend
import YowsupSendStack
from wareceive
import YowsupReceiveStack, MessageReceived

def credential():
    return "919061957981", "Pu4gJ//+L445+SHVZ9WbQ2HOUjQ="

def Answer(risp):
    try:
    stack = YowsupSendStack(credential(), [(["919061957981", risp])])
stack.start()
except: pass
return

def Refresh():
    Answer("Refreshing the repos.")
os.system("sudo apt-get -y update")
Answer("Repos updated.")
return

def Restart():
    Answer("Rebooting")
os.system("sudo reboot")
return

def Temp():
    t = float(subprocess.check_output(["/opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell = True)[: -1])
ts = str(t)
Answer("My temperature is " + ts + " C")
return

def Disk():
    result = subprocess.check_output("df -h .", shell = True)
output = result.split()
Answer("Disk space:\nTotal: " + output[8] + "\nUsed: " + output[9] + " (" + output[11] + ")\nFree: " + output[10])
return
while True:
    try:
    stack = YowsupReceiveStack(credential())
stack.start()
except MessageReceived as rcvd:
    received = rcvd.value.lower()
if received[: len("6583747967")] == "6583747967":
    received = received[len("6583747967"): ]
if received[: 4] == "hiya": Answer("Hi chap!")
elif received[: 7] == "restart"
or received[: 6] == "reboot": Restart()
elif "disk" in received: Disk()
elif "hot" in received: Temp()
elif "refresh" in received: Refresh()
else :Answer("Eh? What was that?")
else :#message from wrong sender
with open("/home/pi/whatsapp.log", "a") as mf: mf.write("Unauthorised access from: " + received[: len("6586723603")] + "\n")
