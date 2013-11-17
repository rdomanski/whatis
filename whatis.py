#!/usr/bin/env python
# 
# whatis server
#
# Author: Radek Domanski
# email: radek.domanski # gmail.com
# website: intothebug.com

import asyncore
import socket
import subprocess
import ConfigParser
import re

class WhatisHandler(asyncore.dispatcher_with_send):

    def verifyIP(self, ip):
	return re.match("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",ip)
    
    def getData(self, plugin, ip):

	config.read('whatis.conf')

	try:
	    # get the name of the script that must be executed
	    script = config.get(plugin, 'script')
	except Exception, e:
	    print "Error: %s" % e
	    return plugin + ": Not recognized plugin name"

	# location of the script to execute
	script = PLUGINS_DIR.strip('"')+script.strip('"')

	try:
	    # execute the script and get results
	    x = subprocess.check_output([script,ip])
	except Exception, e:
	    print "Error: %s" % e
	
	# return data
	return plugin + ': \n' + x

    def handle_read(self):
        data = self.recv(1024)
        if data:
	    response = ''

	    # ip must at the end of the input
	    ip = data.split(':')[-1].strip()

	    # syntax check for received input
	    if self.verifyIP(ip) is None:
		response = "IP syntax error"
	    else:
		for plugin in data.split(':'):
		    # if received plugin name is registered in configuration then invoke corresponfing plugin
		    if plugin.upper() in pluginList:
			response += str(self.getData(plugin.upper(), ip))
            
	    self.sendall(response)
	    self.close()

class WhatisServer(asyncore.dispatcher):


    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
	try:
	    self.bind((host, port))
	    self.listen(5)
	except Exception, e:
	    print "Error: %s" % e

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'connected %s' % repr(addr)
            handler = WhatisHandler(sock)


if __name__ == "__main__":
    config = ConfigParser.SafeConfigParser()
    config.read('whatis.conf')

    # retrieve configuration variables
    try:
	PORT = int(config.get('server', 'port'))
	IP = config.get('server', 'listen_ip')
	PLUGINS_DIR = config.get('server', 'plugins_dir')
    except Exception, e:
	print "Error: %s" % e

    pluginList = []
    try:
	# Get all registered plugins and add them to pluginList
	for i in config.get('server', 'plugins').split(','):
	    pluginList.append(i.strip().upper())
    except Exception, e:
	print "Error: %s" % e

    # start server
    server = WhatisServer(IP, PORT)
    asyncore.loop()

