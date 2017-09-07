# -*- coding: utf-8 -*-
import os, subprocess, time

from yowsup.layers.interface                           import YowInterfaceLayer                 #Reply to the message
from yowsup.layers.interface                           import ProtocolEntityCallback            #Reply to the message
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity   #Online
from yowsup.layers.protocol_presence.protocolentities  import UnavailablePresenceProtocolEntity #Offline
from yowsup.layers.protocol_presence.protocolentities  import PresenceProtocolEntity            #Name presence
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity   #is writing, writing pause
from yowsup.common.tools                               import Jid                               #is writing, writing pause

allowedPersons=['6583747967'] #Filter the senders numbers
ap = set(allowedPersons)

name = "NAMEPRESENCE"
filelog = "/home/pi/yowsup/Not allowed.log"

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack()) #Set received (double v)
            time.sleep(0.5)
            self.toLower(PresenceProtocolEntity(name = name)) #Set name Presence
            time.sleep(0.5)
            self.toLower(AvailablePresenceProtocolEntity()) #Set online
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack(True)) #Set read (double v blue)
            time.sleep(0.5)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set is writing
            time.sleep(2)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set no is writing
            time.sleep(1)
            self.onTextMessage(messageProtocolEntity) #Send the answer
            time.sleep(3)
            self.toLower(UnavailablePresenceProtocolEntity()) #Set offline

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print entity.ack()
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        namemitt   = messageProtocolEntity.getNotify()
        message    = messageProtocolEntity.getBody().lower()
        recipient  = messageProtocolEntity.getFrom()
        textmsg    = TextMessageProtocolEntity

        #For a break to use the character \n
        #The sleep you write so #time.sleep(1)

        if messageProtocolEntity.getFrom(True) in ap:
            if message == 'Hi':
                answer = "Hi "+namemitt+" " 
                self.toLower(textmsg(answer, to = recipient ))
                print answer

            elif message == 'sends the list':
                answer = "Hi "+namemitt+"\n\nYou can ask me these things:\n\nTemperature\nRestart\nOn GPIO14\nOff GPIO14"
                self.toLower(textmsg(answer, to = recipient ))
                print answer

            elif message == 'temperature':
                t=float(subprocess.check_output(["/opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell=True)[:-1])
                ts=str(t)
                answer = 'My temperature is '+ts+' °C'
                self.toLower(textmsg(answer, to = recipient ))
                print answer

            elif message == 'restart':
                answer = "Ok "+namemitt+", rebooting. Bye bye."
                self.toLower(textmsg(answer, to = recipient ))
                print answer
                time.sleep(3)
                self.toLower(UnavailablePresenceProtocolEntity())
                time.sleep(2)
                os.system('reboot')

           
            else:
                answer = "Sorry "+namemitt+", I can not understand what you're asking me.." 
                self.toLower(textmsg(answer, to = recipient))
                print answer

        else:
            answer = "Hi "+namemitt+", I'm sorry, I do not want to be rude, but I can not chat with you.."
            time.sleep(20)
            self.toLower(textmsg(answer, to = recipient))
            print answer
           # out_file = open(filelog,"a")
           # out_file.write("------------------------"+"\n"+"Sender:"+"\n"+namemitt+"\n"+"Number sender:"+"\n"+recipient+"\n"+"Message text:"+"\n"+message+"\n"+"------------------------"+"\n"+"\n")
           # out_file.close()
