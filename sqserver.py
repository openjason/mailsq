#author:jasonchan
import urllib.request
a_url = 'http://www.webxml.com.cn/WebServices/TrainTimeWebService.asmx?wsdl'
a_url = 'http://www.webxml.com.cn/WebServices/MobileCodeWS.asmx?op=getMobileCodeInfo'
dataraw = urllib.request.urlopen(a_url).read()
type(dataraw)
data = dataraw.decode("utf-8")
print(data)