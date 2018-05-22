import urllib.request

def InvokeWebservice(phone,msg):
    texturl = 'http://192.168.18.101:8008/Queryemsmail?wsdl'
    texturl='http://localhost:8008/Queryemsmail?wsdl'

    print("website:",texturl)
    postcontent='''<?xml version="1.0" encoding="utf-8"?>
<listexpressmail>
<expressmail>
<serialnumber> 00000000000000000001 </serialnumber>
<mailnum> LK434266003CN </mailnum>
<procdate> 20130702 </procdate>
<proctime> 000100 </proctime>
<orgfullname> 所在地名称 </orgfullname>
<action> 00 </action>
<description> 描述信息 </description>
<effect> 有效、无效 </effect>
<properdelivery> 妥投使用 </properdelivery>
<notproperdelivery> 未妥投使用 </notproperdelivery>
</expressmail>
</listexpressmail>
'''
    req=urllib.request.Request(texturl,data=postcontent.encode('utf-8'),headers={'Content-Type': 'text/xml'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('utf-8'))

InvokeWebservice('1234','abcd')

