cd /usr/local/lib/python2.7/dist-packages/yowsup2-2.5.2-py2.7.egg/yowsup/layers/axolotl
patch < /home/pi/Jabber/layer_receive.patch
cd /usr/local/lib/python2.7/dist-packages/yowsup2-2.5.2-py2.7.egg/yowsup/layers/protocol_media
patch < /home/pi/Jabber/picture.patch
cd /usr/local/lib/python2.7/dist-packages/yowsup2-2.5.2-py2.7.egg/yowsup/common/
sudo patch < /home/pi/Jabber/tools.patch
cd /usr/local/lib/python2.7/dist-packages/yowsup2-2.5.2-py2.7.egg/yowsup//layers/axolotl/
sudo patch < /home/pi/Jabber/layer_send.patch
cd /usr/local/lib/python2.7/dist-packages/yowsup2-2.5.2-py2.7.egg/yowsup/layers/protocol_media/
sudo patch < /home/pi/Jabber/mediauploader.patch
cd /usr/local/lib/python2.7/dist-packages/yowsup2-2.5.2-py2.7.egg/yowsup/layers/protocol_media/protocolentities/

sudo patch < /home/pi/Jabber/iq_requestupload.patch
sudo patch < /home/pi/Jabber/iq_requestupload_result.patch
sudo patch < /home/pi/Jabber/message_media.patch
sudo patch < /home/pi/Jabber/message_media_downloadable.patch
sudo patch < /home/pi/Jabber/message_media_downloadable_image.patch

cd /usr/local/lib/python2.7/dist-packages/yowsup2-2.5.2-py2.7.egg/yowsup/layers/protocol_messages/proto/
sudo patch < /home/pi/Jabber/wa_pb2.patch
