#author:jasonchan
# import urllib.request
# a_url = 'http://www.webxml.com.cn/WebServices/TrainTimeWebService.asmx?wsdl'
# a_url = 'http://www.webxml.com.cn/WebServices/MobileCodeWS.asmx?op=getMobileCodeInfo'
# dataraw = urllib.request.urlopen(a_url).read()
# type(dataraw)
# data = dataraw.decode("utf-8")
# print(data)
import pymysql.cursors

# Connect to the database
serialnumber = '0000000000000001'
mailnum = 'LK434266003CN'
procdate = '20130702'
proctime = '000100'
orgfullname = '所在地名称'
action = '00'
description = '描述信息'
effect = '0'
properdelivery = '12'
notproperdelivery = '100'

connection = pymysql.connect(host='1.1.1.64',
                             user='mailer',
                             password='Admin@007',
                             db='ems',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    for i in range(400):
        serialnumber = str(i).zfill(20)
        with connection.cursor() as cursor:
            sql = "insert into maillist (serialnumber,mailnum,procdate,proctime,orgfullname,action,properdelivery,notproperdelivery,description,effect) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (serialnumber,mailnum,procdate,proctime,orgfullname,action,properdelivery,notproperdelivery,description,effect))

        connection.commit()
finally:
    connection.close()
