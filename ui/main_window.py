import sys
from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QMenuBar, QMenu, QAction, QMainWindow, QApplication)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.layout = QVBoxLayout(self)

        # Меню
        self.menubar = self.menuBar() # Получаем меню-бар из QMainWindow

        self.fileMenu = QMenu('Файл', self)
        self.editMenu = QMenu('Редактировать', self)
        self.reportMenu = QMenu('Отчеты', self)

        self.menubar.addMenu(self.fileMenu)
        self.menubar.addMenu(self.editMenu)
        self.menubar.addMenu(self.reportMenu)

        # Действия меню
        exitAction = QAction(QIcon('exit.png'), 'Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.app.quit) # Используем app
        self.fileMenu.addAction(exitAction)

        # Вкладки
        self.tabs = QTabWidget(self)
        self.layout.addWidget(self.tabs)

        self.setCentralWidget(QWidget()) #  Установка centralWidget для QVBoxLayout 
        self.centralWidget().setLayout(self.layout) # Установка layout на centralWidget

if __name__ == '__main__':
    app = QApplication(sys.argv) # Создаем экземпляр QApplication
    main_window = MainWindow(app) # Передаем app в MainWindow
    main_window.show()
    sys.exit(app.exec_()) 
