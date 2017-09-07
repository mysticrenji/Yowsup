import os, subprocess, yowsup, logging
from wasend import YowsupSendStack
from wareceive import YowsupReceiveStack, MessageReceived

def credential():
    return "919746350493","3D215eTYTS0PtX3y6HKir/lBm3k="

def Answer(risp):
    try:
        stack=YowsupSendStack(credential(), ["390000000000", risp])
        stack.start()
    except:
        pass
    return

def UpdateFunc():
    Answer("Updating...")
    os.system("sudo apt-get -y update")
    Answer("System updated!")
    return

def RestartFunc():
    Answer("Restarting the system...")
    os.system("sudo reboot")
    return

def TempFunc():
    t=float(subprocess.check_output(["/opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell=True)[:-1])
    ts=str(t)
    Answer("My temperature is "+ts+" Degree Celsius")
    return

while True:
    try:
        stack=YowsupReceiveStack(credential())
        stack.start()
    except MessageReceived as rcvd:
        received=rcvd.value.lower()
        if received[:len("390000000000")]=="390000000000":
            received=received[len("390000000000"):]
            if received[:5]=="hello": Answer("Hello!")
            elif received[:6]=="update": UpdateFunc()
            elif received[:7]=="restart" or received[:6]=="reboot": RestartFunc()
            elif "temperature" in received: TempFunc()
            else: Answer("Sorry, I cannot understand what you are asking for...")
        else: #message from wrong sender
            with open("/home/pi/youwsup/whatsapp.log","a") as mf: mf.write("Wrong sender: "+received[:len("390000000000")]+"\n")
