from sqlalchemy import create_engine

server = "localhost"
database = "FinanceAI"
username = "sysadmin1"
password = "qwertyuiop"

connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(connection_string)