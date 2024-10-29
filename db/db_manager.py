from http.client import FORBIDDEN
import mysql.connector

class DatabaseManager:
  def __init__(self, host, user, password, database):
    self.conn = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=database
    )
    self.cursor = self.conn.cursor()
    self.create_tables()
     

  def create_tables(self):
    # Таблица сотрудников
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Employees (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        position VARCHAR(255) NOT NULL,
        salary DECIMAL(10,2)
      )
    """)

    # Таблица меню
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Menu (
        menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        price DECIMAL(10,2) NOT NULL
      )
    """)

    # Таблица ингредиентов
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Ingredients (
        ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
      )
    """)

    # Таблица состав блюда
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS MenuItemIngredients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        menu_item_id INT NOT NULL,
        ingredient_id INT NOT NULL,
        quantity DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (menu_item_id) REFERENCES Menu(menu_item_id),
        FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
      )
    """)

    # Таблица столов
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Tables (
        table_id INT AUTO_INCREMENT PRIMARY KEY,
        capacity INT NOT NULL
      )
    """)

    # Таблица заказов
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        table_id INT NOT NULL,
        employee_id INT NOT NULL,
        order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(255) DEFAULT 'В обработке',
        FOREIGN KEY (table_id) REFERENCES Tables(table_id),
                FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
      )
    """)

    # Таблица деталей заказа
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS OrderDetails (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        menu_item_id INT NOT NULL,
        quantity INT NOT NULL,
        notes TEXT,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
        FOREIGN KEY (menu_item_id) REFERENCES Menu(menu_item_id)
      )
    """)

    # Таблица склада
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Inventory (
        inventory_id INT AUTO_INCREMENT PRIMARY KEY,
        ingredient_id INT NOT NULL,
        quantity DECIMAL(10,2) NOT NULL,
        unit VARCHAR(255) NOT NULL,
        FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
      )
    """)

    # Таблица смен сотрудников
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS EmployeeShifts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        employee_id INT NOT NULL,
        shift_start TIMESTAMP NOT NULL,
        shift_end TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
      )
    """)

    # Таблица продаж
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Sales (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        sale_date DATE DEFAULT CURRENT_DATE,
        total_amount DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
      )
    """)

    self.conn.commit()

  # Методы для работы с Employees
  def add_employee(self, first_name, last_name, position, salary):
    sql = "INSERT INTO Employees (first_name, last_name, position, salary) VALUES (%s, %s, %s, %s)"
    val = (first_name, last_name, position, salary)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_employees(self):
    self.cursor.execute("SELECT * FROM Employees")
    return self.cursor.fetchall()
  
  def get_employee_by_id(self, employee_id):
    sql = "SELECT * FROM Employees WHERE employee_id = %s"
    self.cursor.execute(sql, (employee_id,))
    return self.cursor.fetchone()

  def update_employee(self, employee_id, first_name, last_name, position, salary):
    sql = "UPDATE Employees SET first_name = %s, last_name = %s, position = %s, salary = %s WHERE employee_id = %s"
    val = (first_name, last_name, position, salary, employee_id)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def delete_employee(self, employee_id):
    sql = "DELETE FROM Employees WHERE employee_id = %s"
    self.cursor.execute(sql, (employee_id,))
    self.conn.commit()

  # Методы для работы с Menu
  def add_menu_item(self, name, category, price):
    sql = "INSERT INTO Menu (name, category, price) VALUES (%s, %s, %s)"
    val = (name, category, price)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def update_menu_item(self, menu_item_id, name, category, price):
    sql = "UPDATE Menu SET name = %s, category = %s, price = %s WHERE menu_item_id = %s"
    val = (name, category, price, menu_item_id)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_menu_items(self):
    self.cursor.execute("SELECT * FROM Menu")
    return self.cursor.fetchall()
  
  def get_menu_item_by_id(self, menu_item_id):
    sql = "SELECT * FROM Menu WHERE menu_item_id = %s"
    self.cursor.execute(sql, (menu_item_id,))
    return self.cursor.fetchone()
  
  def delete_menu_item(self, menu_item_id):
    sql = "DELETE FROM Menu WHERE menu_item_id = %s"
    self.cursor.execute(sql, (menu_item_id,))
    self.conn.commit()
    
  # Методы для работы с Ingredients
  def add_ingredient(self, name):
    sql = "INSERT INTO Ingredients (name) VALUES (%s)"
    val = (name,)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_ingredients(self):
    self.cursor.execute("SELECT * FROM Ingredients")
    return self.cursor.fetchall()

  # Методы для работы с MenuItemIngredients
  def add_menu_item_ingredient(self, menu_item_id, ingredient_id, quantity):
    sql = "INSERT INTO MenuItemIngredients (menu_item_id, ingredient_id, quantity) VALUES (%s, %s, %s)"
    val = (menu_item_id, ingredient_id, quantity)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_menu_item_ingredients(self):
    self.cursor.execute("SELECT * FROM MenuItemIngredients")
    return self.cursor.fetchall()

  def add_table(self, table_number, capacity):
    sql = "INSERT INTO Tables (capacity) VALUES (%s)"
    val = (capacity,) 
    self.cursor.execute(sql, val)
    self.conn.commit()
     

  def get_tables(self):
    self.cursor.execute("SELECT * FROM Tables")
    return self.cursor.fetchall()
  
  # Методы для работы с Orders
  def add_order(self, table_id, employee_id, order_time, status):
    sql = "INSERT INTO Orders (table_id, employee_id, order_time, status) VALUES (%s, %s, %s, %s)"
    val = (table_id, employee_id, order_time, status)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_orders(self):
    self.cursor.execute("SELECT * FROM Orders")
    return self.cursor.fetchall()

  # Методы для работы с OrderDetails
  def add_order_detail(self, order_id, menu_item_id, quantity, notes):
    sql = "INSERT INTO OrderDetails (order_id, menu_item_id, quantity, notes) VALUES (%s, %s, %s, %s)"
    val = (order_id, menu_item_id, quantity, notes)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_order_details(self):
    self.cursor.execute("SELECT * FROM OrderDetails")
    return self.cursor.fetchall()

  # Методы для работы с Inventory
  def add_inventory(self, ingredient_id, quantity, unit):
    sql = "INSERT INTO Inventory (ingredient_id, quantity, unit) VALUES (%s, %s, %s)"
    val = (ingredient_id, quantity, unit)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_inventory(self):
    self.cursor.execute("SELECT * FROM Inventory")
    return self.cursor.fetchall()
  
  def get_products(self):
        # Получаем список ингредиентов из Inventory с помощью JOIN
        sql = """
            SELECT 
                Ingredients.name, 
                Inventory.quantity, 
                Inventory.unit
            FROM 
                Inventory
            JOIN 
                Ingredients ON Inventory.ingredient_id = Ingredients.ingredient_id
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

  # Методы для работы с EmployeeShifts
  def add_employee_shift(self, employee_id, shift_start, shift_end):
    sql = "INSERT INTO EmployeeShifts (employee_id, shift_start, shift_end) VALUES (%s, %s, %s)"
    val = (employee_id, shift_start, shift_end)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_employee_shifts(self):
    self.cursor.execute("SELECT * FROM EmployeeShifts")
    return self.cursor.fetchall()

  # Методы для работы с Sales
  def add_sale(self, order_id, sale_date, total_amount):
    sql = "INSERT INTO Sales (order_id, sale_date, total_amount) VALUES (%s, %s, %s)"
    val = (order_id, sale_date, total_amount)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_sales(self):
    self.cursor.execute("SELECT * FROM Sales")
    return self.cursor.fetchall()

  def close_connection(self):
    self.conn.close()
