from http.client import HTTPException

from dotenv import load_dotenv
import pyodbc

import os

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_SERVER},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    print(f"Attempting to connect to database with connection string: {connection_string}")
    if not connection_string:
        raise HTTPException(status_code=500, detail="Database connection string is not properly configured.")
    
    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
