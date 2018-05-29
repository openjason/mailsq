#!/usr/bin/python
# -*- coding: utf-8 -*-
# 物流信息接收处理系统
# 系统是一个物流信息中转系统，主要是接收在物流公司实时发送的http-post报文，保存在数据库，
# 系统在客户查询的时候返回最新的物流信息，也支持主动批量将物流信息发送给客户指定网络接口。
# 系统处理数据量大，百万条记录以上，实时性要求高，要及时处理报文，以免影响报文的接收和发送。
# 报文发送和接收有验证机制，接口地址判断，头信息，授权码等方式确认报文来源验证。
#
# mysql数据库表结构导出
# 命令行下具体用法如下：
# mysqldump - u用戶名 - p密码 - d
# 导出整个数据库结构和数据
# mysqldump - h localhost - uroot - p123456 database > dump.sql
#
# 导出单个数据表结构和数据
# mysqldump - h localhost - uroot - p123456 database table > dump.sql
#
# 导出整个数据库结构（不包含数据）
# / usr / local / mysql / bin / mysqldump - uroot - d entrym > dump.sql
# 导出单个数据表结构（不包含数据）
# mysqldump - h localhost - uroot - p123456 - d database table > dump.sql

# 文本文件数据导入MYSQL：
# load data local infile 'filename.txt' into table tablename(field1,field2,field3)
# 如果文本数据用空格分开，硬回车结束，可不加下面的命令：
#   FIELDS TERMINATED BY ':'
#   LINES TERMINATED BY '\r\n';
# mysqlimport客户端提供了LOAD DATA INFILE SQL语句的一个命令行接口。mysqlimport的大多数选项直接对应LOAD DATA INFILE子句。
#
# 一次插入多条数据，可用values后更多条值，用小括号包含每条数据，用逗号分开。
# insert into normalcode(code,detail) values('11','本人收'),('12','单位收发章'),('13','未出口退回妥投'),('14','退回妥投')
# grant all on mailstore.* to mailer@'%';
# show grants for mailer@'%';
# revoke all on mailstore.* form mailer@'%';
# 命令生效：flush privileges;

#author: jason chan

'''
CREATE TABLE `maillist` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`serialnumber` CHAR(20) NOT NULL,
	`mailnum` CHAR(20) NOT NULL,
	`procdate` DATE NOT NULL,
	`proctime` TIME(6) NOT NULL,
	`orgfullname` CHAR(6) NOT NULL,
	`action` CHAR(2) NOT NULL,
	`properdelivery` CHAR(3) NOT NULL,
	`notproperdelivery` CHAR(3) NOT NULL,
	`description` VARCHAR(512) NULL DEFAULT NULL,
	`effect` CHAR(1) NOT NULL,
	`success` CHAR(1) NULL DEFAULT NULL,
	`failmailnums` CHAR(255) NULL DEFAULT NULL,
	`remark` TEXT NULL,
	PRIMARY KEY (`id`),
	INDEX `Index 1` (`mailnum`)
)
COMMENT='listexpressmail'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=10752
;

'''

import pymysql.cursors

def emstodb(connection,emsdict):
    # （已转换为列表形式）接收的ems报文插入到数据库
    serialnumber = emsdict[0]
    mailnum = emsdict[1]
    procdate = emsdict[2]
    proctime = emsdict[3]
    orgfullname = emsdict[4]
    action = emsdict[5]
    description = emsdict[6]
    effect = emsdict[7]
    properdelivery = emsdict[8]
    notproperdelivery = emsdict[9]
    try:
        with connection.cursor() as cursor:
            sql = "insert into emslist (serialnumber,mailnum,procdate,proctime,orgfullname,action,properdelivery,notproperdelivery,description,effect) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (serialnumber,mailnum,procdate,proctime,orgfullname,action,properdelivery,notproperdelivery,description,effect))
        connection.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

def query_ems(connection,ems_mail_num):
    # （已转换为列表形式）接收的ems报文插入到数据库
    rstr_all = []
    try:
        with connection.cursor() as cursor:
            sql = "select serialnumber,mailnum,procdate,proctime,orgfullname,action,properdelivery,\
notproperdelivery,description,effect from emslist where mailnum='%s' order by procdate desc,proctime desc"%(ems_mail_num)

            #            print("sql:",sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                rstr_one = []
                serialnumber = row['serialnumber']
                mailnum = row['mailnum']
                procdate = row['procdate']
                proctime = row['proctime']
                orgfullname = row['orgfullname']
                action = row['action']
                description = row['description']
                effect = row['effect']
                properdelivery = row['properdelivery']
                notproperdelivery = row['notproperdelivery']

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
    except:
        return "error in query ems mail record."
#    print(rstr_all)
    return rstr_all

if __name__=="__main__":
    # Connect to the database
    try:
        connection = pymysql.connect(host='1.1.1.64',
                                     user='mailer',
                                     password='test@007',
                                     db='mailstore',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
#### test for write db
        # for i in range(10):
        #     emsdict = []
        #     serialnumber = str(i).zfill(20)
        #     mailnum = 'LK434266003CN'
        #     procdate = '20130702'
        #     proctime = '000100'
        #     orgfullname = '所在地名称'
        #     action = '00'
        #     description = '描述信息'
        #     effect = '0'
        #     properdelivery = '12'
        #     notproperdelivery = '100'
        #
        #     emsdict.append(serialnumber)
        #     emsdict.append(mailnum)
        #     emsdict.append(procdate)
        #     emsdict.append(proctime)
        #     emsdict.append(orgfullname)
        #     emsdict.append(action)
        #     emsdict.append(description)
        #     emsdict.append(effect)
        #     emsdict.append(properdelivery)
        #     emsdict.append(notproperdelivery)
        #     print (emsdict)
#            emstodb(connection,emsdict)

# test for query_ems_record.
        ret = query_ems(connection,'LK542000001CN')
        for r in ret:
            print(r)

    except:
        print("error.")

    finally:
        connection.close()
