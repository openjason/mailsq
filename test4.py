import sys
import http.client
from urllib import parse,request

HOST = 'www.webxml.com.cn'

API_URL = '/WebServices/MobileCodeWS.asmx?op=getMobileCodeInfo'
API_URL = '/WebServices/MobileCodeWS.asmx'
url = 'http://www.webxml.com.cn/WebServices/MobileCodeWS.asmx'
xmlstr = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <getMobileCodeInfo xmlns="http://WebXml.com.cn/">
      <mobileCode>13825632612</mobileCode>
      <userID>test</userID>
    </getMobileCodeInfo>
  </soap12:Body>
</soap12:Envelope>'''

#params = parse.urlencode({'xml': xmlstr})
params = xmlstr.encode()
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
headers = {'Content-Type': 'application/xml'}
request2 = xmlstr.encode()
webservice = http.client.HTTPConnection(HOST)
webservice.putrequest("POST", API_URL)
webservice.putheader("Host", HOST)
webservice.putheader("User-Agent","Python post")
webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
webservice.putheader("Content-length", "%d" % len(request2))
webservice.endheaders()

#result = webservice.request("POST", API_URL, params, headers)

response = request.urlopen(url, params)

#response = webservice.getresponse()
#print(response.status, response.reason)

data = response.read()

#statuscode, statusmessage, header = webservice.getreply()
#result = webservice.getfile().read()
#print (statuscode, statusmessage, header)
print (data)