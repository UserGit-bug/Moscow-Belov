import sqlite3 as sql
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import QtWidgets, QtCore
import sys


class Database:
    def __init__(self, name_of_database=None):
        self.name = name_of_database

    def change_name(self, name_of_database=None):
        self.name = name_of_database

    def direct_sql_request(self, sql_request):
        con = sql.connect(self.name)
        cur = con.cursor()

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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self, name_of_database):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('Coffees')
        self.database = Database(name_of_database)
        self.create_table()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program('coffee.sqlite')
    ex.show()
    sys.exit(app.exec())
