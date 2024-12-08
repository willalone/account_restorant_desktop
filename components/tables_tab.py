from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QMessageBox)
from PyQt5.QtCore import Qt

class TablesTab(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.layout = QVBoxLayout(self)

        # Создаем виджеты
        self.table_number_label = QLabel("Номер стола:", self)
        self.table_number_input = QLineEdit(self)
        self.capacity_label = QLabel("Вместимость:", self)
        self.capacity_input = QLineEdit(self)
        self.add_table_button = QPushButton("Добавить стол", self)
        self.add_table_button.clicked.connect(self.add_table)

        # Таблица столов
        self.tables_table = QTableWidget(self)
        self.tables_table.setColumnCount(2)
        self.tables_table.setHorizontalHeaderLabels(["Номер стола", "Вместимость"])
        self.update_tables_table()

        # Кнопки для управления столами
        self.edit_table_button = QPushButton("Редактировать стол", self)
        self.edit_table_button.clicked.connect(self.show_edit_table_dialog)
        self.delete_table_button = QPushButton("Удалить стол", self)
        self.delete_table_button.clicked.connect(self.delete_table)

        # Создаем макеты
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.table_number_label)
        input_layout.addWidget(self.table_number_input)
        input_layout.addWidget(self.capacity_label)
        input_layout.addWidget(self.capacity_input)
        input_layout.addWidget(self.add_table_button)
        self.layout.addLayout(input_layout)

        self.layout.addWidget(self.tables_table)
        self.layout.addWidget(self.edit_table_button)
        self.layout.addWidget(self.delete_table_button)

        self.setLayout(self.layout)

    def add_table(self):
        table_number = self.table_number_input.text().strip()
        capacity = self.capacity_input.text().strip()

        if not table_number or not capacity:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            self.db_manager.add_table(table_number, capacity)
            self.update_tables_table()
            self.table_number_input.clear()
            self.capacity_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить стол: {e}")

    def update_tables_table(self):
        self.tables_table.setRowCount(0)
        try:
            tables = self.db_manager.get_tables()
            for row_number, table in enumerate(tables):
                self.tables_table.insertRow(row_number)

                # Сохраняем ID как свойство первого элемента строки
                table_number_item = QTableWidgetItem(str(table[2] or ""))
                table_number_item.setData(Qt.UserRole, table[0])  # Сохраняем ID
                self.tables_table.setItem(row_number, 0, table_number_item)  # Номер стола
                self.tables_table.setItem(row_number, 1, QTableWidgetItem(str(table[1])))  # Вместимость
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить таблицы: {e}")

    def show_edit_table_dialog(self):
        selected_row = self.tables_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите стол для редактирования.")
            return

        # Извлекаем данные о выбранном столе
        table_number_item = self.tables_table.item(selected_row, 0)
        table_id = table_number_item.data(Qt.UserRole)  # ID стола
        table_number = table_number_item.text()  # Номер стола
        capacity_item = self.tables_table.item(selected_row, 1)
        capacity = capacity_item.text() if capacity_item else ""

        # Передаем данные в диалог
        table_data = (table_id, capacity, table_number)
        dialog = EditTableDialog(self.db_manager, table_data, self)
        if dialog.exec_() == QDialog.Accepted:
            self.update_tables_table()

    def delete_table(self):
        selected_row = self.tables_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите стол для удаления.")
            return

        table_number_item = self.tables_table.item(selected_row, 0)
        table_id = table_number_item.data(Qt.UserRole)  # Извлекаем ID
        try:
            self.db_manager.delete_table(table_id)
            self.update_tables_table()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить стол: {e}")

class EditTableDialog(QDialog):
    def __init__(self, db_manager, table_data=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Редактировать стол")
        self.layout = QVBoxLayout(self)

        self.capacity_input = QLineEdit(self)
        self.table_number_input = QLineEdit(self)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_changes)

        if table_data:
            self.table_id = table_data[0]
            self.capacity_input.setText(str(table_data[1]))
            self.table_number_input.setText(str(table_data[2] or ""))
        else:
            self.table_id = None

        self.layout.addWidget(QLabel("Вместимость:"))
        self.layout.addWidget(self.capacity_input)
        self.layout.addWidget(QLabel("Номер стола:"))
        self.layout.addWidget(self.table_number_input)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def save_changes(self):
        capacity = self.capacity_input.text().strip()
        table_number = self.table_number_input.text().strip()

        if not capacity:
            QMessageBox.warning(self, "Ошибка", "Поле вместимости должно быть заполнено.")
            return

        try:
            self.db_manager.update_table(self.table_id, capacity, table_number)
            QMessageBox.information(self, "Успех", "Изменения сохранены.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {e}")
