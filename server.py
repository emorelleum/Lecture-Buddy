import psycopg2
import psycopg2.extras
import os

from flask import Flask, render_template, request, session, url_for, redirect
app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

ADMIN_CODE = 546238

def connectToDB():
  connectionString = 'dbname=lecturebuddy user=postgres password=beatbox host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/')
def mainIndex():
    return render_template('welcome.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        adminCode = request.form['adminCode']
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
   # if request.method == 'POST':
        #username = request.form['username']
        #password = request.form['password']

        #query = "SELECT username, password FROM admins WHERE username = %s AND password = crypt(%s, password)"
        #cur.execute(query, (username, password))
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
    return render_template('welcome.html')
    
@app.route('/homeAdmin')
def homeAdmin():
    return render_template('homeAdmin.html')
    
@app.route('/homeStudent')
def homeStudent():
    return render_template('homeStudent.html')
    
@app.route('/createQuestion')
def createQuestion():
    return render_template('createQuestion.html')
    
@app.route('/questionResponse')
def questionResponse():
    return render_template('questionResponse.html')
    
@app.route('/viewStatistics')
def viewStatistics():
    return render_template('viewStatistics.html')
    
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)