import urllib.request




def emsquery(mailnum):
    texturl='http://1.1.1.64:8008/queryems'
#    texturl = 'http://192.168.18.101:8008/Queryrfdmail?wsdl'
    print("website:",texturl)
    postcontent='''<?xml version="1.0" encoding="utf-8"?>
<request>
	<onceKey>3eef7836aac024fdf699f88ab6414a1d</onceKey>
<requestModel>
		<distributorCode>ems</distributorCode>
<orderNo>%(mailnum)s</orderNo>
		<logId>440462</logId>
</requestModel>
</request>'''%{'mailnum':mailnum}

    print (postcontent)
    req=urllib.request.Request(texturl,data=postcontent.encode('utf-8'),headers={'Content-Type': 'text/xml'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('utf-8'))

if __name__ == '__main__':
#    InvokeWebservice('1234', 'abcd')
    emsquery('LK142005002CN')
