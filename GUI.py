from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Mainlayout(QWidget):
    def __init__(self, executor):
        super().__init__()

        self.executor = executor
        self.t_names, self.all_c_infos = executor.get_infos()

        self.layout_btns = QVBoxLayout()
        self.setButtons()

        self.table_widget = QTableWidget(self)
        self.t_info_header = ['연번', '테이블명']
        self.t_info_data = self.make_t_info_data()
        self.show_tables()

        self.msgbox = QMessageBox()
        self.msgbox.setGeometry(250, 250, 200, 200)
        self.msgbox.setIcon(QMessageBox.Information)

        layout_main = QHBoxLayout()

        layout_main.addLayout(self.layout_btns)
        layout_main.addWidget(self.table_widget)

        self.setLayout(layout_main)

    def make_t_info_data(self):
        t_info_data = []
        for i, data in enumerate(self.t_names):
            t_info_data.append([str(i+1), data])

        return t_info_data

    def setButtons(self):
        self.create_table_btn = QPushButton("Create Table")
        self.insert_record_btn = QPushButton("Insert Record")
        self.show_records_btn = QPushButton("Show Records")
        self.show_tables_btn = QPushButton("Show Tables")

        self.create_table_btn.clicked.connect(self.create_table)
        self.insert_record_btn.clicked.connect(self.insert_record)
        self.show_records_btn.clicked.connect(self.show_records)
        self.show_tables_btn.clicked.connect(self.show_tables)

        self.layout_btns.addWidget(self.create_table_btn)
        self.layout_btns.addWidget(self.insert_record_btn)
        self.layout_btns.addWidget(self.show_records_btn)
        self.layout_btns.addWidget(self.show_tables_btn)

    def create_table(self):
        t_name, _ = QInputDialog.getText(self, "Create Table", "Enter the table name : ")
        if t_name in self.t_names:
            self.msgbox.setText("Name already exists. Try other name.")
            self.msgbox.exec_()
            return

        c_num, _ = QInputDialog.getInt(self, "Create Table", "Enter the column nums : ")
        c_infos = []

        for _ in range(c_num):
            c_name, _ = QInputDialog.getText(self, "Create Table", "Enter the column name : ")
            c_type, _ = QInputDialog.getText(self, "Create Table", "Enter the type of {} : ".format(c_name))

            c_type = self.executor.adjust_type(c_type)
            c_infos.append((c_name, c_type))

        self.executor.create_table(t_name, c_infos)

        t_nums = len(self.t_info_data) + 1
        self.t_info_data.append([str(t_nums), t_name])

        self.t_names.append(t_name)
        self.all_c_infos.append(c_infos)

        self.show_tables()

    def insert_record(self):
        t_name, _ = QInputDialog.getText(self, "Insert Record", "Enter the table name : ")
        if t_name in self.t_names:
            c_infos = self.get_c_infos(t_name)

        else:
            self.msgbox.setText("No such table")
            self.msgbox.exec_()
            return

        values = []
        for c_name, c_type in c_infos:
            value, _ = QInputDialog.getText(self, "Insert Record", "Enter the data of col {} ({}): ".format(c_name, c_type))
            values.append(value)

        self.executor.insert_value(t_name, values)

    def show_records(self):
        t_name, _ = QInputDialog.getText(self, "Show Records", "Enter the table name : ")

        if t_name in self.t_names:
            c_names = self.get_c_names(t_name)

        else:
            self.msgbox.setText("No such table")
            self.msgbox.exec_()
            return

        t_data = self.executor.select_all(t_name)

        self.adjust_table(c_names, t_data)

    def get_c_infos(self, t_name):
        idx = self.t_names.index(t_name)
        return self.all_c_infos[idx]

    def get_c_names(self, t_name):
        idx = self.t_names.index(t_name)
        c_names = [item[0] for item in self.all_c_infos[idx]]
        return c_names

    def show_tables(self):
        self.adjust_table(self.t_info_header, self.t_info_data)

    def adjust_table(self, header, data):
        row = len(data)
        col = len(header)

        self.table_widget.clear()

        self.table_widget.setRowCount(row)
        self.table_widget.setColumnCount(col)
        self.table_widget.setHorizontalHeaderLabels(header)

        for i in range(row):
            for j in range(col):
                item = QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(i, j, item)

        self.table_widget.resizeRowsToContents()
        self.table_widget.resizeColumnsToContents()


class MainWindow(QMainWindow):
    def __init__(self, executor):
        super().__init__()

        layout = Mainlayout(executor)
        self.setCentralWidget(layout)

        self.setWindowTitle("Tabularec")
        self.setGeometry(200, 200, 300, 200)
        self.show()

