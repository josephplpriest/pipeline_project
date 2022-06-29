from sqlalchemy import create_engine
import psycopg2

user = "postgres"

pwd = "tdheVArLiBbYGFNLnCI8"

url = "database-1.cluster-cwqkmv4ix7na.us-east-1.rds.amazonaws.com"

port_num = 5432

engine = create_engine(f'postgresql+psycopg2://{user}:{pwd}@{url}:{port_num}')

engine.connect()

print("connected")

