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
    
    admin = 0
    errorMessage = ""
    
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        adminCode = request.form['adminCode']
        
        if int(adminCode) == ADMIN_CODE:
            admin = 1
            
        if password1 == password2 and password1 != "":
            if firstName != "" and lastName != "" and username != "":
                try:
                    #Insert Person Information
                    query = "SELECT username FROM person WHERE username = '%s'"
                    cur.execute(query % username)
                    results = cur.fetchall()
                    if not results:
                        try:
                            #Insert Person Information
                            query1 = "INSERT INTO person (firstname, lastname, admin, username, password) VALUES (%s, %s, %s, %s, crypt(%s, gen_salt('bf')))"
                            cur.execute(query1, (firstName, lastName, str(admin), username, password1))
                            conn.commit()
                            return redirect(url_for('login'))
                        except:
                            print("Error Registering")
                            errorMessage = "Error Registering"
                    else:
                        print("Username Is Already In Use")
                        errorMessage = "Username Is Already In Use"
                except:
                    print("Error Registering")
                    errorMessage = "Error Registering"
            else:
                print "Either firstName, lastName, or username was left empty"
                errorMessage = "Either First Name, Last Name, or Username Were Left Empty"
        else:
            print("Passwords Do Not Match")
            errorMessage = "Passwords Do Not Match"
        
    
    return render_template('register.html', error = errorMessage)

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            query = "SELECT username, password, admin FROM person WHERE username = %s AND password = crypt(%s, password)"
            cur.execute(query, (username, password))
            results = cur.fetchone()
            
            if results:
                session['username'] = results[0]
                if results[2]:
                    return redirect(url_for('homeAdmin'))
                else:
                    return redirect(url_for('homeStudent'))
            else:
                errorMessage = "Username or Password Incorrect."
        except:
            errorMessage = "Error On Login"
            print("Error On Login")
            
    return render_template('login.html', error = errorMessage)
    
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
    
@app.route('/createQuestion', methods=['GET', 'POST'])
def createQuestion():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    
    if request.method == 'POST':
        if 'questionType' in request.form:
            questionType = request.form['questionType']
        if 'image' in request.form:
            image = request.form['image']
        if 'questionText' in request.form:
            questionText = request.form['questionText']
        if 'answer' in request.form:
            answer = request.form['answer']
        if 'hiddenChoice' in request.form:
            choices = request.form.getlist('hiddenChoice')
        if 'correctAnswer' in request.form:
            correctMultipleChoiceAnswer = request.form['correctAnswer']
            
        if questionType == "shortAnswer":
            print "shortAnswer"
        if questionType == "map":
            print "map"
        if questionType == "multipleChoice":
            print "multipleChoice"
            
    return render_template('createQuestion.html', error=errorMessage)
    
@app.route('/previousQuestions')
def previousQuestions():
    return render_template('previousQuestions.html')
    
@app.route('/viewStatistics')
def viewStatistics():
    return render_template('viewStatistics.html')
    
@app.route('/viewQuestion')
def viewQuestion():
    return render_template('viewQuestion.html')
    
@app.route('/questionBank')
def questionBank():
    return render_template('questionBank.html')
    
@app.route('/closedQuestions')
def closedQuestions():
    return render_template('closedQuestions.html')
    
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)