#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.sax

data_one = []
data_any = []

class MovieHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.type = ""
        self.format = ""
        self.year = ""
        self.rating = ""
        self.stars = ""
        self.description = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "movie":
            print("*****Movie*****")
            title = attributes["title"]
            print("Title:", title)

    # 元素结束事件处理
    def endElement(self, tag):
        if self.CurrentData == "type":
            print("Type:", self.type)

        elif self.CurrentData == "format":
            print("Format:", self.format)

        elif self.CurrentData == "year":
            print("Year:", self.year)

        elif self.CurrentData == "rating":
            print("Rating:", self.rating)

        elif self.CurrentData == "stars":
            print("Stars:", self.stars)

        elif self.CurrentData == "description":
            print("Description:", self.description)

        self.CurrentData = ""
        data_one.append(self.type)
        data_one.append(self.format)
        data_one.append(self.year)
        data_one.append(self.rating)
        data_one.append(self.stars)
        data_one.append(self.description)

        data_any.append(data_one)

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "type":
            self.type = content
        elif self.CurrentData == "format":
            self.format = content
        elif self.CurrentData == "year":
            self.year = content
        elif self.CurrentData == "rating":
            self.rating = content
        elif self.CurrentData == "stars":
            self.stars = content
        elif self.CurrentData == "description":
            self.description = content

def xml_rfd():
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)
    parser.parse("ems.xml")

if (__name__ == "__main__"):
    xml_rfd()