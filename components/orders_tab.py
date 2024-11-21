import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
                             QMessageBox)
from PyQt5.QtCore import Qt
from components.dish_selection_dialog import DishSelectionDialog

class OrdersTab(QWidget):
    def __init__(self, db_manager, user_role, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_role = user_role
        self.selected_dishes = []  # Список выбранных блюд для текущего заказа

        # Таблица для отображения заказов
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(9)  # Увеличиваем количество столбцов на 1
        self.orders_table.setHorizontalHeaderLabels(
            ["ID", "Стол", "Сотрудник", "Время", "Статус", "Блюда", "Итоговая цена", "Добавить блюдо", "Удалить"]
        )
        self.orders_table.verticalHeader().setVisible(False)
        self.orders_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.orders_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Запрет на редактирование ячеек

        # Поля для добавления/редактирования заказов
        self.table_id_input = QLineEdit()
        self.table_id_input.setPlaceholderText("ID стола")
        self.employee_id_input = QLineEdit()
        self.employee_id_input.setPlaceholderText("ID сотрудника")
        self.status_input = QComboBox()
        self.status_input.addItems(["В обработке", "Готовится", "Завершен", "Отменен"])

        self.add_button = QPushButton("Добавить заказ")
        self.add_button.clicked.connect(self.add_order)

        self.select_dishes_button = QPushButton("Выбрать блюда")
        self.select_dishes_button.clicked.connect(self.open_dish_selection_dialog)

        # Макет
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Новый заказ:"))
        input_layout.addWidget(self.table_id_input)
        input_layout.addWidget(self.employee_id_input)
        input_layout.addWidget(self.status_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_dishes_button)
        button_layout.addWidget(self.add_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.orders_table)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Загрузка заказов
        self.load_orders()

    def load_orders(self):
        # Загрузка заказов из базы данных
        orders = self.db_manager.get_orders()  # Получаем список заказов
        self.orders_table.setRowCount(len(orders))

        for i, order in enumerate(orders):
            # Основная информация о заказе
            self.orders_table.setItem(i, 0, QTableWidgetItem(str(order[0])))  # order_id
            self.orders_table.setItem(i, 1, QTableWidgetItem(str(order[1])))  # table_id
            self.orders_table.setItem(i, 2, QTableWidgetItem(str(order[2])))  # employee_id
            self.orders_table.setItem(i, 3, QTableWidgetItem(order[3].strftime("%Y-%m-%d %H:%M:%S")))  # order_time
            self.orders_table.setItem(i, 4, QTableWidgetItem(order[4]))  # status

            # Получаем блюда, связанные с заказом
            order_id = order[0]
            query = "SELECT dish_id, quantity FROM order_dishes WHERE order_id = %s"
            self.db_manager.cursor.execute(query, (order_id,))
            dishes = self.db_manager.cursor.fetchall()

            # Формируем строку с блюдами для отображения и считаем итоговую цену
            dish_info = ""
            total_price = 0.0
            for dish in dishes:
                dish_id, quantity = dish
                # Получаем название блюда и его цену
                query = "SELECT name, price FROM menu WHERE menu_item_id = %s"
                self.db_manager.cursor.execute(query, (dish_id,))
                dish_name, price = self.db_manager.cursor.fetchone()
                dish_info += f"{dish_name} (x{quantity}), "
                total_price += float(price) * quantity  # Рассчитываем итоговую цену

            # Убираем последнюю запятую
            if dish_info:
                dish_info = dish_info.rstrip(", ")

            # Отображаем блюда в таблице
            self.orders_table.setItem(i, 5, QTableWidgetItem(dish_info))

            # Отображаем итоговую цену в таблице
            self.orders_table.setItem(i, 6, QTableWidgetItem(f"{total_price:.2f}"))  # Новый столбец

            # Добавляем кнопки для редактирования и удаления заказа
            edit_button = QPushButton("Редактировать")
            edit_button.clicked.connect(lambda _, row=i: self.edit_order(row))
            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(lambda _, row=i: self.delete_order(row))

            self.orders_table.setCellWidget(i, 7, edit_button)
            self.orders_table.setCellWidget(i, 8, delete_button)

    def open_dish_selection_dialog(self):
        dialog = DishSelectionDialog(self.db_manager, self)
        if dialog.exec_():
            self.selected_dishes = dialog.get_selected_dishes()
            print("Выбранные блюда:", self.selected_dishes)

    def add_order(self):
        # Добавление нового заказа
        table_id = self.table_id_input.text()
        employee_id = self.employee_id_input.text()
        status = self.status_input.currentText()

        if not table_id or not employee_id:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        if not self.selected_dishes:
            QMessageBox.warning(self, "Ошибка", "Блюда не выбраны.")
            return

        try:
            # Вставка заказа в таблицу orders
            query = "INSERT INTO orders (table_id, employee_id, status, order_time) VALUES (%s, %s, %s, NOW())"
            self.db_manager.cursor.execute(query, (table_id, employee_id, status))
            order_id = self.db_manager.cursor.lastrowid

            # Вставка выбранных блюд в таблицу order_dishes
            for dish_id, quantity in self.selected_dishes:
                query = "INSERT INTO order_dishes (order_id, dish_id, quantity) VALUES (%s, %s, %s)"
                self.db_manager.cursor.execute(query, (order_id, dish_id, quantity))

            self.db_manager.conn.commit()
            QMessageBox.information(self, "Успех", "Заказ добавлен.")
            self.load_orders()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить заказ: {e}")

    def edit_order(self, row):
        # Редактирование заказа
        order_id = self.orders_table.item(row, 0).text()
        table_id = self.orders_table.item(row, 1).text()
        employee_id = self.orders_table.item(row, 2).text()
        status = self.orders_table.item(row, 4).text()

        # Открытие диалогового окна для выбора/редактирования блюд
        self.table_id_input.setText(table_id)
        self.employee_id_input.setText(employee_id)
        self.status_input.setCurrentText(status)

        # Загружаем текущие блюда для редактирования
        self.selected_dishes = self.get_current_dishes(order_id)
        print(f"Текущие блюда для редактирования: {self.selected_dishes}")

        # Открыть диалоговое окно для выбора блюд
        dialog = DishSelectionDialog(self.db_manager, self)
        dialog.set_selected_dishes(self.selected_dishes)  # Передаем выбранные блюда
        if dialog.exec_():
            self.selected_dishes = dialog.get_selected_dishes()
            print("Обновленные выбранные блюда:", self.selected_dishes)

            # Изменить данные заказа и обновить блюда
            self.update_order(order_id, table_id, employee_id, status)

    def get_current_dishes(self, order_id):
        # Получаем текущие блюда, связанные с заказом
        query = "SELECT dish_id, quantity FROM order_dishes WHERE order_id = %s"
        self.db_manager.cursor.execute(query, (order_id,))
        dishes = self.db_manager.cursor.fetchall()
        return [(dish_id, quantity) for dish_id, quantity in dishes]

    def update_order(self, order_id, table_id, employee_id, status):
        # Обновляем информацию о заказе
        try:
            update_query = "UPDATE orders SET table_id=%s, employee_id=%s, status=%s WHERE order_id=%s"
            self.db_manager.cursor.execute(update_query, (table_id, employee_id, status, order_id))

            # Удаляем старые блюда из таблицы order_dishes
            delete_query = "DELETE FROM order_dishes WHERE order_id=%s"
            self.db_manager.cursor.execute(delete_query, (order_id,))

            # Вставляем обновленные блюда
            for dish_id, quantity in self.selected_dishes:
                insert_query = "INSERT INTO order_dishes (order_id, dish_id, quantity) VALUES (%s, %s, %s)"
                self.db_manager.cursor.execute(insert_query, (order_id, dish_id, quantity))

            self.db_manager.conn.commit()
            QMessageBox.information(self, "Успех", "Заказ обновлен.")
            self.load_orders()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить заказ: {e}")

    def delete_order(self, row):
        # Удаление заказа
        order_id = self.orders_table.item(row, 0).text()
        try:
            delete_query = "DELETE FROM orders WHERE order_id=%s"
            self.db_manager.cursor.execute(delete_query, (order_id,))
            self.db_manager.conn.commit()
            QMessageBox.information(self, "Успех", "Заказ удален.")
            self.load_orders()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить заказ: {e}")
