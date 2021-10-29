class Column:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.sql = ''
        self.is_not_null = True
        self.is_unique = False
        self.is_PK = False

        self.type_candidate = ['INT', 'FLOAT', 'VARCHAR']

    def input_column(self):
        print("Enter the column name : ", end='')
        self.name = input()

        while True:
            print("Enter the type name; Name should be INT, VARCHAR or FLOAT")
            type_name = input()

            if type_name not in self.type_candidate:
                print("Wrong type format!")
                continue

            self.type = type_name

            if type_name == 'VARCHAR':
                self.type += '(255)'
            elif type_name == 'INT':
                self.type += '(11)'
            elif type_name == 'FLOAT':
                self.type += '(16)'
            break

        print("Is null allowed? If yes, enter anything : ", end='')
        is_null = input()
        if is_null:
            self.is_not_null = False

        print("Is it UNIQUE? If yes, enter anything : ", end='')
        is_unique = input()
        if is_unique:
            self.is_unique = True

        print("Is it PK? If yes, enter anything : ", end='')
        is_PK = input()
        if is_PK:
            self.is_PK = True

    def sqlgen_create_table_column(self):
        self.sql += self.name + ' '
        self.sql += self.type + ' '
        if self.is_PK:
            self.sql += 'PRIMARY KEY'

        else:
            if self.is_unique:
                self.sql += 'UNIQUE '

            if self.is_not_null:
                self.sql += 'NOT NULL '

        return self.sql