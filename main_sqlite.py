import sqlite3
import sys

from sql_executor import SQLexecutor
from GUI import MainWindow

from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    connector = sqlite3.connect("tabularec.db")
    cursor = connector.cursor()

    executor = SQLexecutor(connector, cursor)

    app = QApplication(sys.argv)
    window = MainWindow(executor)
    sys.exit(app.exec_())
