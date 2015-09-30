import psycopg2
import psycopg2.extras
import os

from flask import Flask, render_template, request, session, url_for, redirect
app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

def connectToDB():
  connectionString = 'dbname=LectureBuddy user=postgres password=beatbox host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/')
def mainIndex():
    return render_template('index.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
   # if request.method == 'POST':
        #username = request.form['username']
       # password = request.form['password']

        #query = "SELECT username, password FROM admins WHERE username = %s AND password = crypt(%s, password)"
       # cur.execute(query, (username, password))
        #results = cur.fetchone()
        
        #if results:
        #    session['username'] = results[0]
        #    return redirect(url_for('home'))
        #else:
         #   errorMessage = "Username or Password Incorrect."

    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')
    
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)