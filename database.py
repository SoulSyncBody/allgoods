# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# 載入 .env 檔案中的所有變數
load_dotenv() 

# 從環境變量中讀取 PostgreSQL 連線 URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trustswap.db") 
# 如果沒有設定 DATABASE_URL，則退回使用 SQLite（用於本地開發和測試）

engine = create_engine(DATABASE_URL)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)