from flask import Flask, render_template, request, redirect, url_for
from database import db_session, init_db
from models import Transaction
import re

app = Flask(__name__)

# --- 核心自動化：數據標準化函式 ---
def standardize_name(name):
    if not name:
        return ""
    # 1. 轉小寫
    std = name.lower()
    # 2. 移除常見贅詞 (可以自己增加)
    for word in ['絕版', '全新', '可議價', ' ']: # 注意這裡包含空格
        std = std.replace(word, '')
    return std

# --- 初始化資料庫 ---


# --- 網頁路由 ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. 接收網頁表單資料
        line_id = request.form['line_id']
        have_raw = request.form['have_item']
        want_raw = request.form['want_item']
        price = request.form['price']

        # 2. 執行自動化標準化
        have_std = standardize_name(have_raw)
        want_std = standardize_name(want_raw)

        # 3. 存入資料庫
        new_trans = Transaction(
            line_id=line_id,
            have_item_raw=have_raw,
            want_item_raw=want_raw,
            price=float(price),
            have_item_std=have_std,  # 這裡存入自動清理過的資料
            want_item_std=want_std
        )
        db_session.add(new_trans)
        db_session.commit()
        
        return redirect(url_for('success'))

    return render_template('index.html')

@app.route('/success')
def success():
    # 顯示目前資料庫裡所有的資料 (監控用)
    all_data = Transaction.query.order_by(Transaction.id.desc()).all()
    return render_template('success.html', transactions=all_data)

# --- 關閉連線 ---
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    # 在啟動前，先初始化數據庫
    with app.app_context():
        init_db()
    
    app.run(debug=True)