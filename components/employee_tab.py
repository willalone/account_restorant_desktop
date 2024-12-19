from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, 
               QPushButton, QVBoxLayout, QHBoxLayout,
               QTableWidget, QTableWidgetItem, QDialog, QGridLayout, QMessageBox)
import random
import string

class EmployeesTab(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.layout = QVBoxLayout(self)

        # Добавляем выпадающий список для выбора роли
        self.role_label = QLabel("Роль:", self)
        self.role_input = QComboBox(self)
        self.role_input.addItems(["admin", "user"])

        self.first_name_label = QLabel("Имя:", self)
        self.first_name_input = QLineEdit(self)
        self.last_name_label = QLabel("Фамилия:", self)
        self.last_name_input = QLineEdit(self)
        self.position_label = QLabel("Должность:", self)
        self.position_input = QLineEdit(self)
        self.salary_label = QLabel("Зарплата:", self)
        self.salary_input = QLineEdit(self)
        self.add_employee_button = QPushButton("Добавить сотрудника", self)
        self.add_employee_button.clicked.connect(self.add_employee)

        # Таблица сотрудников
        self.employees_table = QTableWidget(self)
        self.employees_table.setColumnCount(8)
        self.employees_table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия", "Должность", "Зарплата", "Логин", "Пароль", "Роль"])
        self.update_employees_table()

        # Кнопки для управления сотрудниками
        self.edit_employee_button = QPushButton("Редактировать сотрудника", self)
        self.edit_employee_button.clicked.connect(self.show_edit_employee_dialog)
        self.delete_employee_button = QPushButton("Удалить сотрудника", self)
        self.delete_employee_button.clicked.connect(self.delete_employee)

        # Создаем макеты
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.first_name_label)
        input_layout.addWidget(self.first_name_input)
        input_layout.addWidget(self.last_name_label)
        input_layout.addWidget(self.last_name_input)
        input_layout.addWidget(self.position_label)
        input_layout.addWidget(self.position_input)
        input_layout.addWidget(self.salary_label)
        input_layout.addWidget(self.salary_input)
        input_layout.addWidget(self.role_label)
        input_layout.addWidget(self.role_input)
        input_layout.addWidget(self.add_employee_button)
        self.layout.addLayout(input_layout)

        self.layout.addWidget(self.employees_table)
        self.layout.addWidget(self.edit_employee_button)
        self.layout.addWidget(self.delete_employee_button)
        self.setLayout(self.layout)

    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    def generate_login(self, first_name, last_name):
        # Генерация случайного логина из английских букв и цифр
        all_characters = string.ascii_letters + string.digits  # Все английские буквы и цифры
        login_length = 8  # Минимальная длина логина

        # Генерируем случайный логин длиной не менее 8 символов
        login = ''.join(random.choice(all_characters) for _ in range(login_length))
        
        return login
    
    def add_employee(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        position = self.position_input.text()
        salary = self.salary_input.text()
        role = self.role_input.currentText().lower()

        # Генерация логина и пароля
        login = self.generate_login(first_name, last_name)
        password = self.generate_password()

        # Изменяем вызов метода db_manager
        self.db_manager.add_employee(first_name, last_name, position, salary, login, password, role)
        self.update_employees_table()

        # Очищаем поля
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.position_input.clear()
        self.salary_input.clear()
        self.role_input.setCurrentIndex(0)

    def update_employees_table(self):
        self.employees_table.setRowCount(0)
        employees = self.db_manager.get_employees()
        for row_number, employee in enumerate(employees):
            self.employees_table.insertRow(row_number)
            for col_number, value in enumerate(employee):
                self.employees_table.setItem(row_number, col_number, QTableWidgetItem(str(value) if value is not None else ""))

    def show_edit_employee_dialog(self):
        selected_row = self.employees_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для редактирования.")
            return

        # Получаем ID сотрудника из выбранной строки таблицы
        employee_id = int(self.employees_table.item(selected_row, 0).text())

        # Создаем диалоговое окно и вызываем exec_()
        dialog = EditEmployeeDialog(self.db_manager, employee_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.update_employees_table()

    def delete_employee(self):
        selected_row = self.employees_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления.")
            return

        employee_id = int(self.employees_table.item(selected_row, 0).text())
        self.db_manager.delete_employee(employee_id)

        self.update_employees_table()

# Создаем класс для диалогового окна редактирования сотрудника
class EditEmployeeDialog(QDialog):
    def __init__(self, db_manager, employee_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Редактировать сотрудника")
        self.layout = QGridLayout(self)

        self.employee_id = employee_id
        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.position_input = QLineEdit(self)
        self.salary_input = QLineEdit(self)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_changes)

        db_employee_data = self.db_manager.get_employee_by_id(employee_id)
        if db_employee_data:
            self.first_name_input.setText(db_employee_data[1])
            self.last_name_input.setText(db_employee_data[2])
            self.position_input.setText(db_employee_data[3])
            self.salary_input.setText(str(db_employee_data[4]))

        # Создаем макеты
        self.layout.addWidget(QLabel("Имя:", self), 0, 0)
        self.layout.addWidget(self.first_name_input, 0, 1)
        self.layout.addWidget(QLabel("Фамилия:", self), 1, 0)
        self.layout.addWidget(self.last_name_input, 1, 1)
        self.layout.addWidget(QLabel("Должность:", self), 2, 0)
        self.layout.addWidget(self.position_input, 2, 1)
        self.layout.addWidget(QLabel("Зарплата:", self), 3, 0)
        self.layout.addWidget(self.salary_input, 3, 1)
        self.layout.addWidget(self.save_button, 4, 1)

        self.setLayout(self.layout)

    def save_changes(self):
        try:
            first_name = self.first_name_input.text()
            last_name = self.last_name_input.text()
            position = self.position_input.text()
            salary = self.salary_input.text()

            # Проверка валидности данных
            if not all([first_name, last_name, position, salary]):
                raise ValueError("Все поля должны быть заполнены.")

            self.db_manager.update_employee(self.employee_id, first_name, last_name, position, salary)
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить изменения: {e}")
