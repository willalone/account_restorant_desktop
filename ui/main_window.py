from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QMainWindow, QTabWidget, QMenu, QAction)
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
        self.user_role = user_role  # Сохраняем роль пользователя
        self.db_manager = db_manager  # Сохраняем объект db_manager
        self.setWindowTitle("Главное окно")
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.initUI()

    def initUI(self):
        # Создаем виджеты
        label = QLabel("Это QLabel")
        # Создаем горизонтальный макет
        hbox = QVBoxLayout()
        hbox.addWidget(label)

        # Вкладки
        self.tabs = QTabWidget(self)
        hbox.addWidget(self.tabs)  # Добавляем вкладки в макет

        # Устанавливаем centralWidget
        centralWidget = QWidget()
        centralWidget.setLayout(hbox)  # Устанавливаем макет на центральный виджет
        self.setCentralWidget(centralWidget)

        # Меню
        self.menubar = self.menuBar()  # Получаем меню-бар из QMainWindow

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
        exitAction.triggered.connect(QCoreApplication.quit)  # Используем QCoreApplication для завершения
        self.fileMenu.addAction(exitAction)
