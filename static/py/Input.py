import subprocess
import sqlite3
import os

class Database:
  def __init__(self, app_path):
    self.db_dir = os.path.join(app_path, 'db')
    os.makedirs(self.db_dir, exist_ok=True)
    self.db_path = os.path.join(self.db_dir, 'password.sqlite3')
    self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
    self.c = self.connection.cursor()

  def create_table(self):
    self.c.execute(
      '''
        CREATE TABLE IF NOT EXISTS sudo_password(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT
      );
      '''
    )

  def reg_password(self, password):
    password = str(password)
    self.c.execute(
      f"""
        INSERT INTO sudo_password(password) VALUES (?);
      """, (password,)
    )
    self.connection.commit()

  def get_password(self):
    return self.c.execute(
      """
        SELECT (password) FROM sudo_password WHERE id = 1;
      """
    ).fetchone()

class Input_validator:
  def __init__(self, brightness_level):
    self.brightness_level = str(brightness_level).removesuffix('%')
  
  def __bool__(self):
    try:
      self.brightness_level = int(self.brightness_level)
      return True
    except ValueError:
      return False

  def valid_sudo(self, password):
    result = subprocess.run(
        ['sudo', '-S', '-v'],
        input=f"{password}\n",
        text=True,
        capture_output=True
    )
    #return True if exit code is 0 
    return result.returncode == 0