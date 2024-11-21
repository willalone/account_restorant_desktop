from tkinter import messagebox
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
               QVBoxLayout, QHBoxLayout, QGridLayout,
               QTableWidget, QTableWidgetItem, QComboBox, QDialog)
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

        # Таблица столов (обновили количество столбцов на 2)
        self.tables_table = QTableWidget(self)
        self.tables_table.setColumnCount(2)  # Убираем третий столбец
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
        table_number = self.table_number_input.text()
        capacity = self.capacity_input.text()
        self.db_manager.add_table(table_number, capacity)
        self.update_tables_table()
        self.table_number_input.clear()
        self.capacity_input.clear()

    def update_tables_table(self):
        self.tables_table.setRowCount(0)
        tables = self.db_manager.get_tables()
        for row_number, table in enumerate(tables):
            self.tables_table.insertRow(row_number)
            self.tables_table.setItem(row_number, 0, QTableWidgetItem(str(table[0])))  # Номер стола
            self.tables_table.setItem(row_number, 1, QTableWidgetItem(str(table[1])))  # Вместимость

    def show_edit_table_dialog(self):
        selected_row = self.tables_table.currentRow()
        if selected_row == -1:
            messagebox.warning(self, "Ошибка", "Выберите стол для редактирования.")
            return
        table_id = self.tables_table.item(selected_row, 0).text()
        edit_dialog = EditTableDialog(self.db_manager, table_id)
        edit_dialog.exec_()
        self.update_tables_table()

    def delete_table(self):
        selected_row = self.tables_table.currentRow()
        if selected_row == -1:
            messagebox.warning(self, "Ошибка", "Выберите стол для удаления.")
            return
        table_id = self.tables_table.item(selected_row, 0).text()
        self.db_manager.delete_table(table_id)
        self.update_tables_table()

# Создаем класс для диалогового окна редактирования стола
class EditTableDialog(QDialog):
    def __init__(self, db_manager, table_data=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Редактировать стол")
        self.layout = QGridLayout(self)

        self.table_number_input = QLineEdit(self)
        self.capacity_input = QLineEdit(self)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_changes)

        # Если переданы данные стола, заполняем поля
        if table_data:
            self.table_number_input.setText(str(table_data[0]))
            self.capacity_input.setText(str(table_data[1]))

        # Создаем макеты
        self.layout.addWidget(QLabel("Номер стола:", self), 0, 0)
        self.layout.addWidget(self.table_number_input, 0, 1)
        self.layout.addWidget(QLabel("Вместимость:", self), 1, 0)
        self.layout.addWidget(self.capacity_input, 1, 1)
        self.layout.addWidget(self.save_button, 2, 1)

        self.setLayout(self.layout)

    def save_changes(self):
        table_number = self.table_number_input.text()
        capacity = self.capacity_input.text()
        # Логика сохранения изменений
        self.close()
