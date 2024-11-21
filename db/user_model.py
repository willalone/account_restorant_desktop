from passlib.hash import bcrypt

class user:
  def __init__(self, user_id, login, password, role):
    self.user_id = user_id
    self.login = login
    self.password = password
    self.role = role

  def check_password(self, password):
    return bcrypt.verify(password, self.password)
