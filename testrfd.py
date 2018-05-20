import urllib.request

def InvokeWebservice(phone,msg):
    texturl='http://www.webxml.com.cn/WebServices/MobileCodeWS.asmx?'
    texturl='http://localhost:8008/'
    print("website:",texturl)
    postcontent='<?xml version="1.0" encoding="utf-8"?>'
###    postcontent+='<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
##    postcontent+='<soap:Envelope xmlns:ns0="http://example.com/pysimplesoapsamle/">'
##    postcontent+='<soap:Body>'
##    postcontent+='<echo xmlns="http://example.com/pysimplesoapsamle/">'
###    postcontent+='<getMobileCodeInfo xmlns="http://WebXml.com.cn/">'
##    postcontent+='<mobileCode>13825632612</mobileCode>'#<phonenum>'+phone+'</phonenum>'#参数
##    postcontent+='<userID>123 </userID>'#<message>'+msg+'</message>'#参数
##    postcontent+='</getMobileCodeInfo>'
##    postcontent+='</soap:Body>'
##    postcontent+='</soap:Envelope>'


    postcontent+='<request>'
    postcontent+='  <onceKey>74e9a9a520589e5db9ef41d404a3dc94</onceKey>'
    postcontent+='<requestModel>'
    postcontent+='		<orderNo>20141115001</orderNo>'
    postcontent+='		<distributorCode>rfd</distributorCode>'
    postcontent+='	</requestModel>'
    postcontent+='<requestModel>'
    postcontent+='		<orderNo>20141115002</orderNo>'
    postcontent+='		<distributorCode>rfd</distributorCode>'
    postcontent+='</requestModel>'
    postcontent+='</requestModels>'
    postcontent+='</request>'



    req=urllib.request.Request(texturl,data=postcontent.encode('utf-8'),headers={'Content-Type': 'text/xml'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('utf-8'))

InvokeWebservice('1234','abcd')

