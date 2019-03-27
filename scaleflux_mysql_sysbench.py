# -*- coding: utf-8 -*-
# Sam Wu
# 2019-3-27
# For ScaleFlux SE interview

import subprocess
import pymysql
import logging

logging.basicConfig(filename="sysbench_mysql_log.txt",
                    level=logging.INFO,
                    filemode='w',
                    format='%(asctime)s - %(levelname)s: %(message)s'
                    )


USER = "sbtest"
PASSWORD = "123456"
HOST = "192.168.1.18"
PORT = 3306
TEST_DATABASE_NAME = "tempdb"
TESTLIST = ["bulk_insert","oltp_read_only","oltp_delete", "oltp_insert",
            "oltp_point_select", "oltp_write_only", "oltp_update_index", "oltp_update_non_index",
            "oltp_read_write", "select_random_points", "select_random_ranges"]


def connect_sqlserver(host, port, usr, passwd):
    try:
        db = pymysql.connect(host=host, port=port, user=usr, password=passwd)
        logging.info("connect to {} with username {} successfully!".format(HOST, USER))
    except:
        logging.error("connect to {} with username {} fail!!!".format(HOST, USER))
    return db


def format_output(s):
    list = s.split("\\n")
    for i in list:
        logging.info(i)


def create_database (name):
    sql_cmd = "create database {}".format(name)
    logging.info(sql_cmd)
    db = connect_sqlserver(HOST,PORT,USER,PASSWORD)
    cur = db.cursor()
    try:
        cur.execute(sql_cmd)
        logging.info("create database {} successful!".format(name))
    except:
        logging.warning("database {} already exists".format(name))
    finally:
        cur.close()
        db.close()


def delect_database (name):

    sql_cmd = "drop database {}".format(name)
    logging.info(sql_cmd)
    db = connect_sqlserver(HOST,PORT,USER,PASSWORD)
    cur = db.cursor()
    try:
        cur.execute(sql_cmd)
        logging.info("delect database {} successful!".format(name))
    except:
        logging.error("database {} delect fail!!!".format(name))
    finally:
        cur.close()
        db.close()


def sysbench_mysql(testlist):

    for test in testlist:
        logging.info("##########START {} TEST##########:".format(test))
        cmd = "sysbench --db-driver=mysql --mysql-host={} --mysql-port={}\
         --mysql-user={} --mysql-password={} \
         --mysql-db={} {}".format(HOST, PORT, USER, PASSWORD, TEST_DATABASE_NAME, test)
        logging.info(cmd)
        p = subprocess.Popen(cmd + " prepare", shell=True)
        p.wait()
        r = subprocess.Popen(cmd + " run", stdout=subprocess.PIPE, shell=True)
        r.wait()
        format_output(str(r.communicate()[0]))
        c = subprocess.Popen(cmd + " cleanup", shell=True)
        c.wait()
        logging.info("##########TEST {} IS DONE##########".format(test))




if __name__ == '__main__':
    sysbench_mysql(TESTLIST)



