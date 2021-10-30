import pymysql
from CLI import *
from sql_executor import *


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
    c_names = []

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

                c_names.append([item[0] for item in c_results])

    finally:
        connector_info.close()

    return t_names, c_names


if __name__ == "__main__":
    mysql_info_path = './sql_info.txt'

    mysql_user, mysql_passwd = get_id_pw(mysql_info_path)
    t_names, c_names = get_table_column_names(mysql_user, mysql_passwd)

    connector = pymysql.connect(
        user=mysql_user,
        passwd=mysql_passwd,
        host='127.0.0.1',
        db='tabularec_db',
        charset='utf8'
    )

    while True:
        print_menus(t_names)
        mode = int(input())

        if mode == 1:
            t_name = input_table_name()

            if t_name in t_names:
                print("That table already exists. Try other name.")
                continue

            columns = input_columns()

            sql_execute_create_table(t_name, columns, connector)

            c_name = [col.name for col in columns]

            t_names.append(t_name)
            c_names.append(c_name)

        elif mode == 2:
            t_name = input_table_name()

            if t_name not in t_names:
                print("No such table")
                continue

            idx = t_names.index(t_name)
            values = input_values(c_names[idx])
            sql_execute_insert_value(t_name, values, connector)

        elif mode == 3:
            t_name = input_table_name()

            if t_name not in t_names:
                print("No such table")
                continue

            idx = t_names.index(t_name)

            results = sql_execute_select_all(t_name, connector)
            print_table(t_name, c_names[idx], results)

        elif mode == 0:
            print("Done")
            break

        else:
            print("No such mode")
