from PyQt5.QtWidgets import (QWidget, QVBoxLayout)

class OrdersTab(QWidget):
  def __init__(self, db_manager, parent=None):
    super().__init__(parent)
    self.db_manager = db_manager
    self.layout = QVBoxLayout(self)
