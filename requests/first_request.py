from postgresql.psql_manager import PsqlManager
from pydantic import BaseModel
from utils import parse_data


settings = parse_data('settings.json')
manager = PsqlManager(
  settings["host"], 
  settings["postgresql"]["port"], 
  settings["postgresql"]["login"], 
  settings["postgresql"]["password"]
)

class PercentageOfVisitsParams(BaseModel):
    lessons_id: list[int]
    start: str
    end: str

def percentage_of_visits(lessons_id: list[int], start: str, end: str):
  query = f'''
      SELECT 
          v.student_id, 
          (count(*) FILTER (WHERE v.visited = TRUE))::float / count(*) * 100 
              as percentage_of_visits
      FROM schedule sch
          JOIN visits v ON sch.id = v.schedule_id
          JOIN lessons ls ON sch.lesson_id = ls.id
      WHERE ls.description_id IN {lessons_id}
          AND v.date BETWEEN {start} AND {end}
      GROUP BY v.student_id
      ORDER BY percentage_of_visits LIMIT 10;
  '''
  manager.execute_and_commit(query)
  return manager.cursor.fetchall()
  