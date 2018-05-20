import urllib.request

def InvokeWebservice(phone,msg):
    texturl='http://www.webxml.com.cn/WebServices/MobileCodeWS.asmx?'
    texturl='http://localhost:8008'
    print("website:",texturl)
    postcontent='<?xml version="1.0" encoding="utf-8"?>'
    postcontent+='<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
#    postcontent+='<soap:Envelope xmlns:ns0="http://ns.example.com/pysimplesoapsamle/">'
    postcontent+='<soap:Body>'
    postcontent+='<echo xmlns="http://example.com/pysimplesoapsamle/">'
#    postcontent+='<getMobileCodeInfo xmlns="http://WebXml.com.cn/">'
    postcontent+='<mobileCode>13825632612</mobileCode>'#<phonenum>'+phone+'</phonenum>'#参数
    postcontent+='<userID>123 </userID>'#<message>'+msg+'</message>'#参数
    postcontent+='</getMobileCodeInfo>'
    postcontent+='</soap:Body>'
    postcontent+='</soap:Envelope>'


    req=urllib.request.Request(texturl,data=postcontent.encode('utf-8'),headers={'Content-Type': 'text/xml'})
    respRaw = urllib.request.urlopen(req)
    print(respRaw.read().decode('utf-8'))

InvokeWebservice('1234','abcd')

'''
快递反馈接口报文
反馈的数据报文如下：
Xml反馈报文格式
<?xml version="1.0" encoding="UTF-8"?>
<listexpressmail>
<expressmail>
<serialnumber>00000000000000000001</serialnumber>
<mailnum>LK434266003CN</mailnum>
<procdate>20130702</procdate>
<proctime>000100</proctime>
<orgfullname>所在地名称</orgfullname>
<action>00</action>
<description>描述信息</description>
<effect>有效、无效</effect>
<properdelivery>妥投使用</properdelivery>
<notproperdelivery>未妥投使用</notproperdelivery>
</expressmail>
</listexpressmail>


服务端的响应报文：
Xml:
<?xml version="1.0" encoding="UTF-8"?>
<response>
<success>0</success>
<failmailnums></failmailnums>
<remark></remark>
</response>


1.1.2.2 推送快递单号接口
Post提交参数 请求报文 ：requestxml
签名 ：sign
* 接口说明
默认为每5分钟（可参数配置）将有更新的快递单号全部进行推送，每笔推送消息报文最多包含50笔（可参数配置）快递单号，如超过50笔则拆分为多次推送请求推送过来（无需再等待5分
钟）。
每次请求中同一配送商的快递单号不能重复。
接口响应时间限制为1分钟，超时的订单将进行重新推送。
请求报文示例

<request>
<onceKey>74e9a9a520589e5db9ef41d404a3dc94</onceKey>
<requestModels>
<requestModel>
<orderNo>20141115001</orderNo>
<distributorCode>rfd</distributorCode>
</requestModel>
<requestModel>
<orderNo>20141115002</orderNo>
<distributorCode>rfd</distributorCode>
</requestModel>
</requestModels>
</request>



成功响应报文示例

<response>
<onceKey>bffc0048854d711812662a5c57cc8e19</onceKey>
<isSuccess>0</isSuccess>
<resultCode>01</resultCode>
<responseModels>
<responseModel>
<distributorCode>rfd</distributorCode>
<orderNo>20141115001</orderNo>
</responseModel>
<responseModel>
<distributorCode>rfd</distributorCode>
<orderNo>20141115002</orderNo>
</responseModel>
</responseModels>
</response>

失败响应报文示例
<response>
<onceKey>bffc0048854d711812662a5c57cc8e19</onceKey>
<isSuccess>1</isSuccess>
<resultCode>06</resultCode>
</response>

1.1.2.3 查询物流详情接口
请求报文示例

<request>
<onceKey>3eef7836aac024fdf699f88ab6414a1d</onceKey>
<requestModel>
<distributorCode>rfd</distributorCode>
<orderNo>20141115001</orderNo>
<logId>440462</logId>
</requestModel>
</request>
* 响应报文定
成功响应报文示例

<response>
<onceKey>b362b017614cae41be77a2035ef99da1</onceKey>
<isSuccess>0</isSuccess>
<resultCode>01</resultCode>
<responseModels>
<responseModel>
<distributorCode>rfd</distributorCode>
<logId>440462</logId>
<waybillNo> 9140725075042 </waybillNo>
<orderNo>20141115001</orderNo>
<operateTime>2014/11/15 18:05:40</operateTime>
<operateLog>已送达成功</operateLog>
<status>3</status>
</responseModel>
<responseModel>
<distributorCode>rfd</distributorCode>
<logId>440462</logId>
<waybillNo> 9140725035040 </waybillNo>
<orderNo>20141115002</orderNo>
<operateTime>2014/11/15 18:05:40</operateTime>
<operateLog>
运单已由XXX送出，联系电话：XXX
</operateLog>
<status>2</status>
</responseModel>
</responseModels>
</response>

失败响应报文示例
<response>
<onceKey>b362b017614cae41be77a2035ef99da1</onceKey>
<isSuccess>1</isSuccess>
<resultCode>03<resultCode>
</response>
'''