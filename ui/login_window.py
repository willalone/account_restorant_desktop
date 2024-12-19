from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget

class LoginWindow(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent = parent

        self.setWindowTitle("Вход в систему")
        self.setFixedSize(500, 300)

        # Центрируем окно
        screen_geometry = QDesktopWidget().availableGeometry()  # Получаем доступную область экрана
        window_geometry = self.frameGeometry()  # Получаем геометрию текущего окна
        center_point = screen_geometry.center()  # Находим центр экрана
        window_geometry.moveCenter(center_point)  # Перемещаем окно в центр
        self.move(window_geometry.topLeft())

        # Элементы интерфейса
        self.label_username = QLabel("Имя пользователя:")
        self.input_username = QLineEdit()
        self.label_password = QLabel("Пароль:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("Войти")
        self.button_login.clicked.connect(self.check_credentials)

        # Расположение элементов
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #f4f4f9;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                border-radius: 10px;
                padding: 20px;
            }

            QLabel {
                font-size: 14px;
                color: #333333;
                margin-bottom: 5px;
            }

            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                margin-bottom: 15px;
            }

            QLineEdit:focus {
                border-color: #007bff;
            }

            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #0056b3;
            }

            QPushButton:pressed {
                background-color: #004085;
            }

            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

    def check_credentials(self):
        username = self.input_username.text()
        password = self.input_password.text()

        user_data = self.db_manager.get_user_by_login(username, password)
        print(f"Ищем пользователя: {username}, данные: {user_data}")  # Отладочное сообщение
        
        if user_data and user_data.get('password') == password:
            role = user_data.get('role')
            print(f"Авторизация успешна. Роль: {role}")
            self.parent.show_main_window(role)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль")
            print("Неверные данные для входа")
