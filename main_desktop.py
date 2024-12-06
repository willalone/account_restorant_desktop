import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QCoreApplication


from ui.main_window import MainWindow  # Импорт главного окна
from db.db_manager import DatabaseManager  # Импорт менеджера БД
from components.orders_tab import OrdersTab
from components.employee_tab import EmployeesTab
from components.menu_tab import MenuTab
from components.tables_tab import TablesTab
from components.reports_tab import ReportsTab
from ui.login_window import LoginWindow  # Импорт окна входа

class RestaurantApp(QMainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app  # Инициализируем объект QApplication
        self.db_manager = DatabaseManager("localhost", "new_user", "secure_password", "restaurant")
        self.initUI()

    def initUI(self):
        # Создаем окно входа и показываем его
        self.login_window = LoginWindow(self.db_manager, self)
        self.login_window.show()

        # Главное окно не создается здесь, оно будет создано после входа
        self.main_window = None

    def show_main_window(self, user_role):
        print(f"Showing main window for role: {user_role}")
        try:
            # Проверим, что main_window создается корректно
            self.main_window = MainWindow(self, user_role, self.db_manager)
            self.main_window.show()
            print("Main window shown")

            # Закрытие окна входа
            self.login_window.hide()  # Закрываем только окно входа
            print("Login window closed")

        except Exception as e:
            print(f"Error in creating main window: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаем объект QApplication
    ex = RestaurantApp(app)  # Передаем объект приложения в RestaurantApp
    sys.exit(app.exec_())  # Запуск основного цикла обработки событий
