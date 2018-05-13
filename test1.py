import urllib.parse
import http.client

httpClient = None

params = urllib.parse.urlencode({'mobileCode': '13825632612', 'userID': '5'})

headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
headers = {"Content-type": "text/html; charset=utf-8"}
httpClient = http.client.HTTPConnection('www.webxml.com.cn', 80, timeout=10)

httpClient.request('POST', '/WebServices/MobileCodeWS.asmx', params, headers)

response = httpClient.getresponse()

print(response.status)
print (response.reason)

print (response.read().decode('utf-8'))

print (response.getheaders())


if httpClient:
    httpClient.close()
