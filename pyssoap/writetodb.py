#author:jason chan
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

    with connection.cursor() as cursor:
        sql = "insert into maillist (serialnumber,mailnum,procdate,proctime,orgfullname,action,properdelivery,notproperdelivery,description,effect) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (serialnumber,mailnum,procdate,proctime,orgfullname,action,properdelivery,notproperdelivery,description,effect))
    connection.commit()

if __name__=="__main__":
    # Connect to the database
    try:
        connection = pymysql.connect(host='1.1.1.64',
                                     user='mailer',
                                     password='test@007',
                                     db='ems',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        for i in range(10):
            emsdict = []

            serialnumber = str(i).zfill(20)
            mailnum = 'LK434266003CN'
            procdate = '20130702'
            proctime = '000100'
            orgfullname = '所在地名称'
            action = '00'
            description = '描述信息'
            effect = '0'
            properdelivery = '12'
            notproperdelivery = '100'

            emsdict.append(serialnumber)
            emsdict.append(mailnum)
            emsdict.append(procdate)
            emsdict.append(proctime)
            emsdict.append(orgfullname)
            emsdict.append(action)
            emsdict.append(description)
            emsdict.append(effect)
            emsdict.append(properdelivery)
            emsdict.append(notproperdelivery)
            print (emsdict)
            emstodb(connection,emsdict)
    finally:
        connection.close()
