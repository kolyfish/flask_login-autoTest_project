from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# 模擬的用戶資料庫
users = {
    "test@example.com": "123"  # 用戶名和密碼
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # 驗證用戶名和密碼
        if email in users and users[email] == password:
            return redirect(url_for('welcome', username=email.split('@')[0]))
        return render_template('login.html', error="登入失敗，請檢查帳號或密碼")
    return render_template('login.html')

@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
