from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
               QPushButton, QVBoxLayout, QHBoxLayout,
               QTableWidget, QTableWidgetItem, QDialog, QGridLayout)

class EmployeesTab(QWidget):
  def __init__(self, db_manager, parent=None):
    super().__init__(parent)
    self.db_manager = db_manager
    self.layout = QVBoxLayout(self)

    # Создаем виджеты для добавления сотрудника
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
    self.employees_table.setColumnCount(5)
    self.employees_table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия", "Должность", "Зарплата"])
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
    input_layout.addWidget(self.add_employee_button)
    self.layout.addLayout(input_layout)

    self.layout.addWidget(self.employees_table)
    self.layout.addWidget(self.edit_employee_button)
    self.layout.addWidget(self.delete_employee_button)
    self.setLayout(self.layout)

  def add_employee(self):
    first_name = self.first_name_input.text()
    last_name = self.last_name_input.text()
    position = self.position_input.text()
    salary = self.salary_input.text()
    self.db_manager.add_employee(first_name, last_name, position, salary)
    self.update_employees_table()
    self.first_name_input.clear()
    self.last_name_input.clear()
    self.position_input.clear()
    self.salary_input.clear()

  def update_employees_table(self):
    self.employees_table.setRowCount(0)
    employees = self.db_manager.get_employees()
    for row_number, employee in enumerate(employees):
      self.employees_table.insertRow(row_number)
      self.employees_table.setItem(row_number, 0, QTableWidgetItem(str(employee[0])))
      self.employees_table.setItem(row_number, 1, QTableWidgetItem(employee[1]))
      self.employees_table.setItem(row_number, 2, QTableWidgetItem(employee[2]))
      self.employees_table.setItem(row_number, 3, QTableWidgetItem(employee[3]))
      self.employees_table.setItem(row_number, 4, QTableWidgetItem(str(employee[4])))

  def show_edit_employee_dialog(self):
    # Получение выбранного сотрудника из таблицы
        selected_row = self.employees_table.currentRow()
        if selected_row == -1:
            QWidget.QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для редактирования.")
            return

        employee_id = int(self.employees_table.item(selected_row, 0).text())

        # Создание диалогового окна EditEmployeeDialog
        dialog = EditEmployeeDialog(self.db_manager, employee_id)
        if dialog.exec_():
            if dialog.result() == 200:
              self.update_employees_table()
            
  def delete_employee(self):
    elected_row = self.employees_table.currentRow()
    if elected_row == -1:
      QWidget.QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления.")
      return
    employee_id = int(self.employees_table.item(elected_row, 0).text())
    self.db_manager.delete_employee(employee_id)

    self.update_employees_table()

# Создаем класс для диалогового окна редактирования сотрудника
class EditEmployeeDialog(QDialog):
  def __init__(self, db_manager, employee_data=None, parent=None):
    super().__init__(parent)
    self.db_manager = db_manager
    self.setWindowTitle("Редактировать сотрудника")
    self.layout = QGridLayout(self)

    self.employee_id = employee_data
    self.first_name_input = QLineEdit(self)
    self.last_name_input = QLineEdit(self)
    self.position_input = QLineEdit(self)
    self.salary_input = QLineEdit(self)
    self.save_button = QPushButton("Сохранить", self)
    self.save_button.clicked.connect(self.save_changes)

    db_employee_data = self.db_manager.get_employee_by_id(employee_data)
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

    first_name = self.first_name_input.text()
    last_name = self.last_name_input.text()
    position = self.position_input.text()
    salary = self.salary_input.text()
    self.db_manager.update_employee(self.employee_id, first_name, last_name, position, salary)
    self.done(200)
    self.close()
