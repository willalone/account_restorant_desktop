from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class LoginWindow(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent = parent

        self.setWindowTitle("Вход в систему")
        self.setFixedSize(300, 150)

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
    
    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Проверка логина и пароля
        if username == "user" and password == "user1":
            self.user_role = "employee"  # Устанавливаем роль "читатель"
            QMessageBox.information(self, "Успех", "Вы вошли как пользователь с ограниченным доступом")
            self.close()
        elif username == "admin" and password == "admin123":
            self.user_role = "admin"  # Устанавливаем роль "редактор"
            QMessageBox.information(self, "Успех", "Вы вошли как администратор")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def check_credentials(self):
        username = self.input_username.text()
        password = self.input_password.text()

        try:
            if username == "admin" and password == "admin_228":
                self.parent.show_main_window("admin")  # Показываем главное окно для администратора
            elif username == "user" and password == "user1":
                self.parent.show_main_window("user")  # Показываем главное окно для обычного пользователя
            else:
                QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")
