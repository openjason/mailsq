import urllib.request

def InvokeWebservice(phone,msg):
    texturl='http://www.webxml.com.cn/WebServices/MobileCodeWS.asmx'
    postcontent='<?xml version="1.0" encoding="utf-8"?>'
    postcontent+='<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
    postcontent+='<soap:Body>'
    postcontent+='<getMobileCodeInfo xmlns="http://WebXml.com.cn/">'
    postcontent+='<mobileCode>13825632612</mobileCode>'#<phonenum>'+phone+'</phonenum>'#参数
    postcontent+='<userID> </userID>'#<message>'+msg+'</message>'#参数
    postcontent+='</getMobileCodeInfo>'
    postcontent+='</soap:Body>'
    postcontent+='</soap:Envelope>'
    req=urllib.request.Request(texturl,data=postcontent.encode('utf-8'),headers={'Content-Type': 'text/xml'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('utf-8'))

InvokeWebservice('1234','abcd')

