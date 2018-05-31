#！usr/bin/python
# -*- coding: utf-8 -*-
#author: Jason chan

import xml.etree.ElementTree as ET
import datetime

import logging

log = logging.getLogger('tst')


def xmlet_emsxmlproc(emsxml):
    # 格式化来自ems单详细信息，处理后将保存到数据库
    # root = tree.getroot()
    try:
        rstr_all = []
        root = ET.fromstring(emsxml)        #directory process xml string.
        #print('root-tag:',root.tag,',root-attrib:',root.attrib,',root-text:',root.text)
        for child in root:
            rstr_one = []
            for sub in child:
                subtext = sub.text
                subtext = subtext.strip()

                if sub.tag == 'serialnumber':
                    serialnumber = subtext
                elif sub.tag == 'mailnum' :
                    mailnum = subtext
                elif sub.tag == 'procdate':
                    procdate = subtext
                elif sub.tag == 'proctime':
                    proctime = subtext
                elif sub.tag == 'orgfullname':
                    orgfullname = subtext
                elif sub.tag == 'action':
                    action = subtext
                elif sub.tag == 'description':
                    description = subtext
                elif sub.tag == 'effect':
                    effect = subtext
                elif sub.tag == 'properdelivery':
                    properdelivery = subtext
                elif sub.tag == 'notproperdelivery':
                    notproperdelivery = subtext

    #if var have none value,it append will raise exception.
            rstr_one.append(serialnumber)
            rstr_one.append(mailnum)
            rstr_one.append(procdate)
            rstr_one.append(proctime)
            rstr_one.append(orgfullname)
            rstr_one.append(action)
            rstr_one.append(description)
            rstr_one.append(effect)
            rstr_one.append(properdelivery)
            rstr_one.append(notproperdelivery)
            rstr_all.append(rstr_one)
        return rstr_all
    except Exception as e:
        log.error("error in xmlet_emsxmlproc" + str(e))
        return "error in xmlet_emsxmlproc:" + str(e)

def xmlet_emsqueryproc(emsxml):
    # 格式化对ems的查询申请
    try:
        rstr_all = []
        root = ET.fromstring(emsxml)
    #    print('root-tag:',root.tag,',root-attrib:',root.attrib,',root-text:',root.text)
        for child in root:
    #        print('child-tag:', child.tag, ',child-attrib:', child.attrib, ',child-text:', child.text)
            rstr_one = []
            subtext = child.text
            subtext = subtext.strip()
            if child.tag == 'onceKey':
                rstr_all.append(subtext)

            for sub in child:
    #            print('sub-tag:', sub.tag, ',sub-attrib:', sub.attrib, ',sub-text:', sub.text)
                subtext = sub.text
                subtext = subtext.strip()

                if sub.tag == 'distributorCode' :
                    distributorCode = subtext
                elif sub.tag == 'orderNo':
                    orderNo = subtext
                elif sub.tag == 'logId':
                    logId = subtext

            if child.tag == 'requestModel':
                rstr_one.append(distributorCode)
                rstr_one.append(orderNo)
                rstr_one.append(logId)
                rstr_all.append(rstr_one)


    #if var have none value,it append will raise exception.
            # rstr_one.append(onceKey)
            # rstr_one.append(distributorCode)
            # rstr_one.append(orderNo)
            # rstr_one.append(logId)
            #
            # rstr_all.append(rstr_one)
        return rstr_all
    except Exception as e:
        log.error("error in xmlet_emsqueryproc" + str(e))
        return "error in xmlet_emsqueryproc:" + str(e)

def xmlet_emslist_to_xml(ems_list):
    xmlstr_toems = '<?xml version="1.0" encoding="UTF-8"?><listexpressmail>'

    for ems_rec in ems_list:
        snumber = ems_rec[0]
        mailnum = ems_rec[1]
        procdate = ems_rec[2]
        proctime = ems_rec[3]
        orgfullname = ems_rec[4]
        action = ems_rec[5]
        description = ems_rec[6]
        effect = ems_rec[7]
        properdelivery = ems_rec[8]
        notproperdelivery = ems_rec[9]
        xmlstr_toems = xmlstr_toems + '''
<expressmail>
<serialnumber>%(snumber)s</serialnumber>
<mailnum>%(mailnum)s</mailnum>
<procdate>%(procdate)s</procdate>
<proctime>%(proctime)s</proctime>
<orgfullname>%(orgfullname)s</orgfullname>
<action>%(action)s</action>
<description>%(description)s</description>
<effect>%(effect)s</effect>
<properdelivery>%(properdelivery)s</properdelivery>
<notproperdelivery>%(notproperdelivery)s</notproperdelivery>
</expressmail>'''%{'snumber': snumber, 'mailnum': mailnum,'procdate': procdate,'proctime': proctime,'orgfullname':orgfullname,\
     'action':action,'description':description,'effect':effect,'properdelivery':properdelivery,'notproperdelivery':notproperdelivery}

    xmlstr_toems = xmlstr_toems + '</listexpressmail>'
    return xmlstr_toems

if __name__ == '__main__':

    emsxml = '''<?xml version="1.0" encoding="UTF-8"?>
<listexpressmail>
  <expressmail>
	<serialnumber>00000000000000000001</serialnumber>
    <mailnum>LK434266003CN</mailnum>
    <procdate> 20130702</procdate>
    <proctime> 000100</proctime>
    <orgfullname>所在地名称</orgfullname>
    <action>00</action>
<description>描述信息</description>
<effect>0</effect>
<properdelivery>12</properdelivery>
<notproperdelivery>123</notproperdelivery>
  </expressmail>
  <expressmail>
	<serialnumber>10000000000000000001</serialnumber>
    <mailnum>LK434266003CN</mailnum>
    <procdate> 20130702</procdate>
    <proctime> 000100</proctime>
    <orgfullname>所在地名称</orgfullname>
    <action>00</action>
<description>描述信息</description>
<effect>0</effect>
<properdelivery>12</properdelivery>
<notproperdelivery>123</notproperdelivery>
  </expressmail>
  <expressmail>
	<serialnumber>20000000000000000001</serialnumber>
    <mailnum>LK434266003CN</mailnum>
    <procdate> 20130702</procdate>
    <proctime> 000100</proctime>
    <orgfullname>所在地名称</orgfullname>
    <action>00</action>
<description>描述信息</description>
<effect>0</effect>
<properdelivery>12</properdelivery>
<notproperdelivery>123</notproperdelivery>
  </expressmail>
</listexpressmail>
'''

    emsqueryxml = '''<request>
<onceKey> 3eef7836aac024fdf699f88ab6414a1d </onceKey>
<requestModel>
<distributorCode > ems </distributorCode>
<orderNo> 20141115001 </orderNo>
<logId> 440462 </logId>
</requestModel>
<requestModel>
<distributorCode > ems </distributorCode>
<orderNo> 20141115003 </orderNo>
<logId> 440463 </logId>
</requestModel>
</request>'''
    emsqueryxml = '''<?xml version="1.0" encoding="utf-8"?>
<request>
	<onceKey>3eef7836aac024fdf699f88ab6414a1d</onceKey>
<requestModel>
		<distributorCode>ems</distributorCode>
<orderNo>LK542000001CN</orderNo>
		<logId>440462</logId>
</requestModel>
</request>'''

    from_db_list = []
    from_db_list.append(['4234', 'LK542000001CN', datetime.date(2018, 5, 29), datetime.timedelta(0, 40690), '所在地名称', '00', '描述信息', '1', '22', '100'])
    from_db_list.append(['4234', 'LK542000001CN', datetime.date(2013, 7, 2), datetime.timedelta(0, 21660), '所在地名称', '00', '描述信息', '1', '22', '100'])
    from_db_list.append(['4234', 'LK542000001CN', datetime.date(2013, 7, 2), datetime.timedelta(0, 21660), '所在地名称', '00', '描述信息', '1', '22', '100'])
#    print(from_db_list)
    print(xmlet_emsqueryproc(emsqueryxml))
#    print(xmlet_emslist_to_xml(from_db_list))
