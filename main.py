import sqlite3 as sql
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAction
from interface import Ui_MainWindow
from addeditform_program import AskWidget
from PyQt5 import QtWidgets
import sys


class Database:
    def __init__(self, name_of_database=None):
        self.name = name_of_database

    def change_name(self, name_of_database=None):
        self.name = name_of_database

    def direct_sql_request(self, sql_request):
        con = sql.connect(self.name)
        cur = con.cursor()

        if 'UPDATE' in sql_request or 'INSERT' in sql_request:
            result = cur.execute(sql_request)
        else:
            result = cur.execute(sql_request).fetchall()

        con.close()

        return result

    def return_all_values(self, name_of_table):
        return self.direct_sql_request(f"""SELECT * FROM {name_of_table}""")

    def __str__(self):
        if self.name is None:
            return 'Non-defined Database'
        else:
            return f'Database: {self.name}'

    def __repr__(self):
        if self.name is None:
            return f'Database(name_of_database=None)'
        else:
            return f'Database(name_of_database=\'{self.name}\')'


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self, name_of_database):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('Coffees')
        self.database = Database(name_of_database)
        self.create_table()
        self.create_menubar()

    def create_table(self):
        all_coffees = self.database.return_all_values('coffee_types')

        labels = ['Name', 'Degree', 'Ground/Beans',
                  'Description of taste', 'Price', 'Volume']
        self.table.setColumnCount(len(labels))
        self.table.setRowCount(len(all_coffees))
        self.table.setHorizontalHeaderLabels(labels)

        for i, row in enumerate(all_coffees):
            for j, el in enumerate(row):
                if j != 0:
                    self.table.setItem(i, j - 1, QTableWidgetItem(str(el)))

        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Fixed)

    def create_menubar(self):
        self.menu_bar = self.menuBar()

        fileMenu = self.menu_bar.addMenu('&File')

        new_action = QAction('Update data in table', self)
        new_action.triggered.connect(self.update_the_base)
        fileMenu.addAction(new_action)

    def update_the_base(self):
        self.widg = AskWidget(self.database, self.table.rowCount(), self)
        self.widg.show()

        # self.create_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program('coffee.sqlite')
    ex.show()
    sys.exit(app.exec())
