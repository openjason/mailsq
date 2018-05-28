#！usr/bin/python
# -*- coding: utf-8 -*-
#author: Jason chan

import xml.etree.ElementTree as ET

def emsxmlproc(emsxml):
    # tree = ET.parse('ems.xml') #process the xml file.
    # root = tree.getroot()
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
    print(emsxmlproc(emsxml))
