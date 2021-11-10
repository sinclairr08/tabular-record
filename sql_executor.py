class SQLexecutor():
    def __init__(self, connector):
        self.connector = connector

    def create_table(self, t_name, c_names, c_types):
        with self.connector.cursor() as cursor:
            sql = self.sql_create_table(t_name, c_names, c_types)
            cursor.execute(sql)

        self.connector.commit()
        return

    def insert_value(self, t_name, values):
        with self.connector.cursor() as cursor:
            sql = self.sql_insert_value(t_name, values)
            cursor.execute(sql, values)

        self.connector.commit()
        return

    def select_all(self, t_name):
        with self.connector.cursor() as cursor:
            sql = 'SELECT * FROM ' + t_name
            cursor.execute(sql)

            results = cursor.fetchall()

        return results

    def sql_create_table(self, t_name, c_names, c_types):
        num_iter = len(c_names)

        sql = 'CREATE TABLE ' + t_name + ' (\n'
        for i in range(num_iter - 1):
            sql += c_names[i] + ' '
            sql += c_types[i] + '({})'.format(self.gettypelen(c_types[i]))
            sql += ',\n'

        sql += c_names[num_iter - 1] + ' '
        sql += c_types[num_iter - 1] + '({})'.format(self.gettypelen(c_types[num_iter - 1]))
        sql += ') CHARSET=utf8'

        return sql

    def gettypelen(self, type):
        if type == 'VARCHAR':
            return 255
        elif type == 'INT':
            return 11
        elif type == 'FLOAT':
            return 16
        else:
            return 255


    def sql_insert_value(self, t_name, values):
        num_iter = len(values)

        sql = 'INSERT INTO ' + t_name + ' VALUES ('
        for i in range(num_iter - 1):
            sql += '%s, '

        sql += '%s)'

        return sql