from urllib import parse,request

xmlstr = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <getMobileCodeInfo xmlns="http://WebXml.com.cn/">
      <mobileCode>13825632612</mobileCode>
      <userID>test</userID>
    </getMobileCodeInfo>
  </soap12:Body>
</soap12:Envelope>'''

headers = {'Content-Type': 'application/xml'}
res = request.Request('http://www.webxml.com.cn/WebServices/MobileCodeWS.asmx?', headers=headers, data=xmlstr)
resstr = res.urlopen(res)
print(resstr.read())