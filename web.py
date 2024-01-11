from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
import pyodbc
import logging

app = Flask(__name__ , template_folder='templates')

# # SQL Server 連接設定
server = 'DESKTOP-A1HOT5N\SQLSERVER2019'
database = 'web'
username = 'sa'
password = 'zynzynii'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = conn.cursor()


@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory('static', filename)

@app.route('/')
def index():
    return render_template('登入畫面.html') 

@app.route('/register', methods=['POST'])
def register_page():
    cursor = conn.cursor()
    使用者名稱 = request.form['fullname']
    帳號 = request.form['username']
    密碼 = request.form['password']
    cursor.execute("INSERT INTO 使用者(帳號,密碼,使用者名稱) VALUES (?, ?, ?)", (帳號,密碼,使用者名稱))
    cursor.commit()

    return render_template('登入畫面.html') 

@app.route('/login', methods=['post'])
def login_page():

    帳號 = request.form['username']
    密碼 = request.form['password']

    cursor.execute("SELECT * FROM 使用者 WHERE 帳號=? and 密碼 = ?", (帳號,密碼))
    user = cursor.fetchone() 

    if user:
        # 成功
        return render_template('新增日記.html')
    else:
        # 失敗
        return render_template('登入畫面.html',error="登入失敗, 請重新登入")



@app.route('/save', methods=['POST'])
def savepage():
    cursor = conn.cursor()
    標題 = request.form['diarytitle']
    日期 = request.form['date']
    心情 = request.form['mood']
    內容 = request.form['area']
    
    cursor.execute("INSERT INTO 日記(標題,心情,內容,日期) VALUES (?, ?, ?, ?)", (標題,心情,內容,日期))
    cursor.commit()
    conn.close()

    return render_template('新增日記.html')

@app.route('/update', methods=['POST'])
def update():
    # item = request.form['username']
    # cursor.execute("SELECT * FROM 使用者名稱 WHERE 使用者 = ?", item)
    # results = cursor.fetchall()
    # cursor = conn.cursor()
    # gender = request.form['gender']
    # birthdate = request.form['birthdate']
    # cursor.execute("INSERT INTO 使用者(性別,生日) VALUES (?, ?)", (gender,birthdate))
    # cursor.commit()

    return render_template('新增日記.html') 

@app.route('/search', methods=['POST'])
def search():
    search_type = request.form.get('searchType')
    search_results = []

    if search_type == 'date':
        date_value = request.form.get('date')
        cursor.execute("SELECT * FROM 日記 WHERE 日期 = ?", date_value)
        search_results = cursor.fetchall()
    elif search_type == 'mood':
        mood_value = request.form.get('mood')
        cursor.execute("SELECT * FROM 日記 WHERE 心情 = ?", mood_value)
        search_results = cursor.fetchall()

    # 將搜尋結果回傳給前端
    return render_template('新增日記.html', results=search_results)

@app.route('/個人資料.html') #導覽列
def personupdate():
    return render_template('個人資料.html') 

@app.route('/新增日記.html') #導覽列
def addupdate():
    return render_template('新增日記.html') 

@app.route('/關於我們.html') #導覽列
def aboutupdate():
    return render_template('關於我們.html') 
app.run()