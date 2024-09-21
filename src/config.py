from sqlalchemy import create_engine

def connect_bd():
  return create_engine('postgresql+psycopg2://postgres:admin@localhost:5432/portafolio')