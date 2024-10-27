from tkinter import messagebox
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
               QPushButton, QVBoxLayout, QHBoxLayout,
               QTableWidget, QTableWidgetItem, QComboBox, QGridLayout, QDialog)
from PyQt5.QtCore import Qt

class InventoryTab(QWidget):
  def __init__(self, db_manager, parent=None):
    super().__init__(parent)
    self.db_manager = db_manager
    self.layout = QVBoxLayout(self)

    # Создаем виджеты
    self.product_name_label = QLabel("Название продукта:", self)
    self.product_name_input = QLineEdit(self)
    self.quantity_label = QLabel("Количество:", self)
    self.quantity_input = QLineEdit(self)
    self.unit_label = QLabel("Единица измерения:", self)
    self.unit_combobox = QComboBox(self)
    self.unit_combobox.addItems(["шт.", "кг", "л", "г", "мл"]) 
    self.add_product_button = QPushButton("Добавить продукт", self)
    self.add_product_button.clicked.connect(self.add_product)

    # Таблица продуктов
    self.inventory_table = QTableWidget(self)
    self.inventory_table.setColumnCount(4)
    self.inventory_table.setHorizontalHeaderLabels(["Название", "Количество", "Единица", "Действия"])
    self.update_inventory_table()

    # Кнопки для управления продуктами
    self.edit_product_button = QPushButton("Редактировать продукт", self)
    self.edit_product_button.clicked.connect(self.show_edit_product_dialog)
    self.delete_product_button = QPushButton("Удалить продукт", self)
    self.delete_product_button.clicked.connect(self.delete_product)

    # Создаем макеты
    input_layout = QHBoxLayout()
    input_layout.addWidget(self.product_name_label)
    input_layout.addWidget(self.product_name_input)
    input_layout.addWidget(self.quantity_label)
    input_layout.addWidget(self.quantity_input)
    input_layout.addWidget(self.unit_label)
    input_layout.addWidget(self.unit_combobox)
    input_layout.addWidget(self.add_product_button)
    self.layout.addLayout(input_layout)

    self.layout.addWidget(self.inventory_table)
    self.layout.addWidget(self.edit_product_button)
    self.layout.addWidget(self.delete_product_button)

    self.setLayout(self.layout)

  def add_product(self):
    product_name = self.product_name_input.text()
    quantity = self.quantity_input.text()
    unit = self.unit_combobox.currentText()
    self.db_manager.add_product(product_name, quantity, unit)
    self.update_inventory_table()
    self.product_name_input.clear()
    self.quantity_input.clear()
    self.unit_combobox.setCurrentIndex(0)

  def update_inventory_table(self):
    self.inventory_table.setRowCount(0)
    products = self.db_manager.get_products()
    for row_number, product in enumerate(products):
      self.inventory_stable.insertRow(row_number)
      self.inventory_table.setItem(row_number, 0, QTableWidgetItem(product[0]))
      self.inventory_table.setItem(row_number, 1, QTableWidgetItem(str(product[1])))
      self.inventory_table.setItem(row_number, 2, QTableWidgetItem(product[2]))

  def show_edit_product_dialog(self):
    selected_row = self.inventory_table.currentRow()
    if selected_row == -1:
      messagebox.warning(self, "Ошибка", "Выберите продукт для редактирования.")
      return
    ingredient_id = self.inventory_table.item(selected_row, 0).text()
    quantity = self.inventory_table.item(selected_row, 1).text()
    unit = self.inventory_table.item(selected_row, 2).text()
    dialog = EditProductDialog(self.db_manager, ingredient_id, quantity, unit)
    dialog.exec_()
    self.update_inventory_table()

  def delete_product(self):
    elected_row = self.inventory_table.currentRow()
    if elected_row == -1:
      messagebox.warning(self, "Ошибка", "Выберите продукт для удаления.")
      return
    ingredient_id = self.inventory_table.item(elected_row, 0).text()
    self.db_manager.delete_product(ingredient_id)

    self.update_inventory_table()

# Создаем класс для диалогового окна редактирования продукта
class EditProductDialog(QDialog):
  def __init__(self, db_manager, product_data=None, parent=None):
    super().__init__(parent)
    self.db_manager = db_manager
    self.setWindowTitle("Редактировать продукт")
    self.layout = QGridLayout(self)

    self.product_name_input = QLineEdit(self)
    self.quantity_input = QLineEdit(self)
    self.unit_combobox = QComboBox(self)
    self.unit_combobox.addItems(["шт.", "кг", "л", "г", "мл"]) 
    self.save_button = QPushButton("Сохранить", self)
    self.save_button.clicked.connect(self.save_changes)

    # Если переданы данные продукта, заполняем поля 
    if product_data:
      self.product_name_input.setText(product_data[0])
      self.quantity_input.setText(str(product_data[1]))
      self.unit_combobox.setCurrentText(product_data[2])

    # Создаем макеты
    self.layout.addWidget(QLabel("Название:", self), 0, 0)
    self.layout.addWidget(self.product_name_input, 0, 1)
    self.layout.addWidget(QLabel("Количество:", self), 1, 0)
    self.layout.addWidget(self.quantity_input, 1, 1)
    self.layout.addWidget(QLabel("Единица:", self), 2, 0)
    self.layout.addWidget(self.unit_combobox, 2, 1)
    self.layout.addWidget(self.save_button, 3, 1)

    self.setLayout(self.layout)

  def save_changes(self):
    product_name = self.product_name_input.text()
    quantity = self.quantity_input.text()
    unit = self.unit_combobox.currentText()
    # ... (Логика получения product_id)
    # ... (db_manager.update_product(product_id, product_name, quantity, unit))
    self.close()
