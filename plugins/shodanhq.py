#!/usr/bin/env python
#
# shodan plugin
#
# Author: Radek Domanski
# email: radek.domanski # gmail.com
# website: intothebug.com

from shodan import WebAPI
import sys

# put your shodan API key here
SHODAN_API_KEY = ""

api = WebAPI(SHODAN_API_KEY)

try:
    host = api.host(sys.argv[1])

    r = ''

    # process data from shodan
    for item in host['data']:
	for key in item.keys():
	    r += "%s: %s" % (key, repr(item[key]))
	r += "\n==============================\n"

    print r
except Exception, e:
    print "Error: %s" % e
