import sys
from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QMenuBar, QMenu, QAction, QMainWindow, QApplication, QLabel)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = QApplication.instance() # Получаем текущий экземпляр QApplication
        self.initUI()

    def initUI(self):
        # Создаем виджеты
        label = QLabel("Это QLabel")
        # Создаем горизонтальный макет
        hbox = QVBoxLayout()
        hbox.addWidget(label)

        # Вкладки
        self.tabs = QTabWidget(self)
        hbox.addWidget(self.tabs) # Добавляем вкладки в макет

        # Устанавливаем centralWidget
        centralWidget = QWidget()
        centralWidget.setLayout(hbox) # Устанавливаем макет на центральный виджет
        self.setCentralWidget(centralWidget) 

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
        exitAction.triggered.connect(self.app.quit) 
        self.fileMenu.addAction(exitAction)

if __name__ == '__main__':
    app = QApplication(sys.argv) # Создаем экземпляр QApplication
    main_window = MainWindow() # Не нужно передавать app в MainWindow
    main_window.show()
    sys.exit(app.exec_())
