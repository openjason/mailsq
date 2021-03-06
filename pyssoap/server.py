#!/usr/bin/python
# -*- coding: utf-8 -*-
# 物流信息接收处理系统
# 系统是一个物流信息中转系统，主要是接收在物流公司实时发送的http-post报文，保存在数据库，
# 系统在客户查询的时候返回最新的物流信息，也支持主动批量将物流信息发送给客户指定网络接口。
# 系统处理数据量大，百万条记录以上，实时性要求高，要及时处理报文，以免影响报文的接收和发送。
# 报文发送和接收有验证机制，接口地址判断，头信息，授权码等方式确认报文来源验证。
#
# 文本文件数据导入MYSQL：
# load data local infile 'filename.txt' into table tablename(field1,field2,field3)
# 如果文本数据用空格分开，硬回车结束，可不加下面的命令：
#   FIELDS TERMINATED BY ':'
#   LINES TERMINATED BY '\r\n';
# mysqlimport客户端提供了LOAD DATA INFILE SQL语句的一个命令行接口。mysqlimport的大多数选项直接对应LOAD DATA INFILE子句。
#
# 一次插入多条数据，可用values后更多条值，用小括号包含每条数据，用逗号分开。
# insert into normalcode(code,detail) values('11','本人收'),('12','单位收发章'),('13','未出口退回妥投'),('14','退回妥投')
#
#author: jason chan

import datetime
import sys
import logging
import warnings
import re
import traceback
import logging.handlers
from http.server import BaseHTTPRequestHandler, HTTPServer
from simplexml import SimpleXMLElement, TYPE_MAP, Date, Decimal
from xmlet import xmlet_emsxmlproc,xmlet_emslist_to_xml,xmlet_emsqueryproc
from mysqldb import mysql_emstodb,mysql_query_ems
import pymysql.cursors


unicode = str
LOG_FILE = 'msq.log'
VERSION = 'ep0.06181653'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

log = logging.getLogger('tst')  # 获取名为tst的logger
logging.getLogger('tst').addHandler(console)
log.addHandler(handler)  # 为logger添加handler
log.setLevel(logging.DEBUG)

# Deprecated?
NS_RX = re.compile(r'xmlns:(\w+)="(.+?)"')

__author__ = "jc"
__copyright__ = "ep"
__license__ = "none"
__version__ = "1.04a"

class SoapFault(Exception):
    def __init__(self, faultcode=None, faultstring=None, detail=None):
        self.faultcode = faultcode or self.__class__.__name__
        self.faultstring = faultstring or ''
        self.detail = detail

class SoapDispatcher(object):
    """Simple Dispatcher for SOAP Server"""

    def __init__(self, name, documentation='', action='', location='',
                 namespace=None, prefix=False,
                 soap_uri="http://schemas.xmlsoap.org/soap/envelope/",
                 soap_ns='soap',
                 namespaces={},
                 pretty=False,
                 debug=False,
                 **kwargs):

        self.methods = {}
        self.name = name
        self.documentation = documentation
        self.action = action  # base SoapAction
        self.location = location
        self.namespace = namespace  # targetNamespace
        self.prefix = prefix
        self.soap_ns = soap_ns
        self.soap_uri = soap_uri
        self.namespaces = namespaces
        self.pretty = pretty
        self.debug = debug


    @staticmethod
    def _extra_namespaces(xml, ns):
        """Extends xml with extra namespaces.
        :param ns: dict with namespaceUrl:prefix pairs
        :param xml: XML node to modify
        """
        if ns:
            _tpl = 'xmlns:%s="%s"'
            _ns_str = " ".join([_tpl % (prefix, uri) for uri, prefix in ns.items() if uri not in xml])
            xml = xml.replace('/>', ' ' + _ns_str + '/>')
        return xml

    def register_function(self, name, fn, returns=None, args=None, doc=None):
        self.methods[name] = fn, returns, args, doc or getattr(fn, "__doc__", "")

    def response_element_name(self, method):
        return '%sRes3ponse' % method

    def dispatch(self, xml, action=None, fault=None, method = None):
        """Receive and process SOAP call, returns the xml"""
        # a dict can be sent in fault to expose it to the caller
        # default values:
        prefix = self.prefix
        ret = None
        if fault is None:
            fault = {}
        soap_ns, soap_uri = self.soap_ns, self.soap_uri
        soap_fault_code = 'VersionMismatch'
        name = None

        # namespaces = [('model', 'http://model.common.mt.moboperator'), ('external', 'http://external.mt.moboperator')]
        _ns_reversed = dict(((v, k) for k, v in self.namespaces.items()))  # Switch keys-values
        # _ns_reversed = {'http://external.mt.moboperator': 'external', 'http://model.common.mt.moboperator': 'model'}
        global connection
        try:
            request = xml#SimpleXMLElement(xml, namespace=self.namespace)
            log.debug('dispatch method: %s', method)
#            print("jt1xml:",xml)
            if method == 'rfromems':
                print("run ems insert data")
                    #ems xml request exchage to a list.
                ems_extract_list = xmlet_emsxmlproc(request)

                if isinstance(ems_extract_list,list):
                    for ems_single_list in ems_extract_list:
                        mysql_emstodb(connection, ems_single_list)
                    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<response>
<success>0</success>
<failmailnums></failmailnums>
<remark></remark>
</response>'''
                else:
                    log.debug("ems xml processing error.")
                    log.debug(request)

            elif method == 'queryems':
                print("run ems query")
                ems_extract_list = xmlet_emsqueryproc(request)
                if isinstance(ems_extract_list,list):
                    if len(ems_extract_list) < 2:
                        log.info("error ems_extract_list less than 2.")
                    else:
                        ems_onekey = ems_extract_list.pop(0)    #将 onekey 剥离，保留查询数据。
                        #global connection
                        for ems_single_list in ems_extract_list:
                            if ems_single_list[0] == 'ems':
                                emsqr_list = mysql_query_ems(connection, ems_single_list[1])
                            else:
                                log.error("error ems_extract_list[0] unknow")
                                log.error(ems_single_list)
                        if isinstance(emsqr_list,list):
                            if len(emsqr_list) >0:
                                xml=xmlet_emslist_to_xml(emsqr_list)
                            else:
                                log.error("error not found the mailnum: "+str(ems_single_list[1]))
                                xml = '''<?xml version="1.0" encoding="GBK"?><response>errror ems query, No MailNum Found.</response>'''
                        else:
                            log.error("error emsqr_list not a list")
                            log.error(emsqr_list)
                else:
                    log.debug("error ems query request processing error.")
                    log.debug(request)


            elif method == 'rfdquery':
                print("run rfd")
                xml='''<?xml version="1.0" encoding="GBK"?><response>rfd None</response>'''

            else:
                print("jr1:Can not match method")
                raise Exception
            #soap_fault_code = 'Server'

        except Exception as e:  # This shouldn't be one huge try/except
            logging.info ("error exception "+str(e))
            xml='<response>Request methon error...Exception...</response>'
        xml = SoapDispatcher._extra_namespaces(xml,{})
#        xml = SoapDispatcher._extra_namespaces(xml, _ns_reversed)

        # Change our namespace alias to that given by the client.
        # We put [('model', 'http://model.common.mt.moboperator'), ('external', 'http://external.mt.moboperator')]
        # mix it with {'http://external.mt.moboperator': 'ext', 'http://model.common.mt.moboperator': 'mod'}
        mapping = dict(((k, _ns_reversed[v]) for k, v in self.namespaces.items()))  # Switch keys-values and change value
        # and get {'model': u'mod', 'external': u'ext'}

        response = SimpleXMLElement(xml)#,namespace=self.namespace,namespaces_map=mapping,prefix=prefix)

        body = response#.add_child("%s:Body" % soap_ns, ns=False)

        if fault:
            # generate a Soap Fault (with the python exception)
            body.marshall("%s:Fault" % soap_ns, fault, ns=False)
        else:
            # return normal value
            res = body#.add_child(self.response_element_name(name), ns=self.namespace)
            if not prefix:
                res['xmlns'] = self.namespace  # add target namespace

            # serialize returned values (response) if type definition available
            returns_types = {}
            if returns_types:
                # TODO: full sanity check of type structure (recursive)
                complex_type = isinstance(ret, dict)
                if complex_type:
                    # check if type mapping correlates with return value
                    types_ok = all([k in returns_types for k in ret.keys()])
                    if not types_ok:
                        warnings.warn("Return value doesn't match type structure: "
                                     "%s vs %s" % (str(returns_types), str(ret)))
                if not complex_type or not types_ok:
                    # backward compatibility for scalar and simple types
                    res.marshall(list(returns_types.keys())[0], ret, )
                else:
                    # new style for complex classes
                    for k, v in ret.items():
                        res.marshall(k, v)



#        return response.as_xml('<response><onceKey>bffc0048854d711812662a5c57cc8e19</onceKey><isSuccess>1</isSuccess><resultCode>06</resultCode></response>')
#         print(self.list_methods())
#         print("mm:", self.response_element_name(name))
#        args = supper.path[1:].split("?")

#        req, res, doc = self.server.dispatcher.help(args[0])

        return response.as_xml(pretty=self.pretty)

    # Introspection functions:

    def list_methods(self):
        """Return a list of aregistered operations"""
        return [(method, doc) for method, (function, returns, args, doc) in self.methods.items()]

    def help(self, method=None):
        """Generate sample request and response messages"""
        (function, returns, args, doc) = self.methods[method]
#add line
        xml = """
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
<soap:Body><%(method)s xmlns="%(namespace)s"/></soap:Body>
</soap:Envelope>""" % {'method': method, 'namespace': self.namespace}
        request = SimpleXMLElement(xml, namespace=self.namespace, prefix=self.prefix)
        if args:
            items = args.items()
        elif args is None:
            items = [('value', None)]
        else:
            items = []
        for k, v in items:
            request(method).marshall(k, v, add_comments=True, ns=False)

        xml = """
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
<soap:Body><%(method)sResponse xmlns="%(namespace)s"/></soap:Body>
</soap:Envelope>""" % {'method': method, 'namespace': self.namespace}
        response = SimpleXMLElement(xml, namespace=self.namespace, prefix=self.prefix)
        if returns:
            items = returns.items()
        elif args is None:
            items = [('value', None)]
        else:
            items = []
        for k, v in items:
            response('%sResponse' % method).marshall(k, v, add_comments=True, ns=False)

        return request.as_xml(pretty=True), response.as_xml(pretty=True), doc

    def wsdl(self):
        """Generate Web Service Description v1.1"""
        xml = """<?xml version="1.0"?>
<wsdl:definitions name="%(name)s"
          targetNamespace="%(namespace)s"
          xmlns:tns="%(namespace)s"
          xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
          xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
          xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">%(documentation)s</wsdl:documentation>

    <wsdl:types>
       <xsd:schema targetNamespace="%(namespace)s"
              elementFormDefault="qualified"
              xmlns:xsd="http://www.w3.org/2001/XMLSchema">
       </xsd:schema>
    </wsdl:types>
</wsdl:definitions>
""" % {'namespace': self.namespace, 'name': self.name, 'documentation': self.documentation}
        wsdl = SimpleXMLElement(xml)

        for method, (function, returns, args, doc) in self.methods.items():
            # create elements:

            def parse_element(name, values, array=False, complex=False):
                if not complex:
                    element = wsdl('wsdl:types')('xsd:schema').add_child('xsd:element')
                    complex = element.add_child("xsd:complexType")
                else:
                    complex = wsdl('wsdl:types')('xsd:schema').add_child('xsd:complexType')
                    element = complex
                element['name'] = name
                if values:
                    items = values
                elif values is None:
                    items = [('value', None)]
                else:
                    items = []
                if not array and items:
                    all = complex.add_child("xsd:all")
                elif items:
                    all = complex.add_child("xsd:sequence")
                for k, v in items:
                    e = all.add_child("xsd:element")
                    e['name'] = k
                    if array:
                        e[:] = {'minOccurs': "0", 'maxOccurs': "unbounded"}
                    if v in TYPE_MAP.keys():
                        t = 'xsd:%s' % TYPE_MAP[v]
                    elif v is None:
                        t = 'xsd:anyType'
                    elif isinstance(v, list):
                        n = "ArrayOf%s%s" % (name, k)
                        l = []
                        for d in v:
                            l.extend(d.items())
                        parse_element(n, l, array=True, complex=True)
                        t = "tns:%s" % n
                    elif isinstance(v, dict):
                        n = "%s%s" % (name, k)
                        parse_element(n, v.items(), complex=True)
                        t = "tns:%s" % n
                    else:
                        raise TypeError("unknonw type %s for marshalling" % str(v))
                    e.add_attribute('type', t)

            parse_element("%s" % method, args and args.items())
            parse_element("%sResponse" % method, returns and returns.items())

            # create messages:
            for m, e in ('Input', ''), ('Output', 'Response'):
                message = wsdl.add_child('wsdl:message')
                message['name'] = "%s%s" % (method, m)
                part = message.add_child("wsdl:part")
                part[:] = {'name': 'parameters',
                           'element': 'tns:%s%s' % (method, e)}

        # create ports
        portType = wsdl.add_child('wsdl:portType')
        portType['name'] = "%sPortType" % self.name
        for method, (function, returns, args, doc) in self.methods.items():
            op = portType.add_child('wsdl:operation')
            op['name'] = method
            if doc:
                op.add_child("wsdl:documentation", doc)
            input = op.add_child("wsdl:input")
            input['message'] = "tns:%sInput" % method
            output = op.add_child("wsdl:output")
            output['message'] = "tns:%sOutput" % method

        # create bindings
        binding = wsdl.add_child('wsdl:binding')
        binding['name'] = "%sBinding" % self.name
        binding['type'] = "tns:%sPortType" % self.name
        soapbinding = binding.add_child('soap:binding')
        soapbinding['style'] = "document"
        soapbinding['transport'] = "http://schemas.xmlsoap.org/soap/http"
        for method in self.methods.keys():
            op = binding.add_child('wsdl:operation')
            op['name'] = method
            soapop = op.add_child('soap:operation')
            soapop['soapAction'] = self.action + method
            soapop['style'] = 'document'
            input = op.add_child("wsdl:input")
            ##input.add_attribute('name', "%sInput" % method)
            soapbody = input.add_child("soap:body")
            soapbody["use"] = "literal"
            output = op.add_child("wsdl:output")
            ##output.add_attribute('name', "%sOutput" % method)
            soapbody = output.add_child("soap:body")
            soapbody["use"] = "literal"

        service = wsdl.add_child('wsdl:service')
        service["name"] = "%sService" % self.name
        service.add_child('wsdl:documentation', text=self.documentation)
        port = service.add_child('wsdl:port')
        port["name"] = "%s" % self.name
        port["binding"] = "tns:%sBinding" % self.name
        soapaddress = port.add_child('soap:address')
        soapaddress["location"] = self.location
        return wsdl.as_xml(pretty=True)


class SOAPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """User viewable help information and wsdl"""
        args = self.path[1:].split("?")
        if self.path != "/" and args[0] not in self.server.dispatcher.methods.keys():
            self.send_error(404, "Method not found: %s" % args[0])
        else:
            if self.path == "/":
                # return wsdl if no method supplied
                response = self.server.dispatcher.wsdl()
            else:
                # return supplied method help (?request or ?response messages)
                req, res, doc = self.server.dispatcher.help(args[0])
                if len(args) == 1 or args[1] == "request":
                    response = req
                else:
                    response = res
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.end_headers()
            self.wfile.write(response)

    def do_POST(self):
        """SOAP POST gateway"""
        args = self.path[1:].split("?")
        request = self.rfile.read(int(self.headers.get('content-length')))
        # convert xml request to unicode (according to request headers)

        encoding = 'utf-8'
        request = request.decode(encoding)
        fault = {}
        # execute the method
        response = self.server.dispatcher.dispatch(request, fault=fault, method = args[0])
        # check if fault dict was completed (faultcode, faultstring, detail)
        if fault:
            self.send_response(500)
        else:
            self.send_response(200)
        if args[0] == 'rfromems':
            self.send_header("authenticate", "sqm123456sqm")
            self.send_header("version", "version523")
        self.send_header("Content-type", "text/xml")
        self.end_headers()
        self.wfile.write(response)


class WSGISOAPHandler(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, environ, start_response):
        return self.handler(environ, start_response)

    def handler(self, environ, start_response):
        if environ['REQUEST_METHOD'] == 'GET':
            return self.do_get(environ, start_response)
        elif environ['REQUEST_METHOD'] == 'POST':
            return self.do_post(environ, start_response)
        else:
            start_response('405 Method not allowed', [('Content-Type', 'text/plain')])
            return ['Method not allowed']

    def do_get(self, environ, start_response):
        path = environ.get('PATH_INFO').lstrip('/')
        query = environ.get('QUERY_STRING')
        if path != "" and path not in self.dispatcher.methods.keys():
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return ["Method not found: %s" % path]
        elif path == "":
            # return wsdl if no method supplied
            response = self.dispatcher.wsdl()
        else:
            # return supplied method help (?request or ?response messages)
            req, res, doc = self.dispatcher.help(path)
            if len(query) == 0 or query == "request":
                response = req
            else:
                response = res
        start_response('200 OK', [('Content-Type', 'text/xml'), ('Content-Length', str(len(response)))])
        return [response]

    def do_post(self, environ, start_response):
        length = int(environ['CONTENT_LENGTH'])
        request = environ['wsgi.input'].read(length)
        response = self.dispatcher.dispatch(request)
        start_response('200 OK', [('Content-Type', 'text/xml'), ('Content-Length', str(len(response)))])
        return [response]


if __name__ == "__main__":
    print('Connecting db and starting server...')
    dispatcher = SoapDispatcher(
        name="EPSoap",
        location="http://localhost:8008/",
        action='http://localhost:8008/',  # SOAPAction
        namespace="http://example.com/pysimplesoapsamle/", prefix="ns0",
        documentation='EPMailProcSystem',
        trace=True, debug=True,
        ns=True)
    global connection
    try:
        connection = pymysql.connect(host='1.1.1.64',
                                     user='mailer',
                                     password='test@007',
                                     db='mailstore',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
    except:
        log.info('Can not connect to db, pls check mysql server or user.')
        exit(2)

    def adder(p, c, dt=None):
        """Add several values"""
        dt = dt + datetime.timedelta(365)
        return {'ab': p['a'] + p['b'], 'dd': c[0]['d'] + c[1]['d'], 'dt': dt}

    def dummy(in0):
        """Just return input"""
        return in0

    def queryrfdmail(onceKey,distributorCode,logId):
        """Just return input"""
        print("jt3",onceKey)
        print("jt4:",distributorCode)
        return {'key':onceKey}

    def rfrom_ems(onceKey,distributorCode,logId):
        """Just return input"""
        print("jt3",onceKey)
        print("jt4:",distributorCode)
        return {'key':onceKey}

    def echo(request):
        """Copy request->response (generic, any type)"""
        return request.value

    dispatcher.register_function(
        'Adder', adder,
        returns={'AddResult': {'ab': int, 'dd': unicode, 'dt': datetime.date}},
        args={'p': {'a': int, 'b': int}, 'dt': Date, 'c': [{'d': Decimal}]}
    )

    dispatcher.register_function(
        'Dummy', dummy,
        returns={'out0': str},
        args={'in0': str}
    )

    dispatcher.register_function(
        'rfromems', rfrom_ems,
        returns={'out0': str},
        args={'in0': str}
    )
    dispatcher.register_function(
        'Queryrfdmail', queryrfdmail,
        returns={'out0': str},
        args={'in0': str}
    )
    dispatcher.register_function('Echo', echo)

    log.info("Server is running...ver:"+VERSION)
    httpd = HTTPServer(("", 8008), SOAPHandler)
    httpd.dispatcher = dispatcher
    httpd.serve_forever()

    connection.close()
