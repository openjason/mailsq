import httplib, urllib, hashlib
from lxml import etree

class TosAPI:
    def __init__(self, **kwargs):
        self.app_name = kwargs.get('app_name')
        self.pass_key = kwargs.get('pass_key')

    def getFirstArrivalToStop(self, **kwargs):
        #server_method, location, KS_ID
       pass

    def getRouteArrivalToStop(self, **kwargs):
        #server_method, location, kr_id, ks_id
        pass

    def getRouteSchedule(self, **kwargs):
        #server_method, location, kr_id
        pass

    def getTransportPosition(self, **kwargs):
        #server_method, location, hullNo
        server_method = kwargs.get('server_method', 'get')
        location = kwargs.get('location', 'json')
        if server_method == 'post':
            if location == 'json':
                return self.serverRequest(server_method, location, {'method' : 'getTransportPosition', 'hullNo':kwargs.get('HULLNO', 0)})
            else:
                requestXml = etree.Element('request')
                tempXml = etree.Element('method')
                tempXml.text = 'getTransportPosition'
                requestXml.append(tempXml)
                tempXml = etree.Element('HULLNO')
                tempXml.text = kwargs.get('HULLNO', 0)
                requestXml.append(tempXml)
                return self.serverRequest(server_method, location, etree.tostring(requestXml))
        pass

    def findShortestPath(self, **kwargs):
        #???
        pass

    def serverRequest(self, server_method, location, request):
        request=str(request)
        signature = hashlib.sha1(request+self.pass_key).hexdigest()
        headers = {"Content-type": "application/x-www-form-urlencoded", "User-Agent":"samis"}
        print request
        print location
        if server_method == 'post':
            full_request = {'message':request, 'os':'testing', 'clientId':self.app_name, 'authKey':self.pass_key}
            conn = httplib.HTTPConnection("localhost")
            conn.request("POST", "/newapi/%s"% location, urllib.urlencode(full_request), headers)
            response = conn.getresponse()
            data = response.read()
            print data
            conn.close()
        else:
            pass
RequestExample= TosAPI(app_name='samis', pass_key='1')

print RequestExample.getTransportPosition(server_method='post', location='json', HULLNO='349081')
