from http.client import FORBIDDEN
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
               QVBoxLayout, QHBoxLayout, QGridLayout,
               QTableWidget, QTableWidgetItem, QComboBox, QDialog, QMessageBox)
from PyQt5.QtCore import Qt
import mysql

class MenuTab(QWidget):
  def __init__(self, db_manager, menu_item_id=None, parent=None):
    super().__init__(parent)
    self.db_manager = db_manager
    self.setWindowTitle("Редактировать блюдо")
    self.layout = QVBoxLayout(self)

    # Создаем виджеты
    self.menu_item_name_label = QLabel("Название блюда:", self)
    self.menu_item_name_input = QLineEdit(self)
    self.category_label = QLabel("Категория:", self)
    self.category_combobox = QComboBox(self)
    self.category_combobox.addItems(["Cморреброды", "Закуски", "Супы", "Овощи", "Гстрономический сет", "Согревающие", "Сливочный чай", "Лимонады", "Холодный чай", "Фреши", "Россия игристые вина", "Росиия белые вина", "Россия красные вина", "Другие страны вина", "Другие страны шампанского"]) # Добавьте категории
    self.price_label = QLabel("Цена:", self)
    self.price_input = QLineEdit(self)
    self.add_menu_item_button = QPushButton("Добавить блюдо", self)
    self.add_menu_item_button.clicked.connect(self.add_menu_item)

    # Таблица меню
    self.menu_table = QTableWidget(self)
    self.menu_table.setColumnCount(3)
    self.menu_table.setHorizontalHeaderLabels(["Название", "Категория", "Цена"])
    self.update_menu_table()

    # Кнопки для управления меню
    self.edit_menu_item_button = QPushButton("Редактировать блюдо", self)
    self.edit_menu_item_button.clicked.connect(self.show_edit_menu_item_dialog)
    self.delete_menu_item_button = QPushButton("Удалить блюдо", self)
    self.delete_menu_item_button.clicked.connect(self.delete_menu_item)

    # Создаем макеты
    input_layout = QHBoxLayout()
    input_layout.addWidget(self.menu_item_name_label)
    input_layout.addWidget(self.menu_item_name_input)
    input_layout.addWidget(self.category_label)
    input_layout.addWidget(self.category_combobox)
    input_layout.addWidget(self.price_label)
    input_layout.addWidget(self.price_input)
    input_layout.addWidget(self.add_menu_item_button)
    self.layout.addLayout(input_layout)

    self.layout.addWidget(self.menu_table)
    self.layout.addWidget(self.edit_menu_item_button)
    self.layout.addWidget(self.delete_menu_item_button)

    self.setLayout(self.layout)

  def add_menu_item(self):
    menu_item_name = self.menu_item_name_input.text()
    category = self.category_combobox.currentText()
    price = self.price_input.text()
    self.db_manager.add_menu_item(menu_item_name, category, price)
    self.update_menu_table()
    self.menu_item_name_input.clear()
    self.category_combobox.setCurrentIndex(0)
    self.price_input.clear()

  def update_menu_table(self):
    self.menu_table.setRowCount(0)
    menu_items = self.db_manager.get_menu_items()
    for row_number, menu_item in enumerate(menu_items):
      self.menu_table.insertRow(row_number)
      self.menu_table.setItem(row_number, 0, QTableWidgetItem(menu_item[1]))
      self.menu_table.setItem(row_number, 1, QTableWidgetItem(menu_item[2]))
      self.menu_table.setItem(row_number, 2, QTableWidgetItem(str(menu_item[3])))
  
  def delete_menu_item(self):
    selected_row = self.menu_table.currentRow()
    if selected_row >= 0:
      menu_item_id = int(self.menu_table.item(selected_row, 0).text())
      self.db_manager.delete_menu_item(menu_item_id)
      self.update_menu_table()

  def show_edit_menu_item_dialog(self):
    selected_row = self.menu_table.currentRow()
    if selected_row >= 0:
      # Получите menu_item_id из нужного столбца (например, 0)
      menu_item_id = self.menu_table.item(selected_row, 0).text() # Предполагаем, что menu_item_id хранится в первом столбце
      edit_dialog = EditMenuItemDialog(self.db_manager, menu_item_id)
      if edit_dialog.exec_():
        self.update_menu_table()
  

  def delete_menu_item(self):
    selected_row = self.menu_table.currentRow()
    if selected_row == -1:
      QMessageBox.warning(self, "Ошибка", "Выберите пункт меню для удаления.")
      return
    menu_item_id = self.menu_table.item(selected_row, 0).text()
    self.db_manager.delete_menu_item(menu_item_id)
    self.update_menu_table()

# Создаем класс для диалогового окна редактирования блюда
class EditMenuItemDialog(QDialog):
  def __init__(self, db_manager, menu_item_id=None, parent=None):
    super().__init__(parent)
    self.db_manager = db_manager
    self.menu_item_id = menu_item_id
    self.setWindowTitle("Редактировать блюдо")
    self.layout = QGridLayout(self)

    self.menu_item_name_input = QLineEdit(self)
    self.category_combobox = QComboBox(self)
    self.category_combobox.addItems(["Cморреброды", "Закуски", "Супы", "Овощи", "Гстрономический сет", "Согревающие", "Сливочный чай", "Лимонады", "Холодный чай", "Фреши", "Россия игристые вина", "Росиия белые вина", "Россия красные вина", "Другие страны вина", "Другие страны шампанского"])
    self.price_input = QLineEdit(self)
    self.save_button = QPushButton("Сохранить", self)
    self.save_button.clicked.connect(self.save_changes)

    if menu_item_id is not None:
      menu_item_data = self.db_manager.get_menu_item_by_id(menu_item_id)
      if menu_item_data:
        self.menu_item_name_input.setText(menu_item_data[1])
        self.category_combobox.setCurrentText(menu_item_data[2])
        self.price_input.setText(str(menu_item_data[3]))

    # Создаем макеты
    self.layout.addWidget(QLabel("Название блюда:", self), 0, 0)
    self.layout.addWidget(self.menu_item_name_input, 0, 1)
    self.layout.addWidget(QLabel("Категория:", self), 1, 0)
    self.layout.addWidget(self.category_combobox, 1, 1)
    self.layout.addWidget(QLabel("Цена:", self), 2, 0)
    self.layout.addWidget(self.price_input, 2, 1)
    self.layout.addWidget(self.save_button, 3, 1)

    self.setLayout(self.layout)
  
  """def open_edit_menu_item_dialog(self, menu_item_id):
     edit_dialog = EditMenuItemDialog(db_manager=self.db_manager, menu_item_id=menu_item_id) 
     edit_dialog.exec_()

  def save_changes(self):
    menu_item_name = self.menu_item_name_input.text()
    category = self.category_combobox.currentText()
    price = self.price_input.text()
    self.db_manager.update_menu_item(self.menu_item_id, menu_item_name, category, price) 
    self.close()

  def get_menu_item_by_id(self, menu_item_id):
    sql = "SELECT * FROM Menu WHERE menu_item_id = %s"
    self.cursor.execute(sql, (menu_item_id,))
    return self.cursor.fetchone()"""

  def save_changes(self):
    menu_item_name = self.menu_item_name_input.text()
    category = self.category_combobox.currentText()
    price = self.price_input.text()
    self.db_manager.update_menu_item(self.menu_item_id, menu_item_name, category, price)
    
    # Получаем соединение
    conn = self.db_manager.conn  
    
    def mit(connection):
        print("MIT License")
        print(f"Соединение: {connection} - Запрещено") 
    
    # Передаем соединение в функцию mit
    mit(conn)  # Вызываем функцию с аргументом
    conn.close()
    
    try:
        # Сохраняем изменения
        conn = mysql.connector.connect(
            host="localhost",
            user="new_user",
            password="secure_password",
            database="restaurant",
            charset="utf8mb4",
            collation="utf8mb4_unicode_ci" 
            )
        cursor = conn.cursor()
        # Выполняем SQL-запрос для обновления данных
        cursor.execute(
            "UPDATE Menu SET name = %s, category = %s, price = %s WHERE menu_item_id = %s", 
            (menu_item_name, category, price, self.menu_item_id)
        )
        
        # Вызываем функцию mit с текущим соединением
        mit(conn)  # Вызываем функцию с аргументом
        
        cursor.close()  # Закрываем курсор
    except mysql.connector.Error as error:
        print("Ошибка при сохранении изменений:", error)
    finally:
        if conn.is_connected():
            conn.close()  # Закрываем соединение
    
    self.close()
        
  def open_edit_menu_item_dialog(self, menu_item_id):
        edit_dialog = EditMenuItemDialog(db_manager=self.db_manager, menu_item_id=menu_item_id)
        edit_dialog.exec_()

  def get_menu_item_by_id(self, menu_item_id):
        sql = "SELECT * FROM Menu WHERE menu_item_id = %s"
        self.db_manager.cursor.execute(sql, (menu_item_id,))
        return self.db_manager.cursor.fetchone()
