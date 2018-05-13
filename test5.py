import urllib.request
import urllib.parse
url = r'http://www.webxml.com.cn/WebServices/MobileCodeWS.asmx'

data = urllib.parse.urlencode({'mobileCode': '13825632612', 'userID': '2'})
data = data.encode('utf-8')
with urllib.request.urlopen(url, data) as f:
    print(f.read().decode('utf-8'))
