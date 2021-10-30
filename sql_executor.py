from sql_generator import sql_generate_insert_value, sql_generate_create_table


def sql_execute_create_table(t_name, columns, connector):
    with connector.cursor() as cursor:
        sql = sql_generate_create_table(t_name, columns)
        cursor.execute(sql)

    connector.commit()
    return


def sql_execute_insert_value(t_name, values, connector):
    with connector.cursor() as cursor:
        sql = sql_generate_insert_value(t_name, values)
        cursor.execute(sql, values)

    connector.commit()
    return


def sql_execute_select_all(t_name, connector):
    with connector.cursor() as cursor:
        sql = 'SELECT * FROM ' + t_name
        cursor.execute(sql)

        results = cursor.fetchall()

    return results
