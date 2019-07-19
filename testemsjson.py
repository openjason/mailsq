import urllib.request
import time

datestr = time.strftime('%Y%m%d', time.localtime(time.time()))
timestr = time.strftime('%H%M%S', time.localtime(time.time()))

def InvokeWebservice(snumber,mailnum):
    texturl = 'http://112.91.148.118:10000/post/GHX'
#    texturl='http://localhost:8008/Queryemsmail?wsdl'
# rfems: Recieve from ems

    datestr = time.strftime('%Y%m%d', time.localtime(time.time()))
    timestr = time.strftime('%H%M%S', time.localtime(time.time()))

    print("website:",texturl)
    postcontent='''{"listexpressmail": [
  {
    "serialnumber":"%(snumber)s1",
    "mailnum": "%(mailnum)s2",
    "procdate": "%(datestr)s",
    "proctime": "%(timestr)s",
    "orgfullname": "所在地名称a",
    "action": "41",
"description": "描述信息a",
"effect":"1",
"properdelivery":"22",
"notproperdelivery":"100"
  }
]}

''' % {'snumber': snumber, 'mailnum': mailnum,'datestr': datestr,'timestr': timestr}

#    print(postcontent)
    req=urllib.request.Request(texturl,data=postcontent.encode('utf-8'),headers={'Content-Type': 'text/json','authenticate':'sqm123456sqm','version':'version523'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('utf-8'))

mailnum = 1175642270178

if __name__ == '__main__':
    for i in range(20190617084004,20190617084006):
        mailnum = mailnum +1
        time.sleep(1)
        InvokeWebservice(str(i),str(mailnum))
        print (i)
        print(mailnum)
