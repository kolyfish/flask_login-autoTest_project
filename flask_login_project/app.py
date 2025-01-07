from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 模擬資料庫 - 用戶名和密碼
users = {
    f"user{i}@example.com": {
        "password": f"Password{i}!",
        "login_attempts": {"success": 0, "failure": 0},
        "failure_timestamps": [],
        "last_login": None
    } for i in range(1, 21)
}

# 管理者日誌
admin_logs = []

# 密碼規範檢查
def validate_password(password):
    if len(password) < 8:
        return "密碼必須至少包含 8 個字符"
    if not any(char.isupper() for char in password):
        return "密碼必須包含至少一個大寫字母"
    if not any(char.islower() for char in password):
        return "密碼必須包含至少一個小寫字母"
    if not any(char.isdigit() for char in password):
        return "密碼必須包含至少一個數字"
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # 驗證用戶名和密碼
        if email in users and users[email]["password"] == password:
            users[email]["login_attempts"]["success"] += 1
            users[email]["last_login"] = datetime.now()
            session['user'] = email
            admin_logs.append(f"[{datetime.now()}] SUCCESS: {email}")
            return redirect(url_for('welcome', username=email.split('@')[0]))

        # 記錄失敗嘗試
        if email in users:
            users[email]["login_attempts"]["failure"] += 1
            users[email]["failure_timestamps"].append(datetime.now())
        admin_logs.append(f"[{datetime.now()}] FAILURE: {email} - Incorrect credentials")
        return render_template('login.html', error="登入失敗，請檢查帳號或密碼")
    
    return render_template('login.html')

@app.route('/welcome/<username>')
def welcome(username):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    email = session['user']
    user_data = users[email]
    return render_template('welcome.html', username=username, user_data=user_data)

@app.route('/admin_logs')
def admin_logs_view():
    if 'user' not in session or session['user'] != 'user1@example.com':  # 管理者帳號
        return "無權訪問該頁面", 403
    return render_template('admin_logs.html', logs=admin_logs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
