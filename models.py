from dotenv import load_dotenv
import os
load_dotenv()

# 從 .env 中讀取費率，如果 .env 中沒有，則預設為 0.06 / 60.0
SERVICE_FEE_RATE = float(os.getenv("SERVICE_FEE_RATE", 0.06))
SHIPPING_FEE = float(os.getenv("SHIPPING_FEE", 60.0))
from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    line_id = Column(String(50))
    
    # 原始輸入
    have_item_raw = Column(String(100))
    want_item_raw = Column(String(100))
    price = Column(Float)

    # 自動化處理後的標準名稱 (KEY)
    have_item_std = Column(String(100))
    want_item_std = Column(String(100))

    # 交易狀態 (0-New, 1-Matched)
    status = Column(String(20), default='0-New')
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Transaction {self.id}: {self.have_item_std} <-> {self.want_item_std}>'