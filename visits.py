from psql_manager import PsqlManager
from table import Table
import random


class Visits(Table):
  TABLE_NAME = 'visits'

  def __init__(self):
    self.psql = PsqlManager()
    if not self.psql.check_table_exist(self.TABLE_NAME):
      self.create_table()


  def __del__(self):
    self.clear()


  def create_table(self):
    query = f'''
      CREATE TABLE {self.TABLE_NAME} (
        student INT NOT NULL,
        lesson INT NULL
      );
    '''
    self.psql.execute_and_commit(query)


  def insert(self, studentID, lessonID):
    map_key_values = {
      'student': studentID,
      'lesson': lessonID
    }
    self.psql.insert(self.TABLE_NAME, map_key_values)


  def read(self, studentID, lessonID):
    query = f'''
      SELECT * FROM {self.TABLE_NAME} 
      WHERE student = {studentID} 
        AND lesson = {lessonID}
    '''
    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchall()


  def update(self):
    raise Exception("This table is unupdatable.")


  def fill(self, count):
    studentsID = []
    lessonsID = []

    for _ in range(count):
      studentId = random.randint(100000, 999999)
      while (studentId in studentsID):
        studentId = random.randint(100000, 999999)
      studentsID.append(studentId)

      lessonID = random.randint(100000, 999999)
      while (lessonID in lessonsID):
        lessonID = random.randint(100000, 999999)
      lessonsID.append(lessonID)
      
      self.insert(studentId, lessonID)


  def clear(self):
    self.psql.clear_table(self.TABLE_NAME)


  def print(self, studentID, lessonID):
    rows = self.read(studentID, lessonID)
    for row in rows:
      print('student =', row[1], 'lesson =', row[2])


  def print_all(self):
    rows = self.psql.select_all(self.TABLE_NAME)
    print('Table:', self.TABLE_NAME)
    for row in rows:
      print('student =', row[1], 'lesson =', row[2])
