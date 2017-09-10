#sudo apt-get install libxml-parser-perl libauthen-sasl-perl
#sudo apt-get install sendxmpp
#!/bin/bash


# This all needs to be run as root.
sudo apt-get update
# Always update before installing new stuff.
sudo apt-get install perl
sudo apt-get install libxml-parser-perl libauthen-sasl-perl

# Pi may tell you about some packages that are no longer needed and can be removed with sudo apt-get autoremove. I don’t think it hurts anything to remove them (I did) but do so at your peril.

sudo apt-get install libnet-xmpp-perl

# Original author has you building the package. Git isn’t there by default, and someone has already compiled a Pi package for you

sudo apt-get install sendxmpp

# We’re done installing packages

echo "mytalkaccount@jabber.org mypassword" >> ~/.sendxmpprc
chmod 700 ~/.sendxmpprc
sudo cp -v ~/.sendxmpprc /etc/sendxmpprc
