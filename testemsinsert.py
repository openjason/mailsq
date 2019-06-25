import urllib.request
import time

datestr = time.strftime('%Y%m%d', time.localtime(time.time()))
timestr = time.strftime('%H%M%S', time.localtime(time.time()))

def InvokeWebservice(snumber,mailnum):
    texturl = 'http://112.91.148.118:10000/post/EMS'
#    texturl='http://localhost:8008/Queryemsmail?wsdl'
# rfems: Recieve from ems

    datestr = time.strftime('%Y%m%d', time.localtime(time.time()))
    timestr = time.strftime('%H%M%S', time.localtime(time.time()))

    print("website:",texturl)
    postcontent='''<?xml version="1.0" encoding="utf-8"?>
<listexpressmail>
<expressmail>
<serialnumber>%(snumber)s</serialnumber>
<mailnum>%(mailnum)s</mailnum>
<procdate>%(datestr)s</procdate>
<proctime>%(timestr)s</proctime>
<orgfullname>所在地名称</orgfullname>
<action>00</action>
<description>描述信息</description>
<effect>1</effect>
<properdelivery>22</properdelivery>
<notproperdelivery>100</notproperdelivery>
</expressmail>
</listexpressmail>
''' % {'snumber': snumber, 'mailnum': mailnum,'datestr': datestr,'timestr': timestr}

#    print(postcontent)
    req=urllib.request.Request(texturl,data=postcontent.encode('utf-8'),headers={'Content-Type': 'text/xml','authenticate':'sqm123456sqm','version':'version523'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('utf-8'))

mailnum = 1175642270178

if __name__ == '__main__':
    for i in range(20190617084004,20190617084006):
        mailnum = mailnum +1
        InvokeWebservice(str(i),str(mailnum))
        print (i)
        print(mailnum)
