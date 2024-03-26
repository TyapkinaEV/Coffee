import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class CoffeeDB(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.pushButton_SetFilter.clicked.connect(self.select_data)
        self.select_data()

    def select_data(self):
        filtertext = "%" + self.lineEdit_SearchText.text() + "%"
        res = self.connection.cursor().execute("""
            SELECT * FROM Brands WHERE Name Like ? or Description Like ?
            """, (filtertext, filtertext)).fetchall()
        self.tableWidget_Result.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget_Result.setRowCount(
                self.tableWidget_Result.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_Result.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeDB()
    ex.show()
    sys.exit(app.exec())
