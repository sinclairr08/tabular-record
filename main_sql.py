import pymysql
from column import Column
from utility import print_line

mysql_user = 'WRITE YOUR USERNAME'
mysql_passwd = 'WRITE YOUR PASSWORD'


def show_menus(t_names):
    print('==============================')
    print('Current Table List')
    print_line(t_names)
    print('==============================')

    print("\nChoose a mode")
    print("1 : Create new table")
    print("2 : Insert record to the table")
    print("3 : Show records at a table")
    print("0 : exit")

    return


def input_table_name():
    print("enter the table name : ")
    t_name = input()

    return t_name


def input_columns():
    columns = []

    print("Enter the number of columns : ", end = '')
    num_column = int(input())

    for i in range(num_column):
        new_column = Column()
        new_column.input_column()

        columns.append(new_column)

    return columns


def sqlgen_create_table(t_name, columns):
    num_iter = len(columns)

    sql = 'CREATE TABLE ' + t_name + ' (\n'
    for i in range(num_iter - 1):
        sql += columns[i].sqlgen_create_table_column() + ',\n'

    sql += columns[num_iter - 1].sqlgen_create_table_column() + ') CHARSET=utf8'

    return sql


def sqlgen_insert_value(t_name, values):
    num_iter = len(values)

    sql = 'INSERT INTO ' + t_name + ' VALUES ('
    for i in range(num_iter - 1):
        sql += '%s, '

    sql += '%s)'

    return sql


def create_table(t_name, connector):
    columns = input_columns()

    with connector.cursor() as cursor:
        sql = sqlgen_create_table(t_name, columns)
        cursor.execute(sql)

    connector.commit()
    c_name = [col.name for col in columns]

    return c_name


def insert_value(t_name, c_name, connector):
    values = []

    for c in c_name:
        print("{} : ".format(c))
        val = input()
        values.append(val)

    with connector.cursor() as cursor:
        sql = sqlgen_insert_value(t_name, values)
        cursor.execute(sql, values)

    connector.commit()
    return


def select_all(t_name, c_name, connector):
    print('==============================')
    print("The Table contents of {}".format(t_name))
    print_line(c_name)
    print('==============================')

    with connector.cursor() as cursor:
        sql = 'SELECT * FROM ' + t_name
        cursor.execute(sql)

        results = cursor.fetchall()

    for result in results:
        print_line(result)

    print('==============================', end = '\n\n')


def create_db():
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


def get_table_column_names():
    connector_info = pymysql.connect(
        user='root',
        passwd='praymeier12@%',
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
                create_db()

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
    t_names, c_names = get_table_column_names()

    connector = pymysql.connect(
        user=mysql_user,
        passwd=mysql_passwd,
        host='127.0.0.1',
        db='tabularec_db',
        charset='utf8'
    )

    while True:
        show_menus(t_names)
        mode = int(input())

        if mode == 1:
            t_name = input_table_name()

            if t_name in t_names:
                print("That table already exists. Try other name.")
                continue

            c_name = create_table(t_name, connector)

            t_names.append(t_name)
            c_names.append(c_name)

        elif mode == 2:
            t_name = input_table_name()

            if t_name not in t_names:
                print("No such table")
                continue

            idx = t_names.index(t_name)
            insert_value(t_name, c_names[idx], connector)

        elif mode == 3:
            t_name = input_table_name()

            if t_name not in t_names:
                print("No such table")
                continue

            idx = t_names.index(t_name)
            select_all(t_name, c_names[idx], connector)

        elif mode == 0:
            print("Done")
            break

        else:
            print("No such mode")
