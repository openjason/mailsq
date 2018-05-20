import urllib.request

def InvokeWebservice(phone,msg):
    texturl='http://localhost:8008/Queryrfdmail?wsdl'
#    texturl = 'http://192.168.18.101:8008/Queryrfdmail?wsdl'
    print("website:",texturl)
    postcontent='''<?xml version="1.0" encoding="utf-8"?>
<request>
	<onceKey>3eef7836aac024fdf699f88ab6414a1d</onceKey>
<requestModel>
		<distributorCode>rfd</distributorCode>
<orderNo>20141115001</orderNo>
		<logId>440462</logId>
</requestModel>
</request>'''

    req=urllib.request.Request(texturl,data=postcontent.encode('utf-8'),headers={'Content-Type': 'text/xml'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('utf-8'))

InvokeWebservice('1234','abcd')

