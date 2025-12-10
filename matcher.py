# matcher.py
from database import db_session
from models import Transaction
from sqlalchemy import or_

# --- 核心自動配對邏輯 ---
def run_matching_engine():
    session = db_session()
    
    # 1. 抓取所有等待配對的紀錄 (Status = 0-New)
    pending_transactions = session.query(Transaction).filter(
        Transaction.status == '0-New'
    ).all()

    print(f"找到 {len(pending_transactions)} 筆等待配對的交易...")
    
    matched_ids = set() # 用來追蹤已配對的ID，避免重複處理

    for trans_a in pending_transactions:
        # 跳過已經被配對的紀錄
        if trans_a.id in matched_ids:
            continue
        
        # 查找潛在的配對 B：
        # 條件：
        # 1. 狀態必須是 0-New 
        # 2. 不能是自己
        # 3. 必須滿足雙向奔赴的條件 (A求 == B有) 且 (A有 == B求)
        
        trans_b = session.query(Transaction).filter(
            Transaction.status == '0-New',
            Transaction.id != trans_a.id,
            # 配對邏輯：A 的求 == B 的有 (且 B 的求 == A 的有，這是雙向配對)
            Transaction.want_item_std == trans_a.have_item_std,
            Transaction.have_item_std == trans_a.want_item_std 
        ).first()

        if trans_b:
            # 2. 執行配對成功和更新狀態
            
            # 確保兩個都沒有被其他迴圈配對
            if trans_b.id not in matched_ids:
                
                # 更新 A 紀錄
                trans_a.status = '1-Matched'
                trans_a.match_id = trans_b.id
                
                # 更新 B 紀錄
                trans_b.status = '1-Matched'
                trans_b.match_id = trans_a.id
                
                matched_ids.add(trans_a.id)
                matched_ids.add(trans_b.id)
                
                print(f"✅ 成功配對: ID {trans_a.id} <-> ID {trans_b.id}")

    session.commit()
    session.close()
    
# --- 運行腳本 ---
if __name__ == '__main__':
    # 這裡的程式碼在您手動執行 matcher.py 時會運行
    from database import init_db
    init_db() # 確保數據庫已初始化
    run_matching_engine()