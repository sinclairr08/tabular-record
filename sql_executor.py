class SQLexecutor():
    def __init__(self, connector, cursor):
        self.connector = connector
        self.cursor = cursor
        self.type_list = ['TEXT', 'NUMERIC', 'INTEGER', 'REAL', 'NONE']
        self.other_list = ['VARCHAR', 'NUM', 'INT', 'FLOAT']

        self.t_names = []
        self.all_c_infos = []

        self.set_infos()

    def set_infos(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(sql)
        t_results = self.cursor.fetchall()

        for t_result in t_results:
            sql = "SELECT sql FROM sqlite_master WHERE tbl_name = ?"
            self.cursor.execute(sql, t_result)
            c_results = self.cursor.fetchall()

            parsed = c_results[0][0].split('\n')

            c_infos = []
            for info in parsed[1:]:
                c_name_type = info.split(' ')
                c_name = c_name_type[0]
                c_type = c_name_type[1][:-1]  # :-1 deletes the punctuations in SQL

                c_infos.append((c_name, c_type))

            self.t_names.append(t_result[0])
            self.all_c_infos.append(c_infos)

        return

    def get_infos(self):
        return self.t_names, self.all_c_infos

    def create_table(self, t_name, c_infos):
        sql = self.sql_create_table(t_name, c_infos)
        self.cursor.execute(sql)
        self.connector.commit()

        return

    def insert_value(self, t_name, values):
        sql = self.sql_insert_value(t_name, values)
        self.cursor.execute(sql, values)
        self.connector.commit()

        return

    def select_all(self, t_name):
        sql = 'SELECT * FROM ' + t_name
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        return results

    def adjust_type(self, c_type):
        c_type = c_type.upper()
        if not c_type:
            return 'TEXT'

        elif c_type in self.type_list:
            return c_type

        elif c_type in self.other_list:
            idx = self.other_list.index(c_type)
            return self.type_list[idx]

        else:
            return 'NONE'

    @staticmethod
    def sql_create_table(t_name, c_infos):
        num_iter = len(c_infos)

        sql = 'CREATE TABLE ' + t_name + ' (\n'
        for i in range(num_iter - 1):
            sql += c_infos[i][0] + ' '
            sql += c_infos[i][1] + ',\n'

        sql += c_infos[num_iter - 1][0] + ' '
        sql += c_infos[num_iter - 1][1] + ')'

        return sql

    @staticmethod
    def sql_insert_value(t_name, values):
        num_iter = len(values)

        sql = 'INSERT INTO ' + t_name + ' VALUES ('
        for i in range(num_iter - 1):
            sql += '?, '

        sql += '?)'

        return sql
