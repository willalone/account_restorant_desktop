import sys
from PyQt5.QtWidgets import *

from ui.main_window import MainWindow # Импорт главного окна
from db.db_manager import DatabaseManager # Импорт менеджера БД
from components.orders_tab import OrdersTab
from components.employee_tab import EmployeesTab
from components.menu_tab import MenuTab
from components.tables_tab import TablesTab
from components.reports_tab import ReportsTab
from components.inventory_tab import InventoryTab

class RestaurantApp(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.app = app
    self.setWindowTitle("Ресторанное приложение")
    self.resize(800, 600)
    self.db_manager = DatabaseManager("localhost", "new_user", "secure_password", "restaurant") # Инициализация менеджера БД
    self.initUI()

  def initUI(self):
    # Создание главного окна
    self.main_window = MainWindow(app)
    self.setCentralWidget(self.main_window)

    # Добавление вкладок
    self.main_window.tabs.addTab(OrdersTab(self.db_manager), "Заказы")
    self.main_window.tabs.addTab(EmployeesTab(self.db_manager), "Сотрудники")
    self.main_window.tabs.addTab(MenuTab(self.db_manager), "Меню")
    self.main_window.tabs.addTab(TablesTab(self.db_manager), "Столы")
    self.main_window.tabs.addTab(ReportsTab(self.db_manager), "Отчеты")
    self.main_window.tabs.addTab(InventoryTab(self.db_manager), "Склад")

    self.show()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  ex = RestaurantApp()
  ex.show()
  sys.exit(app.exec_())