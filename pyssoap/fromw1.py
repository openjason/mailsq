from pysimplesoap.client import SoapClient, SoapFault
import sys
#import MySQLdb as msdb
import datetime
from datetime import date
from datetime import datetime

#Dit is de management.py voor de Linux Machine

# create a simple consumer
client = SoapClient(
    location = "192.168.18.227:8008/",
    action = '192.168.18.227:8008', # SOAPAction
    namespace = "http://example.com/sample.wsdl",
    soap_ns='soap',
    ns = False)

# call a few remote methods
HN = str(client.get_value(number=1).resultaat)
print ("Hostname:", HN)

AVAIL_MEM_MB = str(client.get_value(number=2).resultaat)
print ("Fysiek geheugen :", int(AVAIL_MEM_MB),"MB") # AVAIL_MEM_MB is a number!

IP_ADDRESS = str(client.get_value(number=3).resultaat)
print ("IP_Address: ", IP_ADDRESS) # This is a multiline: strip the newline from the result!

FREE_SPACE = int(client.get_value(number=4).resultaat)
print ("Free Space:", FREE_SPACE)

UPTIME = int(client.get_value(number=5).resultaat)
print ("Uptime: ", UPTIME)

TIMESTAMP = datetime.today()

##try:
##        cnnx = msdb.connect('localhost', 'Gijs', 'Welkom#1', "monitoring" )
##        curs = cnnx.cursor()
##        curs.execute(""" INSERT INTO LINUX (HOST, AVAIL_MEM, IP_ADDRESS, FREE_SPACE, UPTIME, TIMESTAMP) VALUES (%s, %s, %s, %s, %s, %s) """ ,(HN, AVAIL_MEM_MB, IP_ADDRES$
##        cnnx.commit()
##
##finally:
##        if cnnx:
##                cnnx.close()
