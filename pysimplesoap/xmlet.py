#！usr/bin/python
# -*- coding: utf-8 -*-
#==========================
import xml.etree.ElementTree as ET
tree = ET.parse('ems.xml')
root = tree.getroot()
print('root-tag:',root.tag,',root-attrib:',root.attrib,',root-text:',root.text)
for child in root:
     print('child-tag是：',child.tag,',child.attrib：',child.attrib,',child.text：',child.text)
     for sub in child:
          print('sub-tag是：',sub.tag,',sub.attrib：',sub.attrib,',sub.text：',sub.text)
          for sub2 in sub:
               print('sub2-tag是：',sub2.tag,',sub2.attrib：',sub2.attrib,',sub2.text：',sub2.text)

