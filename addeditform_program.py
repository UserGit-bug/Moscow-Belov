from addeditform_interface import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication
import sys


class AskWidget(QWidget, Ui_Form):
    id_line_remember_value = str()

    def __init__(self, database, max_id, self_table):
        super().__init__()
        self.setupUi(self)
        self.database = database
        self.max_id = max_id
        self.table = self_table

        self.setWindowTitle('Update data')
        self.radio_buttons.buttonClicked.connect(self.update_insert_buttons)
        self.update_radio.click()

        self.download_button.clicked.connect(self.download_button_was_clicked)

    def update_insert_buttons(self, button):
        if button.objectName() == self.insert_radio.objectName():
            self.id_line.setReadOnly(True)
            self.id_line_remember_value = self.id_line.text()
            self.id_line.setText('')
        else:
            self.id_line.setReadOnly(False)
            self.id_line.setText(self.id_line_remember_value)

    def download_button_was_clicked(self):
        new_id = self.id_line.text()
        new_name = self.name_line.text()
        new_degree = self.degree_line.text()
        new_grounds = self.groundbeans_line.text()
        new_desc = self.desc_line.text()
        new_price = self.price_line.text()
        new_volume = self.volume_line.text()

        if self.update_radio.isChecked():
            if not new_id.isdigit():
                print('id must be integer')
                return None
            if int(new_id) > self.max_id:
                print('id cannot be so big')
                return None

        if not new_price.isdigit():
            print('Price must be integer')
            return None

        if not new_volume.isdigit():
            print('Volume must be integer')
            return None

        if not new_name:
            print('Name cannot be empty')
            return None

        if not new_degree:
            print('Degree cannot be empty')
            return None

        if not new_grounds:
            print('Ground/Beans cannot be empty')
            return None

        if self.update_radio.isChecked():
            self.database.direct_sql_request(f"""UPDATE coffee_types
                                                SET sortname = '{new_name}',
                                                roastdegree = '{new_degree}',
                                                groundbeans = '{new_grounds}',
                                                description = '{new_desc}',
                                                price = {int(new_price)},
                                                size = {new_volume}
                                                WHERE id = {new_id}""")
        else:
            self.database.direct_sql_request(f"""INSERT INTO coffee_types
                                                VALUES
                                                ({self.max_id + 1}, '{new_name}', 
                                                '{new_degree}', '{new_grounds}', 
                                                '{new_desc}', {new_price}, 
                                                {new_volume})""")
            self.max_id += 1

        self.table.create_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AskWidget('', '', '')
    ex.show()
    sys.exit(app.exec())
