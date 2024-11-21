from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QDialogButtonBox, QInputDialog
from PyQt5.QtCore import Qt

class DishSelectionDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.selected_dishes = []

        self.dish_list_widget = QListWidget()
        self.dish_list_widget.addItems(self.get_dishes())

        self.select_button = QPushButton("Выбрать")
        self.select_button.clicked.connect(self.select_dishes)

        # Удаляем лишний вызов setLayout
        self.init_ui()
        

    def get_selected_dishes(self):
        """Возвращает выбранные блюда."""
        return self.selected_dishes

    def init_ui(self):
        self.setWindowTitle("Выбор блюд для заказа")
        self.setGeometry(100, 100, 400, 300)  # Размеры окна

        # Основной вертикальный layout
        main_layout = QVBoxLayout()

        # Метка для объяснения
        label = QLabel("Выберите блюда для заказа:")
        main_layout.addWidget(label)

        # Список блюд
        self.dish_list = QListWidget()
        self.load_dishes()  # Загружаем блюда из базы данных
        main_layout.addWidget(self.dish_list)

        # Кнопки для добавления и отмены
        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить в заказ")
        cancel_button = QPushButton("Отменить")

        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        # Соединяем кнопки с действиями
        add_button.clicked.connect(self.add_dishes_to_order)
        cancel_button.clicked.connect(self.reject)

        main_layout.addLayout(button_layout)

        # Устанавливаем layout в диалоговое окно
        self.setLayout(main_layout)
    
    def get_dishes(self):
        # Получение списка всех доступных блюд (для примера)
        query = "SELECT name FROM menu"
        self.db_manager.cursor.execute(query)
        dishes = self.db_manager.cursor.fetchall()
        return [dish[0] for dish in dishes]

    def select_dishes(self):
        selected_items = self.dish_list_widget.selectedItems()
        self.selected_dishes = []

        for item in selected_items:
            dish_name = item.text()
            # Получаем dish_id по названию блюда
            dish_id = self.db_manager.get_dish_id_by_name(dish_name)
            if dish_id is not None:
                self.selected_dishes.append((dish_id, 1))  # Добавляем идентификатор блюда и количество
            else:
                print(f"Ошибка: блюдо '{dish_name}' не найдено в базе данных!")

        print(f"Выбраны блюда: {self.selected_dishes}")
        self.accept()

    def get_selected_dishes(self):
        return self.selected_dishes

    def set_selected_dishes(self, dishes):
        # Устанавливаем выбранные блюда в список
        self.selected_dishes = dishes
        self.dish_list_widget.clearSelection()  # Снимаем выделение
        for dish, _ in dishes:
            for index in range(self.dish_list_widget.count()):
                if self.dish_list_widget.item(index).text() == dish:
                    self.dish_list_widget.item(index).setSelected(True)  # Выбираем блюда, переданные в set_selected_dishes

    def load_dishes(self):
        """Загружает блюда из базы данных и добавляет их в список."""
        # Пример запроса для получения всех блюд
        query = "SELECT name FROM Menu"
        dishes = self.db_manager.execute_query(query)

        # Добавляем блюда в QListWidget
        for dish in dishes:
            self.dish_list.addItem(dish[0])  # dish[0] — это имя блюда

    def add_dishes_to_order(self):
        selected_items = self.dish_list.selectedItems()

        if not selected_items:
            self.show_error("Не выбраны блюда для заказа.")
            return

        for item in selected_items:
            # Запрашиваем количество
            quantity, ok = QInputDialog.getInt(self, "Количество", f"Введите количество для {item.text()}:")
            if ok:
                # Получаем ID блюда по его названию
                dish_id = self.db_manager.get_dish_id_by_name(item.text())  # Возвращаем ID блюда
                if dish_id is not None:
                    self.selected_dishes.append((dish_id, quantity))
                else:
                    self.show_error(f"Не удалось найти блюдо: {item.text()}")

        print(f"Добавленные блюда: {self.selected_dishes}")
        self.accept()


    def show_error(self, message):
        """Отображает ошибку в диалоговом окне."""
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Ошибка")
        msg.exec_()
