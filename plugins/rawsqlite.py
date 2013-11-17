#!/usr/bin/env python
#
# sqlite plugin
#
# Author: Radek Domanski
# email: radek.domanski # gmail.com
# website: intothebug.com

import sqlite3
import sys

ip = sys.argv[1]

# Your sqlite db location goes here
DB_LOCATION = ''
# Your query goes here. Remember to use parametrized queries! 
QUERY = ''

conn = sqlite3.connect(DB_LOCATION)

c = conn.cursor()

try:
    # Rewrite this parameter to include any variables that are required to run parametrized query
    c.execute(QUERY, [])
    data = c.fetchall()
except Exception, e:
    print "Error: %s" % (e)

# Here you can postprocess returned data if required

results = ''
try:
    for d in data:
	results += d
except Exception, e:
    print "Error: %s" % e

print results
