from column import Column


def input_table_name():
    print("enter the table name : ", end='')
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


def input_values(c_name):
    values = []

    for c in c_name:
        print("{} : ".format(c), end='')
        val = input()
        values.append(val)

    return values


def print_line(iterable):
    for item in iterable:
        print(item, end='\t\t')
    print()


def print_menus(t_names):
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


def print_table(t_name, c_name, contents):
    print('==============================')
    print("The Table contents of {}".format(t_name))
    print_line(c_name)
    print('==============================')

    for content in contents:
        print_line(content)

    print('==============================', end='\n\n')