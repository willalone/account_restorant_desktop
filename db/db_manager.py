from http.client import FORBIDDEN
import mysql.connector
from db.user_model import user
from datetime import datetime


class User:
  def __init__(self, username, password):
    self.username = username
    self.password = password

  def check_password(self, password):
    return self.password == password

class DatabaseManager:
  def __init__(self, host, user, password, database):
    self.conn = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=database,
      charset="utf8mb4",
      collation="utf8mb4_unicode_ci" 
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

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username TEXT UNIQUE,
        password TEXT
      )
    """)
    self.conn.commit()


    # Таблица меню
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Menu (
        menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        price DECIMAL(10,2) NOT NULL
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
  def add_employee(self, first_name, last_name, position, salary, login, password, role):
    try:
        # Добавляем пользователя в таблицу users
        sql_user = """
            INSERT INTO users (role) 
            VALUES (%s)
        """
        self.cursor.execute(sql_user, (role,))
        user_id = self.cursor.lastrowid  # Получаем ID только что вставленного пользователя

        # Добавляем сотрудника в таблицу Employees с указанным user_id
        sql_employee = """
            INSERT INTO Employees (first_name, last_name, position, salary, user_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        employee_values = (first_name, last_name, position, salary, user_id)
        self.cursor.execute(sql_employee, employee_values)
        self.cursor.fetchall()  # Закрытие результата, если что-то осталось

        # Получаем ID только что вставленного сотрудника
        employee_id = self.cursor.lastrowid

        # Добавляем логин и пароль в таблицу login_credentials
        sql_credentials = """
            INSERT INTO login_credentials (user_id, login, password)
            VALUES (%s, %s, %s)
        """
        credentials_values = (user_id, login, password)
        self.cursor.execute(sql_credentials, credentials_values)
        self.conn.commit()

    except Exception as e:
        self.conn.rollback()
        raise e

  def get_employees(self):
    sql = """
        SELECT e.employee_id, e.first_name, e.last_name, e.position, e.salary, 
               lc.login, lc.password, u.role
        FROM Employees e
        LEFT JOIN login_credentials lc ON e.user_id = lc.user_id
        LEFT JOIN users u ON e.user_id = u.user_id
    """
    self.cursor.execute(sql)
    return self.cursor.fetchall()
  
  def get_employee_by_id(self, employee_id):
    sql = "SELECT * FROM employees WHERE employee_id = %s"
    with self.conn.cursor() as cursor:
        cursor.execute(sql, (employee_id,))
        return cursor.fetchone()

  def update_employee(self, employee_id, first_name, last_name, position, salary):
    try:
        sql = "UPDATE Employees SET first_name = %s, last_name = %s, position = %s, salary = %s WHERE employee_id = %s"
        val = (first_name, last_name, position, salary, employee_id)
        self.cursor.execute(sql, val)
        self.conn.commit()
    except mysql.connector.Error as e:
        print(f"Error updating employee: {e}")
        self.conn.rollback()  # Откат транзакции в случае ошибки
        raise  # Прокидываем исключение дальше

  def delete_employee(self, employee_id):
    try:
        # Получаем user_id, связанный с этим сотрудником
        sql_get_user_id = "SELECT user_id FROM Employees WHERE employee_id = %s"
        self.cursor.execute(sql_get_user_id, (employee_id,))
        user_id = self.cursor.fetchone()

        if user_id:
            user_id = user_id[0]

            # Удаляем записи из таблицы login_credentials
            sql_delete_credentials = "DELETE FROM login_credentials WHERE user_id = %s"
            self.cursor.execute(sql_delete_credentials, (user_id,))

            # Удаляем сотрудника из таблицы Employees
            sql_delete_employee = "DELETE FROM Employees WHERE employee_id = %s"
            self.cursor.execute(sql_delete_employee, (employee_id,))

            # Удаляем записи из таблицы users
            sql_delete_user = "DELETE FROM users WHERE user_id = %s"
            self.cursor.execute(sql_delete_user, (user_id,))

        # Применяем изменения
        self.conn.commit()

    except Exception as e:
        self.conn.rollback()
        print(f"Ошибка при удалении сотрудника: {e}")
        raise e

    except Exception as e:
        self.conn.rollback()
        print(f"Ошибка при удалении сотрудника: {e}")
        raise e

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

  def get_dish_id_by_name(self, name):
    query = "SELECT menu_item_id FROM menu WHERE name = %s"
    self.cursor.execute(query, (name,))
    result = self.cursor.fetchone()
    return result[0] if result else None

  # Методы для работы с Tables

  def add_table(self, table_number, capacity):
        sql = "INSERT INTO Tables (table_number, capacity) VALUES (%s, %s)"
        val = (table_number, capacity)
        self.cursor.execute(sql, val)
        self.conn.commit()

  def get_table_by_id(self, table_id):
        query = "SELECT table_id, table_number, capacity FROM Tables WHERE table_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (table_id,))
        return cursor.fetchone()

  def update_table(self, table_id, table_number, capacity):
        query = "UPDATE Tables SET table_number = %s, capacity = %s WHERE table_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (table_number, capacity, table_id))
        self.conn.commit()

  def get_tables(self):
        self.cursor.execute("SELECT table_id, table_number, capacity FROM Tables")
        return self.cursor.fetchall()

  def delete_table(self, table_id):
        query = "DELETE FROM Tables WHERE table_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (table_id,))
        self.conn.commit()
  
  # Методы для работы с Orders
  def add_order(self, table_id, employee_id, status):
    sql = """
        INSERT INTO Orders (table_id, employee_id, status)
        VALUES (%s, %s, %s)
    """
    val = (table_id, employee_id, status)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def edit_order(self, order_id, table_id, employee_id, status):
    sql = """
        UPDATE Orders
        SET table_id = %s, employee_id = %s, status = %s
        WHERE order_id = %s
    """
    val = (table_id, employee_id, status, order_id)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def delete_order(self, order_id):
    sql = "DELETE FROM Orders WHERE order_id = %s"
    self.cursor.execute(sql, (order_id,))
    self.conn.commit()

  def get_orders(self):
    self.cursor.execute("SELECT order_id, table_id, employee_id, status FROM Orders")
    return self.cursor.fetchall()
  
  def execute_query(self, query, params=None):
    """Выполняет SQL-запрос и возвращает результат."""
    cursor = self.conn.cursor()  # Используем self.conn, а не self.db_connection
    cursor.execute(query, params or ())
    result = cursor.fetchall()  # Получаем все строки результата
    cursor.close()
    return result

  # Методы для работы с Sales
  def add_sale(self, order_id, sale_date, total_amount):
    sql = "INSERT INTO Sales (order_id, sale_date, total_amount) VALUES (%s, %s, %s)"
    val = (order_id, sale_date, total_amount)
    self.cursor.execute(sql, val)
    self.conn.commit()

  def get_sales_by_day(self, sale_date):
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

    # Метод для получения данных за месяц
  def get_sales_by_month(self, start_date, end_date):
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
  
  # Методы для работы с регистрацией
  def get_user_by_login(self, login, password):
    """Возвращает информацию о пользователе по логину и паролю."""
    self.cursor.execute(
        "SELECT u.user_id, u.role, lc.password FROM users u "
        "JOIN login_credentials lc ON u.user_id = lc.user_id "
        "WHERE lc.login = %s AND lc.password = %s", 
        (login, password)
    )
    user_data = self.cursor.fetchone()
    if user_data:
        return {"user_id": user_data[0], "role": user_data[1], "password": user_data[2]}  # Добавлен password
    else:
        return None

  
