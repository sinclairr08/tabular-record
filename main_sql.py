import pymysql
import sys

from sql_executor import SQLexecutor
from GUI import MainWindow

from PyQt5.QtWidgets import *


def get_id_pw(file_path):
    with open(file_path, 'r') as f:
        ID = f.readline().strip()
        PW = f.readline().strip()

    return ID, PW


def create_db(mysql_user, mysql_passwd):
    connector_db = pymysql.connect(
        user=mysql_user,
        passwd=mysql_passwd,
        host='127.0.0.1',
        charset='utf8'
    )

    try:
        with connector_db.cursor() as cursor:
            sql = 'CREATE DATABASE tabularec_db'
            cursor.execute(sql)
        connector_db.commit()

    finally:
        connector_db.close()


def get_table_column_names(mysql_user, mysql_passwd):
    connector_info = pymysql.connect(
        user=mysql_user,
        passwd=mysql_passwd,
        host='127.0.0.1',
        db='information_schema',
        charset='utf8'
    )

    t_names = []
    all_c_names = []

    try:
        with connector_info.cursor() as cursor:
            sql = 'select schema_name FROM schemata where schema_name = \'tabularec_db\''
            cursor.execute(sql)
            result = cursor.fetchall()

            if len(result) == 0:
                create_db(mysql_user, mysql_passwd)

            sql = 'select table_name FROM tables where table_schema = \'tabularec_db\''
            cursor.execute(sql)
            t_results = cursor.fetchall()

            t_names = [item[0] for item in t_results]

            for table in t_names:
                sql = 'SELECT column_name FROM columns WHERE table_name = %s'
                cursor.execute(sql, table)
                c_results = cursor.fetchall()

                all_c_names.append([item[0] for item in c_results])

    finally:
        connector_info.close()

    return t_names, all_c_names


if __name__ == "__main__":
    mysql_info_path = './sql_info.txt'

    mysql_user, mysql_passwd = get_id_pw(mysql_info_path)
    t_names, all_c_names = get_table_column_names(mysql_user, mysql_passwd)

    connector = pymysql.connect(
        user=mysql_user,
        passwd=mysql_passwd,
        host='127.0.0.1',
        db='tabularec_db',
        charset='utf8'
    )

    executor = SQLexecutor(connector)

    app = QApplication(sys.argv)
    window = MainWindow(executor, t_names, all_c_names)
    sys.exit(app.exec_())
