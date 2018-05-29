import urllib.request

def InvokeWebservice(phone,msg):
    texturl='http://1.1.1.64:8008/Queryrfdmail?wsdl'
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

    req=urllib.request.Request(texturl,data=postcontent.encode('GBK'),headers={'Content-Type': 'text/xml'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('GBK'))



if __name__ == '__main__':
    InvokeWebservice('1234', 'abcd')