from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
               QVBoxLayout, QHBoxLayout, QGridLayout,
               QTableWidget, QTableWidgetItem, QComboBox,
               QDateEdit)
from PyQt5.QtCore import Qt, QDate 
class ReportsTab(QWidget):
  def __init__(self, db_manager, parent=None):
    super().__init__(parent)
    self.db_manager = db_manager
    self.layout = QVBoxLayout(self)

    # Создаем виджеты
    self.report_type_label = QLabel("Тип отчета:", self)
    self.report_type_combobox = QComboBox(self)
    self.report_type_combobox.addItems(["Продажи за день", "Продажи за неделю", "Продажи за месяц"])

    self.start_date_label = QLabel("Дата начала:", self)
    self.start_date_edit = QDateEdit(self)
    self.start_date_edit.setDate(QDate.currentDate())

    self.end_date_label = QLabel("Дата окончания:", self)
    self.end_date_edit = QDateEdit(self)
    self.end_date_edit.setDate(QDate.currentDate())

    self.generate_report_button = QPushButton("Сгенерировать отчет", self)
    self.generate_report_button.clicked.connect(self.generate_report)

    # Таблица для отчета
    self.report_table = QTableWidget(self)
    self.report_table.setColumnCount(4)
    self.report_table.setHorizontalHeaderLabels(["Название блюда", "Количество", "Сумма", "Дата продажи"])

    # Создаем макеты
    input_layout = QHBoxLayout()
    input_layout.addWidget(self.report_type_label)
    input_layout.addWidget(self.report_type_combobox)
    input_layout.addWidget(self.start_date_label)
    input_layout.addWidget(self.start_date_edit)
    input_layout.addWidget(self.end_date_label)
    input_layout.addWidget(self.end_date_edit)
    input_layout.addWidget(self.generate_report_button)
    self.layout.addLayout(input_layout)

    self.layout.addWidget(self.report_table)

    self.setLayout(self.layout)

  def generate_report(self):
    report_type = self.report_type_combobox.currentText()
    start_date = self.start_date_edit.date().toPyDate()
    end_date = self.end_date_edit.date().toPyDate()

    if report_type == "Продажи за день":
      report_data = self.db_manager.get_sales_by_day(start_date)
    elif report_type == "Продажи за неделю":
      report_data = self.db_manager.get_sales_by_week(start_date, end_date)
    elif report_type == "Продажи за месяц":
      report_data = self.db_manager.get_sales_by_month(start_date, end_date)
    else:
      # Обработка ошибки некорректного типа отчета
      # ...
      return

    # Заполняем таблицу данными
    self.report_table.setRowCount(0)
    for row_number, data_row in enumerate(report_data):
      self.report_table.insertRow(row_number)
      self.report_table.setItem(row_number, 0, QTableWidgetItem(data_row[0]))
      self.report_table.setItem(row_number, 1, QTableWidgetItem(str(data_row[1])))
      self.report_table.setItem(row_number, 2, QTableWidgetItem(str(data_row[2])))
      self.report_table.setItem(row_number, 3, QTableWidgetItem(str(data_row[3])))

# Дополнения для db_manager.py:

  def get_sales_by_day(self, sale_date):
    # Запрос для получения продаж за день
    self.cursor.execute("""
      SELECT 
        m.name, 
        SUM(od.quantity), 
        SUM(od.quantity * m.price), 
        s.sale_date
      FROM 
        Orders o
      JOIN 
        OrderDetails od ON o.order_id = od.order_id
      JOIN 
        Menu m ON od.menu_item_id = m.menu_item_id
      JOIN 
        Sales s ON o.order_id = s.order_id
      WHERE 
        s.sale_date = %s
      GROUP BY 
        m.name
    """, (sale_date,))
    return self.cursor.fetchall()

  def get_sales_by_week(self, start_date, end_date):
    # Запрос для получения продаж за неделю
    self.cursor.execute("""
      SELECT 
        m.name, 
        SUM(od.quantity), 
        SUM(od.quantity * m.price), 
        s.sale_date
      FROM 
        Orders o
      JOIN 
        OrderDetails od ON o.order_id = od.order_id
      JOIN 
        Menu m ON od.menu_item_id = m.menu_item_id
      JOIN 
        Sales s ON o.order_id = s.order_id
      WHERE 
        s.sale_date BETWEEN %s AND %s
      GROUP BY 
        m.name
    """, (start_date, end_date))
    return self.cursor.fetchall()

  def get_sales_by_month(self, start_date, end_date):
    # Запрос для получения продаж за месяц
    self.cursor.execute("""
      SELECT 
        m.name, 
        SUM(od.quantity), 
        SUM(od.quantity * m.price), 
        s.sale_date
      FROM 
        Orders o
      JOIN 
        OrderDetails od ON o.order_id = od.order_id
      JOIN 
        Menu m ON od.menu_item_id = m.menu_item_id
      JOIN 
        Sales s ON o.order_id = s.order_id
      WHERE 
        s.sale_date BETWEEN %s AND %s
      GROUP BY 
        m.name
    """, (start_date, end_date))
    return self.cursor.fetchall()
