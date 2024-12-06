from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QMainWindow, QTabWidget, QMenu, QAction, QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication  # Добавим импорт QCoreApplication

from components.orders_tab import OrdersTab
from components.employee_tab import EmployeesTab
from components.menu_tab import MenuTab
from components.tables_tab import TablesTab
from components.reports_tab import ReportsTab
from ui.login_window import LoginWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None, user_role=None, db_manager=None, app=None):
        super().__init__(parent)
        self.parent = parent
        self.user_role = user_role
        self.db_manager = db_manager
        self.setWindowTitle("Главное окно")
        self.tabs = QTabWidget()  # Используем одно создание вкладок
        self.setCentralWidget(self.tabs)  # Назначаем вкладки центральным виджетом
        self.initUI()

    def initUI(self):
        # Установка стиля для обводки главного окна
        self.setStyleSheet("""
            QMainWindow {
                border: 2px solid red;
                border-radius: 10px;
            }
        """)

        # Стилизация вкладок
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: 2px solid red; 
                border-radius: 5px; 
            }
            QTabBar::tab {
                background: lightgray;
                border: 1px solid red;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background: white;
                border-color: red;
            }
        """)

        # Создаем виджеты
        label = QLabel("Хочу 5")
        hbox = QVBoxLayout()
        hbox.addWidget(label)

        # Вкладки
        self.tabs = QTabWidget(self)
        hbox.addWidget(self.tabs)

        centralWidget = QWidget()
        centralWidget.setLayout(hbox)
        self.setCentralWidget(centralWidget)

        # Меню
        self.menubar = self.menuBar()
        self.fileMenu = QMenu('Файл', self)
        self.editMenu = QMenu('Редактировать', self)
        self.reportMenu = QMenu('Отчеты', self)

        self.menubar.addMenu(self.fileMenu)
        self.menubar.addMenu(self.editMenu)
        self.menubar.addMenu(self.reportMenu)

        self.tabs.addTab(OrdersTab(self.db_manager, self.user_role), "Заказы")
        self.tabs.addTab(EmployeesTab(self.db_manager), "Сотрудники")
        self.tabs.addTab(MenuTab(self.db_manager), "Меню")
        self.tabs.addTab(TablesTab(self.db_manager), "Столы")
        self.tabs.addTab(ReportsTab(self.db_manager), "Отчеты")

        # Действия меню
        exitAction = QAction(QIcon('exit.png'), 'Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QCoreApplication.quit)
        self.fileMenu.addAction(exitAction)
    
    def showEvent(self, event):
        # Центрируем окно при показе
        screen_geometry = QDesktopWidget().availableGeometry()  # Получаем доступную область экрана
        window_geometry = self.frameGeometry()  # Получаем геометрию текущего окна
        center_point = screen_geometry.center()  # Находим центр экрана
        window_geometry.moveCenter(center_point)  # Перемещаем окно в центр
        self.move(window_geometry.topLeft())  # Перемещаем окно
        super().showEvent(event)  # Не забываем вызвать родительский обработчик
