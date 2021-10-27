import pymysql

mysql_user = 'WRITE YOUR USERNAME'
mysql_passwd = 'WRITE YOUR PASSWORD'


def print_line(list_elem):
    for elem in list_elem:
        print(elem, end='\t')
    print()


def show_menus(tables):
    print('==============================')
    print('Current Table List')
    print_line(tables)
    print('==============================')

    print("\nChoose a mode")
    print("1 : Create new table")
    print("2 : Insert record to the table")
    print("3 : Show records at a table")
    print("0 : exit")

    return


def input_table_name():
    print("enter the table name : ")
    table_name = input()

    return table_name


def input_column_names():
    c_idx = 1
    c_names = []

    print("Enter the column names. If you want to stop, press '\\'")

    while True:
        print("column {} : ".format(c_idx), end='')
        c_name = input()

        if c_name == '\\':
            break

        c_names.append(c_name)
        c_idx += 1

    if c_idx <= 1:
        print("No columns are added")
        exit()

    return c_names


def sqlgen_create_table(table_name, columns):
    num_iter = len(columns)

    sql = 'CREATE TABLE ' + table_name + ' (\n'
    for i in range(num_iter - 1):
        sql += columns[i] + ' varchar(255),\n'

    sql += columns[num_iter - 1] + ' varchar(255)) CHARSET=utf8'

    return sql


def sqlgen_insert_value(table_name, values):
    num_iter = len(values)

    sql = 'INSERT INTO ' + table_name + ' VALUES ('
    for i in range(num_iter - 1):
        sql += '%s, '

    sql += '%s)'

    return sql


def create_table(tables, columns, connector):
    table_name = input_table_name()

    if table_name in tables:
        print("That table already exists. Try other name.")
        return

    input_columns = input_column_names()
    with connector.cursor() as cursor:
        sql = sqlgen_create_table(table_name, input_columns)
        cursor.execute(sql)

    connector.commit()

    tables.append(table_name)
    columns.append(input_columns)
    return


def insert_value(tables, columns, connector):
    table_name = input_table_name()

    if table_name not in tables:
        print("No such table")
        return

    idx = tables.index(table_name)
    values = []

    for column in columns[idx]:
        print("{} : ".format(column))
        val = input()
        values.append(val)

    with connector.cursor() as cursor:
        sql = sqlgen_insert_value(table_name, values)
        cursor.execute(sql, values)

    connector.commit()
    return


def select_all(tables, columns, connector):
    table_name = input_table_name()

    if table_name not in tables:
        print("No such table")
        return

    idx = tables.index(table_name)
    print_line(columns[idx])

    with connector.cursor() as cursor:
        sql = 'SELECT * FROM ' + table_name
        cursor.execute(sql)

        results = cursor.fetchall()

    for result in results:
        print_line(result)


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


def get_table_columns():
    connector_info = pymysql.connect(
        user='root',
        passwd='praymeier12@%',
        host='127.0.0.1',
        db='information_schema',
        charset='utf8'
    )

    tables = []
    columns = []

    try:
        with connector_info.cursor() as cursor:
            sql = 'select schema_name FROM schemata where schema_name = \'tabularec_db\''
            cursor.execute(sql)
            result = cursor.fetchall()

            if len(result) == 0:
                create_db()

            sql = 'select table_name FROM tables where table_schema = \'tabularec_db\''
            cursor.execute(sql)
            result_table = cursor.fetchall()

            tables = [item[0] for item in result_table]

            for table in tables:
                sql = 'SELECT column_name FROM columns WHERE table_name = %s'
                cursor.execute(sql, table)
                result_column = cursor.fetchall()

                columns.append([item[0] for item in result_column])

    finally:
        connector_info.close()

    return tables, columns


if __name__ == "__main__":
    tables, columns = get_table_columns()

    connector = pymysql.connect(
        user=mysql_user,
        passwd=mysql_passwd,
        host='127.0.0.1',
        db='tabularec_db',
        charset='utf8'
    )

    while True:
        show_menus(tables)
        mode = int(input())

        if mode == 1:
            create_table(tables, columns, connector)

        elif mode == 2:
            insert_value(tables, columns, connector)

        elif mode == 3:
            select_all(tables, columns, connector)

        elif mode == 0:
            print("Done")
            break

        else:
            print("No such mode")
