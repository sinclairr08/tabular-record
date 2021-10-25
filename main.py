import os


def parse_tokens(line, parser):
    columns = [word.strip() for word in line.split(parser)]
    return columns


if __name__ == "__main__":
    table_path = "./tables/"
    if not os.path.isdir(table_path):
        os.mkdir(table_path)

    while True:
        print("Choose a mode")
        print("1 : Create a table, 2 : Show tables, 3 : Show certain table, 4 : Write table, 0 : exit")

        mode = int(input())

        if mode == 1:
            print("enter the table name : ")
            table_name = input()

            if os.path.isfile(table_path + table_name + '.txt'):
                print("That table already exists. Try other name.")
                continue

            with open(table_path + table_name + ".txt", 'w') as f:
                print("enter the column names; seperate them as |")
                first_line = input()
                f.write(first_line+ '\n')

        elif mode == 2:
            file_list = os.listdir(table_path)
            print(file_list)

        elif mode == 3:
            print("enter the table name : ")
            table_name = input()

            if not os.path.isfile(table_path + table_name + '.txt'):
                print("No such table")

            with open(table_path + table_name + ".txt", 'r') as f:
                line = f.readline()
                while line:
                    print(line, end ='')
                    line = f.readline()

        elif mode == 4:
            print("enter the table name : ")
            table_name = input()

            if not os.path.isfile(table_path + table_name + '.txt'):
                print("No such table")

            with open(table_path + table_name + ".txt", 'r') as f:
                first_line = f.readline()

                first_columns = parse_tokens(first_line, "|")
                first_num_columns = len(first_columns)

            with open(table_path + table_name + ".txt", 'a') as f:
                print("enter the record")

                input_line = input()
                input_columns = parse_tokens(line, '|')
                input_num_columns = len(input_columns)

                if input_num_columns != first_num_columns:
                    print("wrong format")

                else:
                    f.write(line + '\n')

        elif mode == 0:
            print("Done")
            break

        else:
            print("No such mode")
