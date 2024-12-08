from http.client import FORBIDDEN
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
               QVBoxLayout, QHBoxLayout, QGridLayout,
               QTableWidget, QTableWidgetItem, QComboBox, QDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
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
        self.category_combobox.addItems([
            "Сморреброды", "Закуски", "Супы", "Овощи", "Гастрономический сет",
            "Согревающие", "Сливочный чай", "Лимонады", "Холодный чай", "Фреши",
            "Россия игристые вина", "Россия белые вина", "Россия красные вина",
            "Другие страны вина", "Другие страны шампанского"
        ])
        self.price_label = QLabel("Цена:", self)
        self.price_input = QLineEdit(self)
        self.add_menu_item_button = QPushButton("Добавить блюдо", self)
        self.add_menu_item_button.clicked.connect(self.add_menu_item)

        # Таблица меню
        self.menu_table = QTableWidget(self)
        self.menu_table.setColumnCount(4)
        self.menu_table.setHorizontalHeaderLabels(["id", "Название", "Категория", "Цена"])
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

    def get_selected_menu_item_id(self):
        selected_row = self.menu_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите пункт меню.")
            return None
        menu_item_id_item = self.menu_table.item(selected_row, 0)  # ID блюда
        return int(menu_item_id_item.text()) if menu_item_id_item else None

    def add_menu_item(self):
        menu_item_name = self.menu_item_name_input.text()
        category = self.category_combobox.currentText()
        price = self.price_input.text()
        try:
            self.db_manager.add_menu_item(menu_item_name, category, price)
            self.update_menu_table()
            QMessageBox.information(self, "Успех", "Блюдо успешно добавлено.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить блюдо: {e}")
        finally:
            self.menu_item_name_input.clear()
            self.category_combobox.setCurrentIndex(0)
            self.price_input.clear()

    def update_menu_table(self):
        try:
            self.menu_table.setRowCount(0)
            menu_items = self.db_manager.get_menu_items()
            for row_number, menu_item in enumerate(menu_items):
                self.menu_table.insertRow(row_number)
                self.menu_table.setItem(row_number, 0, QTableWidgetItem(str(menu_item[0])))
                self.menu_table.setItem(row_number, 1, QTableWidgetItem(menu_item[1]))
                self.menu_table.setItem(row_number, 2, QTableWidgetItem(menu_item[2]))
                self.menu_table.setItem(row_number, 3, QTableWidgetItem(str(menu_item[3])))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить таблицу: {e}")

    def delete_menu_item(self):
      menu_item_id = self.get_selected_menu_item_id()
      if menu_item_id is None:
          return  # Ничего не выбрано, отменяем операцию
      try:
          self.db_manager.delete_menu_item(menu_item_id)
          self.update_menu_table()
          QMessageBox.information(self, "Успех", "Блюдо успешно удалено.")
      except Exception as e:
          QMessageBox.critical(self, "Ошибка", f"Не удалось удалить блюдо: {e}")

    def show_edit_menu_item_dialog(self):
      menu_item_id = self.get_selected_menu_item_id()
      if menu_item_id is None:
          return  # Ничего не выбрано, отменяем операцию

      # Извлекаем данные из выбранной строки
      selected_row = self.menu_table.currentRow()
      menu_item_name = self.menu_table.item(selected_row, 1).text()
      category = self.menu_table.item(selected_row, 2).text()
      price = self.menu_table.item(selected_row, 3).text()

      # Передаем данные в диалог
      dialog = EditMenuItemDialog(self.db_manager, menu_item_id=menu_item_id, parent=self)

      dialog.menu_item_name_input.setText(menu_item_name)
      dialog.category_combobox.setCurrentText(category)
      dialog.price_input.setText(price)

      dialog.menu_item_updated.connect(self.update_menu_table)

      if dialog.exec_() == QDialog.Accepted:
          self.update_menu_table()

# Создаем класс для диалогового окна редактирования блюда
class EditMenuItemDialog(QDialog):
    menu_item_updated = pyqtSignal()  # Сигнал для уведомления об обновлении

    def __init__(self, db_manager, menu_item_id=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.menu_item_id = menu_item_id
        self.setWindowTitle("Редактировать блюдо")
        self.layout = QGridLayout(self)

        self.menu_item_name_input = QLineEdit(self)
        self.category_combobox = QComboBox(self)
        self.category_combobox.addItems([
            "Cморреброды", "Закуски", "Супы", "Овощи", 
            "Гстрономический сет", "Согревающие", "Сливочный чай", 
            "Лимонады", "Холодный чай", "Фреши", 
            "Россия игристые вина", "Росиия белые вина", 
            "Россия красные вина", "Другие страны вина", "Другие страны шампанского"
        ])
        self.price_input = QLineEdit(self)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_changes)

        if menu_item_id is not None:
            try:
                menu_item_data = self.db_manager.get_menu_item_by_id(menu_item_id)
                if menu_item_data:
                    self.menu_item_name_input.setText(menu_item_data[1])
                    self.category_combobox.setCurrentText(menu_item_data[2])
                    self.price_input.setText(str(menu_item_data[3]))
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")

        self.layout.addWidget(QLabel("Название блюда:", self), 0, 0)
        self.layout.addWidget(self.menu_item_name_input, 0, 1)
        self.layout.addWidget(QLabel("Категория:", self), 1, 0)
        self.layout.addWidget(self.category_combobox, 1, 1)
        self.layout.addWidget(QLabel("Цена:", self), 2, 0)
        self.layout.addWidget(self.price_input, 2, 1)
        self.layout.addWidget(self.save_button, 3, 1)

        self.setLayout(self.layout)

    def save_changes(self):
      menu_item_name = self.menu_item_name_input.text().strip()
      category = self.category_combobox.currentText().strip()
      price = self.price_input.text().strip()

      if not menu_item_name or not price:
          QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
          return

      try:
          price = float(price)
          self.db_manager.update_menu_item(self.menu_item_id, menu_item_name, category, price)
          QMessageBox.information(self, "Успех", "Изменения сохранены.")
          self.menu_item_updated.emit()  # Испускаем сигнал
          self.close()  # Закрываем диалог
      except ValueError:
          QMessageBox.warning(self, "Ошибка", "Цена должна быть числом.")
      except Exception as e:
          QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {e}")

