import http.client, urllib.parse
HOST = 'www.webxml.com.cn'

a_url = '/WebServices/MobileCodeWS.asmx?op=getMobileCodeInfo'.encode('utf-8')
#params = urllib.parse.urlencode({'@mobileCode': 13825632612, '@userID': 'issue'})
#params = urllib.parse.urlencode(/WebServices/MobileCodeWS.asmx?op=getMobileCodeInfo)
headers = {"Content-type": "text/html; charset=utf-8"}
conn = http.client.HTTPConnection(HOST)
conn.request("POST", "", a_url, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read().decode('utf-8')
print(data)

conn.close()