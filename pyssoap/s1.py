from pysimplesoap.server import SoapDispatcher, SOAPHandler
from http.server import HTTPServer
import base64
#import cv2
from frvehiclelpr import *
import sys
import json

lpr = 0


def analyseImg(data, fileFormat):
    s = base64.b64decode(data)
    fileName = "test1." + fileFormat
    fileName = str(fileName)
    f = open(fileName, 'wb')
    f.write(s)
    f.flush()
    f.close()

    res = lpr.recognizeFile(fileName)
    res['platenum'] = res['platenum'].decode('gb2312')
    # print res['platenum']
    jstr = json.dumps(res)
    bstr = base64.b64encode(jstr)
    return bstr


if __name__ == '__main__':
    lpr = FrVehicleLpr()
    res = lpr.init()
    if not res:
        print(        "init lpr failed !")
        sys.exit(0)

    dispatcher = SoapDispatcher(
        'my_dispatcher',
        location="http://localhost:8008/",
        action='http://localhost:8008/',
        namespace="http://example.com/sample.wsdl", prefix="ns0",
        trace=True,
        ns=True)

    dispatcher.register_function('AnalyseImg', analyseImg,
                                 returns={'analyseResult': str},
                                 args={'data': str, 'fileFormat': str})

    print(    "Starting server...")
    httpd = HTTPServer(("", 8008), SOAPHandler)
    httpd.dispatcher = dispatcher
    httpd.serve_forever()