import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget


class CoffeeDBAddEdit(QWidget):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.main_window = main_window
        self.current_id = 0
        self.pushButton_Ok.clicked.connect(self._оk)
        self.pushButton_Cancel.clicked.connect(self._сancel)
        # self.change_data()

    def change_data(self):
        exec_str = 'SELECT * FROM Brands WHERE id = ' + str(self.current_id)
        cur = self.main_window.connection.cursor()
        element = cur.execute(exec_str).fetchone()
        if element is not None:
            element = element[1:]
            self.sort_edit.setText(element[0])
            self.degree_edit.setText(str(element[1]))
            self.ground_or_grains_box.setValue(element[2])
            self.flavor_edit.setText(element[3])
            self.price_box.setValue(element[4])
            self.volume_box.setValue(element[5])

    def _оk(self):
        sort = self.sort_edit.text()
        degree = self.degree_edit.text()
        ground_or_grains = self.ground_or_grains_box.value()
        flavor = self.flavor_edit.text()
        price = self.price_box.value()
        volume = self.volume_box.value()
        cur = self.main_window.connection.cursor()
        if self.current_id != 0:
            cur.execute("""
            UPDATE Brands
               SET Name = ?,
                   Strength = ?,
                   Beans = ?,
                   Description = ?,
                   Price = ?,
                   Volume = ?
             WHERE ID = ? 
            """, (sort, degree, ground_or_grains, flavor, price, volume, self.current_id))
        else:
            cur.execute("""
            INSERT INTO Brands (
                       Name,
                       Strength,
                       Beans,
                       Description,
                       Price,
                       Volume) VALUES (?, ?, ?, ?, ?, ?)
            """, (sort, degree, ground_or_grains, flavor, price, volume))
        self.main_window.connection.commit()
        self.main_window.select_data()
        self.close()

    def _сancel(self):
        self.close()


class CoffeeDB(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.add_edit_form = None
        self.pushButton_SetFilter.clicked.connect(self.select_data)
        self.pushButton_Add.clicked.connect(self.add_item)
        self.pushButton_Edit.clicked.connect(self.edit_item)
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

    def add_item(self):
        self.add_edit_form = CoffeeDBAddEdit(self)
        self.add_edit_form.current_id = 0
        self.add_edit_form.show()

    def edit_item(self):
        self.add_edit_form = CoffeeDBAddEdit(self)
        self.add_edit_form.current_id = self.tableWidget_Result.item(self.tableWidget_Result.currentRow(), 0).text()
        self.add_edit_form.change_data()
        self.add_edit_form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeDB()
    ex.show()
    sys.exit(app.exec())
