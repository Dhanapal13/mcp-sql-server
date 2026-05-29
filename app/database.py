from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
    f"?driver=ODBC+DRIVER+18+for+SQL+Server"
    f"&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommmit=False)