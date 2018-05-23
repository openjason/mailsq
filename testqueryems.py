import urllib.request

def InvokeWebservice(snumber,mailnum):
    texturl = 'http://1.1.1.64:8008/Queryemsmail?wsdl'
#    texturl='http://localhost:8008/Queryemsmail?wsdl'

    print("website:",texturl)
    postcontent='''<?xml version="1.0" encoding="utf-8"?>
<listexpressmail>
<expressmail>
<serialnumber> %(snumber)s </serialnumber>
<mailnum> LK%(mailnum)sCN </mailnum>
<procdate> 20130702 </procdate>
<proctime> 60100 </proctime>
<orgfullname> 所在地名称 </orgfullname>
<action> 00 </action>
<description> 描述信息 </description>
<effect> 1</effect>
<properdelivery> 22 </properdelivery>
<notproperdelivery> 100 </notproperdelivery>
</expressmail>
</listexpressmail>
''' % {'snumber': snumber, 'mailnum': mailnum}
    req=urllib.request.Request(texturl,data=postcontent.encode('utf-8'),headers={'Content-Type': 'text/xml','authenticate':'sqm123456sqm','version':'version523'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('utf-8'))

mailnum = 522000000

for i in range(1):
    mailnum = mailnum +1
    InvokeWebservice(str(i),str(mailnum))
    print (i)
    print(mailnum)
