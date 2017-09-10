# -*- coding: utf-8 -*-
import os, subprocess, time

#import RPi.GPIO as GPIO

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(14, GPIO.OUT)
from picamera import PiCamera
from yowsup.layers.interface                           import YowInterfaceLayer                 #Reply to the message
from yowsup.layers.interface                           import ProtocolEntityCallback            #Reply to the message
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity   #Online
from yowsup.layers.protocol_presence.protocolentities  import UnavailablePresenceProtocolEntity #Offline
from yowsup.layers.protocol_presence.protocolentities  import PresenceProtocolEntity            #Name presence
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity   #is writing, writing pause
from yowsup.common.tools                               import Jid                               #is writing, writing pause


from yowsup.layers.protocol_media.protocolentities     import *
from yowsup.layers.protocol_media.mediauploader        import MediaUploader

from yowsup.layers.protocol_media.picture              import YowMediaPictureLayer              #descarga imagen
from yowsup.layers.protocol_media.mediadownloader      import MediaDownloader                   #descarga imagen
import sys, shutil, logging, mimetypes


#Log, but only creates the file and writes only if you kill by hand from the console (CTRL + C)
#import sys
#class Logger(object):
#    def __init__(self, filename="Default.log"):
#        self.terminal = sys.stdout
#        self.log = open(filename, "a")
#
#    def write(self, message):
#        self.terminal.write(message)
#        self.log.write(message)
#sys.stdout = Logger("/1.txt")
#print "Hello world !" # this is should be saved in yourlogfilename.txt
#------------#------------#------------#------------#------------#------------
logger = logging.getLogger(__name__)
allowedPersons=['65','65'] #Filter the senders numbers
ap = set(allowedPersons)

name = "NAMEPRESENCE"
filelog = "/home/pi/.yowsup/Not allowed.log"

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.5)
        elif messageProtocolEntity.getType() == 'media':
            time.sleep(0.5)
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

    #def onMediaMessage(self, messageProtocolEntity):
    #    if messageProtocolEntity.getMediaType() == "image":
    #        url = messageProtocolEntity.url
    #        self.extension = self.getExtension(messageProtocolEntity.getMimeType())
    #        return self.downloadMedia(url)
	
    def getMediaMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getMediaType() in ("image", "audio", "video", "document"):
            return self.getDownloadableMediaMessageBody(messageProtocolEntity)
        else:
            return "[Media Type: %s] %s" % (messageProtocolEntity.getMediaType(), messageProtocolEntity)

    def getDownloadableMediaMessageBody(self, messageProtocolEntity):
	self.extension = self.getExtension(messageProtocolEntity.getMimeType())
	self.url = messageProtocolEntity.getMediaUrl()
	self.mediaKey = messageProtocolEntity.mediaKey
	self.cryptKeys = getcryptKeys(messageProtocolEntity.getMediaType())
        #filename = "%s/%s%s"%(tempfile.gettempdir(),messageProtocolEntity.getId(),messageProtocolEntity.getExtension())
        filename = "%s/%s%s"%('/home/pi/yowsup/Jabber/Downloads',messageProtocolEntity.getId(),self.extension)
        with open(filename, 'wb') as f:
            #f.write(messageProtocolEntity.getMediaContent())
            f.write(self.getMediaContent(self.url))
        #return "[Media Type:{media_type}, Size:{media_size}, URL:{media_url}, FILE:{fname}]".format(
        return "{fname}".format(
            media_type=messageProtocolEntity.getMediaType(),
            media_size=messageProtocolEntity.getMediaSize(),
            media_url=messageProtocolEntity.getMediaUrl(),
            fname=filename
        )

    def decrypt(self, encimg, refkey):
        #derivative = HKDFv3().deriveSecrets(refkey, binascii.unhexlify("None"), 112)
        derivative = HKDFv3().deriveSecrets(refkey, binascii.unhexlify(self.cryptKeys), 112)
        parts = ByteUtil.split(derivative, 16, 32)
        iv = parts[0]
        cipherKey = parts[1]
        e_img = encimg[:-10]
        AES.key_size=128
        cr_obj = AES.new(key=cipherKey,mode=AES.MODE_CBC,IV=iv)
        return cr_obj.decrypt(e_img)

    def isEncrypted(self):
        return self.cryptKeys and self.mediaKey

    def getMediaContent(self,url):
        data = urlopen(self.url).read()
        if self.isEncrypted():
            data = self.decrypt(data, self.mediaKey)
        return bytearray(data)

    def getcryptKeys(self, mediaType):
	if mediaType == "image":
	    #self.cryptKeys = '576861747341707020496d616765204b657973'
	    return "576861747341707020496d616765204b657973"
	elif mediaType == "audio":
	    #self.cryptKeys = '576861747341707020417564696f204b657973'
	    return "576861747341707020417564696f204b657973"	
        elif mediaType == "video":
	    #self.cryptKeys = '576861747341707020566964656f204b657973'
	    return "576861747341707020566964656f204b657973"
	elif mediaType == "document":
	    #self.cryptKeys = '576861747341707020446f63756d656e74204b657973'
	    return "576861747341707020446f63756d656e74204b657973"
	return "None"

    def downloadMedia(self, url):
        print("Downloading %s" % url)
        downloader = MediaDownloader(self.onSuccess, self.onError, self.onProgress)
        downloader.download(url)

    def onError(self):
        logger.error("Error download file")

    def onSuccess(self, path):
        outPath = "/root/%s%s" % (os.path.basename(path), self.extension)
        shutil.copyfile(path, outPath)
        print("\nPicture downloaded to %s" % outPath)

    def onProgress(self, progress):
        sys.stdout.write("Download progress => %d%% \r" % progress)
        sys.stdout.flush()

    def getExtension(self, mimetype):
        type = mimetypes.guess_extension(mimetype.split(';')[0])
        if type is None:
            raise Exception("Unsupported/unrecognized mimetype: "+mimetype);
        return type

    #def image_send(self, number, path, caption = None):
       # jid = number
       # mediaType = "image"
      #  entity = RequestUploadIqProtocolEntity(mediaType, filePath = path)
        #successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, mediaType, path, successEntity, originalEntity, caption)
      #  errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)
     #   self._sendIq(entity, successFn, errorFn)

    def doSendMedia(self, mediaType, filePath, url, to, ip = None, caption = None):
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        self.toLower(entity)

    def onRequestUploadResult(self, jid, mediaType, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, caption = None):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendMedia(mediaType, filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp(), caption)
        else:
            successFn = lambda filePath, jid, url: self.doSendMedia(mediaType, filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
            resultRequestUploadIqProtocolEntity.getUrl(),
            resultRequestUploadIqProtocolEntity.getResumeOffset(),
            successFn, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        logger.error("Request upload for file %s for %s failed" % (path, jid))

    def onUploadError(self, filePath, jid, url):
        logger.error("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()
		
    def image_send(self, number, path, caption = None):
        jid = number
        mediaType = "image"
        entity = RequestUploadIqProtocolEntity(mediaType, filePath = path)
        successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, mediaType, path, successEntity, originalEntity, caption)
        errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)
        self._sendIq(entity, successFn, errorFn)

    def doSendMedia(self, mediaType, filePath, url, to, ip = None, caption = None):
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        self.toLower(entity)

    def onRequestUploadResult(self, jid, mediaType, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, caption = None):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendMedia(mediaType, filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp(), caption)
        else:
            successFn = lambda filePath, jid, url: self.doSendMedia(mediaType, filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        logger.error("Request upload for file %s for %s failed" % (path, jid))

    def onUploadError(self, filePath, jid, url):
        logger.error("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()

    def onTextMessage(self,messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            message    = messageProtocolEntity.getBody().lower()
        elif messageProtocolEntity.getType() == 'media':
            message    = messageProtocolEntity.getMediaType()
        namemitt   = messageProtocolEntity.getNotify()
        recipient  = messageProtocolEntity.getFrom()
        textmsg    = TextMessageProtocolEntity

        #For a break to use the character \n
        #The sleep you write so #time.sleep(1)

        if messageProtocolEntity.getFrom(False) in ap:
            if message == 'hi':
                answer = "Hi "+namemitt+" " 
                self.toLower(textmsg(answer, to = recipient ))
                print answer
              
            elif message == 'send the list':
                answer = "Hi "+namemitt+"\n\nYou can ask me these things:\n\nTemperature\nRestart\nSend image\nSend position\nOn GPIO14\nOff GPIO14"
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

            elif message == 'send image':
                answer = "Hi "+namemitt+", here is the picture you asked me." 
                self.toLower(textmsg(answer, to = recipient ))
                print answer
                path = "/home/pi/Jabber/Images/Image.jpg"
                self.image_send(recipient, path)

	    elif message == 'raspberry':
                answer = "Hi "+namemitt+", here is the the real time pic you requested."  
		self.toLower(textmsg(answer, to = recipient ))
		print answer
		camera = PiCamera()
		imageLocation="/home/pi/Jabber/Images/Image.jpg"
		camera.capture(imageLocation)
		time.sleep(5)
		self.image_send(recipient, path)
				
            elif message == 'send position':
                answer = "Hi "+namemitt+", here is the position you asked me." 
                self.toLower(textmsg(answer, to = recipient ))
                print answer
                latitude="28.3744278" # from -90 to 90, positive means north and negative means south
                longitude="-81.5494113" # from -180 to 180, positive means east and negative means west
                locationName="Epcot\n200 Epcot Center DR, Orlando FL" # optional, the first line will become a clickable link, the second won't
                locationURL="disneyworld.disney.go.com" # optional, this is the link you'll be redirected when you click the locationName
                locationEncoding="raw"
                outLocation = (LocationMediaMessageProtocolEntity(latitude, longitude, locationName, locationURL, locationEncoding, to = recipient ))
                self.toLower(outLocation)

           # elif message == 'on gpio14':
            #    GPIO.output(14, True) # Pin 2 in up
            #    answer = "Ok, il GPIO14 è su true"
            #    self.toLower(textmsg(answer, to = recipient ))
            #    print answer

            #elif message == 'off gpio14':
             #   GPIO.output(14, False) # Pin 2 in down
              #  answer = "Ok, il GPIO14 è su false"
                #self.toLower(textmsg(answer, to = recipient ))
               # print answer

            #elif messageProtocolEntity.getMediaType() == "image":
            #    print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            #    answer = "Hi "+namemitt+", thank you for sending me your picture."
            #    self.toLower(textmsg(answer, to = recipient ))
            #    self.onMediaMessage(messageProtocolEntity)
            #    print answer

            #elif messageProtocolEntity.getMediaType() == "location":
             #   print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))
            #    answer = "Hi "+namemitt+", thank you for sending me your geolocation."
             #   self.toLower(textmsg(answer, to = recipient ))
             #   print answer

            #elif messageProtocolEntity.getMediaType() == "vcard":
            #    print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
            #    answer = "Hi "+namemitt+", thank you for sending me your contact."
            #    self.toLower(textmsg(answer, to = recipient ))
             #   print answer

            else:
                answer = "Sorry "+namemitt+", I can not understand what you're asking me.." 
                self.toLower(textmsg(answer, to = recipient))
                print answer

        else:
            answer = "Hi "+namemitt+", I'm sorry, I do not want to be rude, but I can not chat with you.."
            time.sleep(20)
            self.toLower(textmsg(answer, to = recipient))
            print answer
            out_file = open(filelog,"a")
            out_file.write("------------------------"+"\n"+"Sender:"+"\n"+namemitt+"\n"+"Number sender:"+"\n"+recipient+"\n"+"Message text:"+"\n"+message+"\n"+"------------------------"+"\n"+"\n")
            out_file.close()
