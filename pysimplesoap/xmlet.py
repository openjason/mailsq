#！usr/bin/python
# -*- coding: utf-8 -*-
#==========================
import xml.etree.ElementTree as ET



def emsxmlproc(emsxml):
    # tree = ET.parse('ems.xml')
    # root = tree.getroot()
    root = ET.fromstring(emsxml)

    #print('root-tag:',root.tag,',root-attrib:',root.attrib,',root-text:',root.text)
    rstr = []
    for child in root:
    #     print('child-tag是：',child.tag,',child.attrib：',child.attrib,',child.text：',child.text)
        for sub in child:
           subtext = sub.text
           subtext = subtext.split()

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

    rstr.append(serialnumber)
    rstr.append(mailnum)
    rstr.append(procdate)
    rstr.append(proctime)
    rstr.append(orgfullname)
    rstr.append(action)
    rstr.append(description)
    rstr.append(effect)
    rstr.append(properdelivery)
    rstr.append(notproperdelivery)
    return rstr


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
</listexpressmail>
'''
    print(emsxmlproc(emsxml))
