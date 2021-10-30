def sql_generate_create_table(t_name, columns):
    num_iter = len(columns)

    sql = 'CREATE TABLE ' + t_name + ' (\n'
    for i in range(num_iter - 1):
        sql += columns[i].sqlgen_create_table_column() + ',\n'

    sql += columns[num_iter - 1].sqlgen_create_table_column() + ') CHARSET=utf8'

    return sql


def sql_generate_insert_value(t_name, values):
    num_iter = len(values)

    sql = 'INSERT INTO ' + t_name + ' VALUES ('
    for i in range(num_iter - 1):
        sql += '%s, '

    sql += '%s)'

    return sql