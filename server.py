import psycopg2
import psycopg2.extras
import time
import os
import datetime

from flask import Flask, render_template, request, session, url_for, redirect, send_from_directory

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

ADMIN_CODE = "546238"

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
        
        if adminCode == ADMIN_CODE:
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
                            if admin == 1:
                                os.mkdir("static/pictures/" + username)
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
    
    errorMessage = ""
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            query = "SELECT username, password, admin, personid FROM person WHERE username = %s AND password = crypt(%s, password)"
            cur.execute(query, (username, password))
            results = cur.fetchone()
            
            if results:
                session['username'] = results[0]
                session['admin'] = results[2]
                session['personid'] = results[3]
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
    if 'admin' in session:
        if not session['admin']:
            return redirect(url_for('welcome'))
    else:
        return redirect(url_for('welcome'))

    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    errorMessage = ""
    openQs = [] 
    displayClasses = []
    personClasses = []
    
    try:
        query = "SELECT classid, classname, section FROM class"
        cur.execute(query)
        classes = cur.fetchall()
        try:
            query = "SELECT classid FROM person_class_join WHERE personid = '%s'"
            cur.execute(query % session['personid'])
            results = cur.fetchall()
            
            for item in results:
                personClasses.append(item[0])
            for item2 in classes:
                if item2[0] in personClasses:
                    temp = "" + str(item2[1]) + " " + str(item2[2])
                    temp2 = [item2[0], temp]
                    displayClasses.append(temp2)
        except:
            errorMessage = "Error Getting Person's Classes"
            print "Error Getting Person's Classes" 
    except:
        errorMessage = "Error Gathering All Classes"
        print "Error Gathering All Classes"
        
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (short_answer_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 't' AND t2.questiontype = 'shortAnswer') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (multiple_choice_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 't' AND t2.questiontype = 'multipleChoice') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (map_selection_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 't' AND t2.questiontype = 'map') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
        
    return render_template('homeAdmin.html', openQs = openQs, classes=displayClasses)
    
@app.route('/homeStudent', methods=['GET', 'POST'])
def homeStudent():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    displayClasses = []
    activeClasses = []
    personClasses = []
    openQs = [] 
    
    try:
        query = "SELECT classid, classname, section FROM class"
        cur.execute(query)
        classes = cur.fetchall()
        try:
            query = "SELECT classid FROM person_class_join WHERE personid = '%s'"
            cur.execute(query % session['personid'])
            results = cur.fetchall()
            
            for item in results:
                personClasses.append(item[0])
            for item2 in classes:
                if item2[0] not in personClasses:
                    temp = "" + str(item2[1]) + " " + str(item2[2])
                    displayClasses.append(temp)
                elif item2[0] in personClasses:
                    temp = "" + str(item2[1]) + " " + str(item2[2])
                    temp2 = [item2[0], temp]
                    activeClasses.append(temp2)
        except:
            errorMessage = "Error Getting Person's Classes"
            print "Error Getting Person's Classes" 
    except:
        errorMessage = "Error Gathering All Classes"
        print "Error Gathering All Classes"
        
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (short_answer_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 't' AND t2.questiontype = 'shortAnswer') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (multiple_choice_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 't' AND t2.questiontype = 'multipleChoice') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (map_selection_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 't' AND t2.questiontype = 'map') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    
    return render_template('homeStudent.html', error = errorMessage, classes = displayClasses, activeClasses = activeClasses, openQs = openQs)
    
@app.route('/createQuestion', methods=['GET', 'POST'])
def createQuestion():
    #Checks to make sure that the user is an admin and logged in
    if 'admin' in session:
        if not session['admin']:
            return redirect(url_for('welcome'))
    else:
        return redirect(url_for('welcome'))
    
    #Connect to the database.
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #Instantiate Variables
    errorMessage = ""
    questionType = ""
    questionText = ""
    answer = ""
    choices = []
    correctMultipleChoiceAnswer = ""
    finalImageName = ""
    
    #If the user is attempting to create a question.
    if request.method == 'POST':
        if 'questionType' in request.form:
            questionType = request.form['questionType']
        if 'image' in request.files:
            image = request.files['image']
        if 'questionText' in request.form:
            questionText = request.form['questionText']
        if 'answer' in request.form:
            answer = request.form['answer']
        if 'hiddenChoice' in request.form:
            choices = request.form.getlist('hiddenChoice')
        if 'correctAnswer' in request.form:
            correctMultipleChoiceAnswer = request.form['correctAnswer']
            
        imageName = image.filename
        finalImageName = imageName
        imageName2 = imageName
        counter = 1
        
        while (os.path.isfile("static/pictures/"+session['username']+"/" + imageName)):
            imageName = imageName2 + str(counter)
            imageName2 = image.filename
            finalImageName = imageName
            counter += 1
            
        #Grab the adminID in order to insert the question into the database.
        try:
            query1 = "SELECT personid FROM person WHERE username = '%s'"
            cur.execute(query1 % session['username'])
            result = cur.fetchone()
            adminCreator = result[0]
            
            #If the question is a short answer
            if questionType == "shortAnswer":
                try:
                    #Insert Person Information
                    query = "INSERT INTO short_answer_q (question, image, adminowner, answer) VALUES (%s, %s, %s, %s)"
                    cur.execute(query, (questionText, finalImageName, adminCreator, answer))
                    conn.commit()
                    
                    if image:
                        writeToMe = open("static/pictures/"+session['username']+"/" + finalImageName, "wb+")
                        writeToMe.write(image.read())   
                        writeToMe.close()
                except:
                    errorMessage = "Error Creating Short Answer Question"
                    print "Error Creating Short Answer Question"
                
            elif questionType == "map":
                try:
                    #Insert Person Information
                    query = "INSERT INTO map_selection_q (question, image, adminowner, answer) VALUES (%s, %s, %s, %s)"
                    cur.execute(query, (questionText, finalImageName, adminCreator, answer))
                    conn.commit()
                    
                    if image:
                        writeToMe = open("static/pictures/"+session['username']+"/" + finalImageName, "wb+")
                        writeToMe.write(image.read())   
                        writeToMe.close()
                except:
                    errorMessage = "Error Creating Map Question"
                    print "Error Creating Map Question"
                    
            elif questionType == "multipleChoice":
                try:
                    #Insert Person Information
                    query = "INSERT INTO multiple_choice_q (question, image, adminowner) VALUES (%s, %s, %s)"
                    cur.execute(query, (questionText, finalImageName, adminCreator))
                    conn.commit()
                    
                    if image:
                        writeToMe = open("static/pictures/"+session['username']+"/" + finalImageName, "wb+")
                        writeToMe.write(image.read())   
                        writeToMe.close()
                        
                    try:
                        query = "SELECT questionid FROM multiple_choice_q WHERE question = '%s'"
                        cur.execute(query % questionText)
                        result1 = cur.fetchone()
                        questionid = result1[0]
                        try:
                            query = "INSERT INTO choices (choicetext, questionid) VALUES (%s, %s)"
                            for option in choices:
                                cur.execute(query, (option, questionid))
                            conn.commit()
                            try:
                                query = "SELECT choiceid FROM choices WHERE choicetext = '%s'"
                                cur.execute(query % correctMultipleChoiceAnswer)
                                result = cur.fetchone()
                                answerid = result[0]
                                try:
                                    update = "UPDATE multiple_choice_q SET answerid = %s WHERE questionid = %s"
                                    cur.execute(update, (answerid, questionid))
                                    conn.commit()
                                except:
                                    errorMessage = "Error Creating Multiple Choice Question"
                                    print "Error Updating Question Table with Answerid"
                            except:
                                errorMessage = "Error Creating Multiple Choice Question"
                                print "Error Getting Choiceid"
                        except:
                            errorMessage = "Error Creating Multiple Choice Question"
                            print "Error Inserting Choices"
                    except:
                        errorMessage = "Error Creating Multiple choice Question"
                        print "Error Getting Question ID"
                    
                except:
                    errorMessage = "Error Creating Multiple Choice Question"
                    print "Error Creating Multiple Choice Question"
        except:
            errorMessage = "Error Creating Question. You are not logged in."
            print "Error Creating Question. You are not logged in."
           
    return render_template('createQuestion.html', error=errorMessage)
    
@app.route('/createClass', methods=['GET', 'POST'])
def createClass():
    #Connect to the database.
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    
    if request.method == 'POST':
        className = request.form['className']
        section = request.form['section']
        
        try:
            query = "SELECT classname, section FROM class WHERE classname = %s AND section = %s"
            cur.execute(query, (className, section))
            results = cur.fetchone()
            
            if not results:
                try:
                    query = "INSERT INTO class (classname, section) VALUES (%s, %s)"
                    cur.execute(query, (className, section))
                    conn.commit()
                    try:
                        query = "SELECT classid FROM class WHERE classname = %s AND section = %s"
                        cur.execute(query, (className, section))
                        classid = cur.fetchone()
                        try:
                            query = "INSERT INTO person_class_join (personid, classid) VALUES (%s, %s)"
                            cur.execute(query, (session['personid'], classid[0]))
                            conn.commit()
                        except:
                            errorMessage = "Error Inserting Into Person_Class_Join"
                            print "Error Inserting Into Person_Class_Join"
                    except:
                        errorMessage = "Error Inserting Into Person_Class_Join"
                        print "Error Inserting Into Person_Class_Join"
                except:         
                    errorMessage = "Error Inserting New Class"
                    print "Error Inserting New Class"
            else:
                errorMessage = "Class Already Exists"
                print "Class Already Exists"
        
        except:
            errorMessage = "Error Checking For Class Name and Section"
            print "Error Checking For Class Name and Section"
            
        return redirect(url_for('homeAdmin'))
        
    return render_template('homeAdmin.html', error = errorMessage)    

@app.route('/joinClass', methods=['GET', 'POST'])
def joinClass():
    #Connect to the database.
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    
    if request.method == 'POST':
        className = request.form['availableClasses']
        name = className.rsplit(' ', 1)[0]
        section = className.rsplit(' ', 1)[1]
        try:
            query = "SELECT personid FROM person WHERE username = '%s'"
            cur.execute(query % session['username'])
            result = cur.fetchone()
            personid = result[0]
            try:
                query = "SELECT classid FROM class WHERE classname = %s AND section = %s"
                cur.execute(query, (name, section))
                results = cur.fetchone()
                classid = results[0]
                try:
                    query1 = "INSERT INTO person_class_join (personid, classid) VALUES (%s, %s)"
                    cur.execute(query1, (personid, classid))
                    conn.commit()
                except:
                    errorMessage = "Error Joining New Class"
                    print "Error Inserting New Class"
            except:
                errorMessage = "Error Joining New Class"
                print "Error Getting Classid"
        except:
            errorMessage = "Error Joining New Class"
            print "Error Getting Personid"
            
        return redirect(url_for('homeStudent'))
        
    return render_template('homeStudent.html', error = errorMessage)  

@app.route('/viewStatistics')
def viewStatistics():
    if 'admin' in session:
        if not session['admin']:
            return redirect(url_for('welcome'))
    else:
        return redirect(url_for('welcome'))
        
    return render_template('viewStatistics.html')


@app.route('/viewInstance', methods=['GET', 'POST'])
def viewInstance():
    if 'admin' not in session:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    questionType = ""
    answerInfo = ""
    choiceInfo = []
    questionInfo = []
    errorMessage = ""
    
    if request.method == 'POST':
        instanceID = request.form['instanceID']
        try:
            query1 = "SELECT questionid, questiontype FROM question_instance WHERE instanceid = '%s'"
            cur.execute(query1 % instanceID)
            instanceInfo = cur.fetchone()
            questionID = instanceInfo[0]
            typeID = instanceInfo[1]
            if typeID == "shortAnswer":
                try:
                    questionType = "Short Answer"
                    query1 = "SELECT question, image, answer, adminowner FROM short_answer_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query5 = "SELECT username FROM person WHERE personid = '%s'"
                        cur.execute(query5 % questionInfo[3])
                        creator = cur.fetchone()[0]
                    except:
                        errorMessage = "Error Getting Question Creator"
                        print "Error Getting Question Creator"
                except:
                    errorMessage = "Error Getting Short Answer Question"
                    print "Error Getting Short Answer Question"     
                    
            if typeID == "multipleChoice":
                try:
                    questionType = "Multiple Choice"
                    query1 = "SELECT question, image, answerid, adminowner FROM multiple_choice_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query2 = "SELECT choicetext, choiceid FROM choices WHERE questionid = '%s'"
                        cur.execute(query2 % questionID)
                        choiceInfo = cur.fetchall()
                        try:
                            query3 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                            cur.execute(query3 % questionInfo[2])
                            answerInfo = cur.fetchone()[0]
                            try:
                                query5 = "SELECT username FROM person WHERE personid = '%s'"
                                cur.execute(query5 % questionInfo[3])
                                creator = cur.fetchone()[0]
                            except:
                                errorMessage = "Error Getting Question Creator"
                                print "Error Getting Question Creator"
                        except:
                            errorMessage = "Error Getting Answer"
                            print "Error Getting Answer" 
                    except:
                        errorMessage = "Error Getting Choices"
                        print "Error Getting Choices"  
                except:
                    errorMessage = "Error Getting Multiple Choice Question"
                    print "Error Getting Multiple Choice Question"  
                    
            if typeID == "map":
                try:
                    questionType = "Map"
                    query1 = "SELECT question, image, answer, adminowner FROM map_selection_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query5 = "SELECT username FROM person WHERE personid = '%s'"
                        cur.execute(query5 % questionInfo[3])
                        creator = cur.fetchone()[0]
                    except:
                        errorMessage = "Error Getting Question Creator"
                        print "Error Getting Question Creator"
                except:
                    errorMessage = "Error Getting Map Question"
                    print "Error Getting map Question"  
        except:
            errorMessage = "Error Getting QuestionId"
            print "Error Getting QuestionID"
            
    if not session['admin']:
        return render_template('questionResponse.html', question=questionInfo, creator=creator, choices=choiceInfo, answerMC=answerInfo, questionType=questionType, questionID=questionID, error=errorMessage,instanceID=instanceID)
    else:
        return render_template('viewInstance.html', question=questionInfo, creator=creator, choices=choiceInfo, answerMC=answerInfo, questionType=questionType, questionID=questionID, error=errorMessage)

@app.route('/viewQuestion', methods=['GET', 'POST'])
def viewQuestion():
    if 'admin' in session:
        if not session['admin']:
            return redirect(url_for('welcome'))
    else:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    questionType = ""
    answerInfo = ""
    choiceInfo = []
    questionInfo = []
    errorMessage = ""
    
    
    if request.method == 'POST':
        questionID = request.form['questionID'] 
        typeID = request.form['questionType']
        
        if typeID == "shortAnswer":
            try:
                questionType = "Short Answer"
                query1 = "SELECT question, image, answer FROM short_answer_q WHERE questionid = '%s'"
                cur.execute(query1 % questionID)
                questionInfo = cur.fetchone()
            except:
                errorMessage = "Error Getting Short Answer Question"
                print "Error Getting Short Answer Question"     
                
        if typeID == "multipleChoice":
            try:
                questionType = "Multiple Choice"
                query1 = "SELECT question, image, answerid FROM multiple_choice_q WHERE questionid = '%s'"
                cur.execute(query1 % questionID)
                questionInfo = cur.fetchone()
                try:
                    query2 = "SELECT choicetext FROM choices WHERE questionid = '%s'"
                    cur.execute(query2 % questionID)
                    choiceInfo = cur.fetchall()
                    try:
                        query3 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                        cur.execute(query3 % questionInfo[2])
                        answerInfo = cur.fetchone()[0]
                    except:
                        errorMessage = "Error Getting Answer"
                        print "Error Getting Answer" 
                except:
                    errorMessage = "Error Getting Choices"
                    print "Error Getting Choices"  
            except:
                errorMessage = "Error Getting Multiple Choice Question"
                print "Error Getting Multiple Choice Question"  
                
        if typeID == "map":
            try:
                questionType = "Map"
                query1 = "SELECT question, image, answer FROM map_selection_q WHERE questionid = '%s'"
                cur.execute(query1 % questionID)
                questionInfo = cur.fetchone()
            except:
                errorMessage = "Error Getting Map Question"
                print "Error Getting map Question"  
        
    return render_template('viewQuestion.html', question=questionInfo, choices=choiceInfo, answerMC=answerInfo, questionType=questionType, questionID=questionID, error=errorMessage)

@app.route('/launchQuestion', methods=['GET', 'POST'])
def launchQuestion():
    if 'admin' in session:
        if not session['admin']:
            return redirect(url_for('welcome'))
    else:
        return redirect(url_for('welcome'))
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    if request.method == 'POST':
        questionID = request.form['questionID']
        questionType = request.form['questionType']
        className = request.form['availableClasses']
        name = className.rsplit(' ', 1)[0]
        section = className.rsplit(' ', 1)[1]
        date = str(datetime.date.today())

        try:
            query = "SELECT classid FROM class WHERE classname = %s AND section = %s"
            cur.execute(query, (name, section))
            results = cur.fetchone()
            classid = results[0]
            try:
                query1 = "INSERT INTO question_instance (questionid, classid, questiontype, date) VALUES (%s, %s, %s, %s)"
                cur.execute(query1, (questionID, classid, questionType, date))
                conn.commit()
            except:
                errorMessage = "Error launching instance"
                print "Error launching instance"
        except:
            errorMessage = "Error Getting Classid"
            print "Error Getting Classid"
            
    return redirect(url_for('questionBank'))
     
@app.route('/questionBank')
def questionBank():
    if 'admin' in session:
        if not session['admin']:
            return redirect(url_for('welcome'))
    else:
        return redirect(url_for('welcome'))
    
    #Connect to the database.
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    shortAnswerResults = []
    multipleChoiceResults = []
    mapSelectionResults = []
    
    try:
        query = "SELECT questionid, question FROM short_answer_q WHERE adminowner = '%s'"
        cur.execute(query % session['personid'])
        shortAnswerResults = cur.fetchall()
        try:
            query = "SELECT questionid, question FROM multiple_choice_q WHERE adminowner = '%s'"
            cur.execute(query % session['personid'])
            multipleChoiceResults = cur.fetchall()
            try:
                query = "SELECT questionid, question FROM map_selection_q WHERE adminowner = '%s'"
                cur.execute(query % session['personid'])
                mapSelectionResults = cur.fetchall()
            except:
                errorMessage = "Error extracting map selection questions"
                print "Error extracting map selection questions"
        except:
            errorMessage = "Error Extracting Multiple Questions"
            print "Error Extracting Multiple Questions"
    except:
        errorMessage = "Error Extracting Short Answer Questions"
        print "Error Extracting Short Answer Questions"
        
    displayClasses = []
    personClasses = []
    
    try:
        query = "SELECT classid, classname, section FROM class"
        cur.execute(query)
        classes = cur.fetchall()
        try:
            query = "SELECT classid FROM person_class_join WHERE personid = '%s'"
            cur.execute(query % session['personid'])
            results = cur.fetchall()
            
            for item in results:
                personClasses.append(item[0])
            for item2 in classes:
                if item2[0] in personClasses:
                    temp = "" + str(item2[1]) + " " + str(item2[2])
                    displayClasses.append(temp)
        except:
            errorMessage = "Error Getting Person's Classes"
            print "Error Getting Person's Classes" 
    except:
        errorMessage = "Error Gathering All Classes"
        print "Error Gathering All Classes"
            
    return render_template('questionBank.html', error=errorMessage, shortAnswerQuestions=shortAnswerResults, multipleChoiceQuestions=multipleChoiceResults, mapSelectionQuestions=mapSelectionResults, classes = displayClasses)
    
@app.route('/deleteQuestion', methods=['GET', 'POST'])
def deleteQuestion():
    #We need to delete instances too.
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    
    if request.method == 'POST':
        questionID = request.form['questionID']
        questionType = request.form['questionType']
        
        if questionType == "shortAnswer":
            try:
                query = "DELETE FROM short_answer_q WHERE questionid = '%s'"
                cur.execute(query % questionID)
                conn.commit()
            except:
                errorMessage = "Error Deleting Short Answer Question"
                print "Error Deleting Short Answer Question"
        
        elif questionType == "multipleChoice":
            try:
                query = "DELETE FROM multiple_choice_q WHERE questionid = '%s'"
                cur.execute(query % questionID)
                conn.commit()
                try:
                    query = "DELETE FROM choices WHERE questionid = '%s'"
                    cur.execute(query % questionID)
                    conn.commit()
                except:
                    errorMessage = "Error Deleting Multiple Choice Choices"
                    print "Error Deleting Multiple Choice Choices"
            except:
                errorMessage = "Error Deleting Multiple Choice Question"
                print "Error Deleting Multiple Choice Question"
        
        elif questionType == "map":
            try:
                query = "DELETE FROM map_selection_q WHERE questionid = '%s'"
                cur.execute(query % questionID)
                conn.commit()
            except:
                errorMessage = "Error Deleting Map Selection Question"
                print "Error Deleting Map Selection Question"
        
        return redirect(url_for('questionBank'))

    return render_template('questionBank.html', error=errorMessage)

@app.route('/deleteInstance', methods=['GET', 'POST'])
def deleteInstance():
    #We need to delete instances too.
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    
    if request.method == 'POST':
        instanceID = request.form['instanceID']
        try:
            query = "DELETE FROM question_instance WHERE instanceid = '%s'"
            cur.execute(query % instanceID)
            conn.commit()
        except:
            errorMessage = "Error Deleting Question Instance"
            print "Error Deleting Question Instance"
            
        return redirect(url_for('homeAdmin'))

    return render_template('homeAdmin.html', error=errorMessage)
    
@app.route('/closeInstance', methods=['GET', 'POST'])
def closeInstance():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    
    if request.method == 'POST':
        instanceID = request.form['instanceID']
        try:
            query = "UPDATE question_instance SET open = 'f' WHERE instanceid = '%s'"
            cur.execute(query % instanceID)
            conn.commit()
        except:
            errorMessage = "Error Closing Question Instance"
            print "Error Closing Question Instance"
        
        
        return redirect(url_for('getStatistics'), code = 307)
        
    return render_template('homeAdmin.html', error=errorMessage)

@app.route('/openInstance', methods=['GET', 'POST'])
def openInstance():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    
    if request.method == 'POST':
        instanceID = request.form['instanceID']
        try:
            query = "UPDATE question_instance SET open = 't' WHERE instanceid = '%s'"
            cur.execute(query % instanceID)
            conn.commit()
        except:
            errorMessage = "Error Opening Question Instance"
            print "Error Opening Question Instance"
            
        return redirect(url_for('closedQuestions'))

    return render_template('closedQuestions.html', error=errorMessage)

@app.route('/closedQuestions')
def closedQuestions():
    if 'admin' in session:
        if not session['admin']:
            return redirect(url_for('welcome'))
    else:
        return redirect(url_for('welcome'))

    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    errorMessage = ""
    openQs = [] 
    displayClasses = []
    personClasses = []
    
    try:
        query = "SELECT classid, classname, section FROM class"
        cur.execute(query)
        classes = cur.fetchall()
        try:
            query = "SELECT classid FROM person_class_join WHERE personid = '%s'"
            cur.execute(query % session['personid'])
            results = cur.fetchall()
            
            for item in results:
                personClasses.append(item[0])
            for item2 in classes:
                if item2[0] in personClasses:
                    temp = "" + str(item2[1]) + " " + str(item2[2])
                    temp2 = [item2[0], temp]
                    displayClasses.append(temp2)
        except:
            errorMessage = "Error Getting Person's Classes"
            print "Error Getting Person's Classes" 
    except:
        errorMessage = "Error Gathering All Classes"
        print "Error Gathering All Classes"
        
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (short_answer_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 'f' AND t2.questiontype = 'shortAnswer') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (multiple_choice_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 'f' AND t2.questiontype = 'multipleChoice') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (map_selection_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 'f' AND t2.questiontype = 'map') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"

    return render_template('closedQuestions.html', openQs = openQs, classes=displayClasses)

@app.route('/questionResponse', methods=['GET', 'POST'])
def questionResponse():
    if 'admin' not in session:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    
    if request.method == 'POST':
        instanceID = request.form['instanceID']
        questionType = request.form['questionType']
        
        if questionType == "Short Answer":
            try:
                queryDel = "DELETE FROM short_answer_ans WHERE userid = %s AND instanceid = %s"
                cur.execute(queryDel, (session['personid'], instanceID))
                conn.commit()
            except:
                errorMessage = "Error Deleting Question Response"
                print "Error Deleting Question Response"
                
            response = request.form['response']
            try:
                query = "INSERT INTO short_answer_ans (userid, instanceid, response) VALUES (%s, %s, %s)"
                cur.execute(query, (session['personid'], instanceID, response))
                conn.commit()
            except:
                errorMessage = "Error Responding To Short Answer Question"
                print "Error Responding To Short Answer Question"
                
        elif questionType == 'Multiple Choice':
            try:
                queryDel = "DELETE FROM multiple_choice_ans WHERE userid = %s AND instanceid = %s"
                cur.execute(queryDel, (session['personid'], instanceID))
                conn.commit()
            except:
                errorMessage = "Error Deleting Question Response"
                print "Error Deleting Question Response"
                
            choiceID = request.form['option']
            try:
                query = "INSERT INTO multiple_choice_ans (userid, instanceid, choiceid) VALUES (%s, %s, %s)"
                cur.execute(query, (session['personid'], instanceID, choiceID))
                conn.commit()
            except:
                errorMessage = "Error Responding To Multiple Choice Question"
                print "Error Responding To Multiple Choice Question"
                
        elif questionType == 'Map':
            try:
                queryDel = "DELETE FROM map_selection_ans WHERE userid = %s AND instanceid = %s"
                cur.execute(queryDel, (session['personid'], instanceID))
                conn.commit()
            except:
                errorMessage = "Error Deleting Question Response"
                print "Error Deleting Question Response"
                
            xCoordinate = request.form['xCoordinate']
            yCoordinate = request.form['yCoordinate']
            try:
                query = "INSERT INTO map_selection_ans (userid, instanceid, xco, yco) VALUES (%s, %s, %s, %s)"
                cur.execute(query, (session['personid'], instanceID, xCoordinate, yCoordinate))
                conn.commit()
            except:
                errorMessage = "Error Responding To Map Question"
                print "Error Responding To Map Question"
        
    return redirect(url_for('previousQuestions'))
    
@app.route('/getStatistics', methods=['GET', 'POST'])
def getStatistics():
    
    if 'admin' not in session:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""    
    if request.method == 'POST':
        instanceID = request.form['instanceID']
        choices = []
        results = []
        #questionType = "Multiple Choice"
        #questionInfo = ("Test Quesiton","12")
        try:
            query1 = "SELECT questionid, questiontype FROM question_instance WHERE instanceid = '%s'"
            cur.execute(query1 % instanceID)
            instanceInfo = cur.fetchone()
            questionID = instanceInfo[0]
            typeID = instanceInfo[1]
            if typeID == "shortAnswer":
                try:
                    questionType = "Short Answer"
                    query1 = "SELECT question, image, answer, adminowner FROM short_answer_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query1 = "SELECT response FROM short_answer_ans WHERE userid = %s AND instanceid = %s"
                        cur.execute(query1, (session['personid'], instanceID))
                        response = cur.fetchone()[0]
                        try:
                            query5 = "SELECT username FROM person WHERE personid = '%s'"
                            cur.execute(query5 % questionInfo[3])
                            creator = cur.fetchone()[0]
                        except:
                            errorMessage = "Error Getting Question Creator"
                            print "Error Getting Question Creator"
                    except:
                        errorMessage = "Error Getting Short Anwser Response"
                        print "Error Getting Short Answer Response"
                except:
                    errorMessage = "Error Getting Short Answer Question"
                    print "Error Getting Short Answer Question"     
                    
            if typeID == "multipleChoice":
                try:
                    questionType = "Multiple Choice"
                    query1 = "SELECT question, image, answerid, adminowner FROM multiple_choice_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query2 = "SELECT choicetext, choiceid FROM choices WHERE questionid = '%s'"
                        cur.execute(query2 % questionID)
                        choiceInfo = cur.fetchall()
                        try:
                            query3 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                            cur.execute(query3 % questionInfo[2])
                            answerInfo = cur.fetchone()[0]
                            try:
                                query5 = "SELECT username FROM person WHERE personid = '%s'"
                                cur.execute(query5 % questionInfo[3])
                                creator = cur.fetchone()[0]
                                try:
                                    query1 = "SELECT choiceid FROM multiple_choice_ans WHERE userid = %s AND instanceid = %s"
                                    cur.execute(query1, (session['personid'], instanceID))
                                    responseAnswer = cur.fetchone()[0]
                                    try:
                                        query6 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                                        cur.execute(query6 % responseAnswer)
                                        response = cur.fetchone()[0]
                                    except:
                                        errorMessage = "Error Getting Multiple Choice Answer Response"
                                        print "Error Getting Multiple Choice Answer Response"
                                except:
                                    errorMessage = "Error Getting Multiple Choice Response"
                                    print "Error Getting Multiple Choice Response"
                            except:
                                errorMessage = "Error Getting Question Creator"
                                print "Error Getting Question Creator"
                        except:
                            errorMessage = "Error Getting Answer"
                            print "Error Getting Answer" 
                    except:
                        errorMessage = "Error Getting Choices"
                        print "Error Getting Choices"  
                except:
                    errorMessage = "Error Getting Multiple Choice Question"
                    print "Error Getting Multiple Choice Question"  
                    
            if typeID == "map":
                try:
                    questionType = "Map"
                    query1 = "SELECT question, image, answer, adminowner FROM map_selection_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query5 = "SELECT username FROM person WHERE personid = '%s'"
                        cur.execute(query5 % questionInfo[3])
                        creator = cur.fetchone()[0]
                        try:
                            query1 = "SELECT xco, yco FROM map_selection_ans WHERE userid = %s AND instanceid = %s"
                            cur.execute(query1, (session['personid'], instanceID))
                            response1 = cur.fetchone()
                            response = "(" + str(response1[0]) + ", " + str(response1[1]) + ")"
                        except:
                            errorMessage = "Error Getting Map Response"
                            print "Error Getting Map Response"
                    except:
                        errorMessage = "Error Getting Question Creator"
                        print "Error Getting Question Creator"
                except:
                    errorMessage = "Error Getting Map Question"
                    print "Error Getting map Question"  
        except:
            errorMessage = "Error Getting QuestionId"
            print "Error Getting QuestionID"
        
        if typeID == "shortAnswer":
            try:
                query = "SELECT response FROM short_answer_ans WHERE instanceid = %s"
                cur.execute(query, (instanceID,))
                results = cur.fetchall()
            except:
                errorMessage = "Error Fetching Question Stats"
                print "Error Fetching Question Stats"
                
        elif typeID == 'multipleChoice':
            #choiceID = request.form['option']
            try:
                query = "SELECT t1.choiceid FROM multiple_choice_ans t1 INNER JOIN choices t2 ON t1.choiceid = t2.choiceid WHERE instanceid = %s"
                cur.execute(query, (instanceID,))
                results = cur.fetchall()
                #choices = ("Choicey","Choicer","Choicest","Choico")
                #results = (22,33,44,55)
            except:
                errorMessage = "Error Fetching Question Stats"
                print "Error Fetching Question Stats"
                
        elif typeID == 'map':
            try:
                query = "SELECT xco, yco FROM map_selection_ans WHERE instanceid = %s"
                cur.execute(query, (instanceID,))
                results = cur.fetchall()
            except:
                errorMessage = "Error Fetching Question Stats"
                print "Error Fetching Question Stats"
        print "Results:"
        print results
        print "Choices:"
        print choices
        return render_template('viewStatistics.html', questionType = typeID, error = errorMessage, results = results, questionInfo = questionInfo)
    
    #return redirect(url_for('closedQuestions'))
    
    #    return redirect(url_for('homeAdmin'))
    return render_template('homeAdmin.html', error=errorMessage)

@app.route('/previousQuestions')
def previousQuestions():
    if 'admin' not in session:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    errorMessage = ""
    openQs = [] 
    displayClasses = []
    personClasses = []

    try:
        query = "SELECT classid, classname, section FROM class"
        cur.execute(query)
        classes = cur.fetchall()
        try:
            query = "SELECT classid FROM person_class_join WHERE personid = '%s'"
            cur.execute(query % session['personid'])
            results = cur.fetchall()
            
            for item in results:
                personClasses.append(item[0])
            for item2 in classes:
                if item2[0] in personClasses:
                    temp = "" + str(item2[1]) + " " + str(item2[2])
                    temp2 = [item2[0], temp]
                    displayClasses.append(temp2)
        except:
            errorMessage = "Error Getting Person's Classes"
            print "Error Getting Person's Classes" 
    except:
        errorMessage = "Error Gathering All Classes"
        print "Error Gathering All Classes"
        
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (short_answer_ans t5 INNER JOIN question_instance t2 ON (t5.instanceid = t2.instanceid) INNER JOIN short_answer_q t1 ON (t1.questionid = t2.questionid AND t2.questiontype = 'shortAnswer') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (multiple_choice_ans t5 INNER JOIN question_instance t2 ON (t5.instanceid = t2.instanceid) INNER JOIN multiple_choice_q t1 ON (t1.questionid = t2.questionid AND t2.questiontype = 'multipleChoice') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (map_selection_ans t5 INNER JOIN question_instance t2 ON (t5.instanceid = t2.instanceid) INNER JOIN map_selection_q t1 ON (t1.questionid = t2.questionid AND t2.questiontype = 'map') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"

    return render_template('previousQuestions.html', openQs = openQs, classes=displayClasses)

@app.route('/viewResponse', methods=['GET', 'POST'])
def viewResponse():
    if 'admin' not in session:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    questionType = ""
    answerInfo = ""
    choiceInfo = []
    questionInfo = []
    errorMessage = ""
    response = ""
    
    if request.method == 'POST':
        instanceID = request.form['instanceID']
        try:
            query1 = "SELECT questionid, questiontype FROM question_instance WHERE instanceid = '%s'"
            cur.execute(query1 % instanceID)
            instanceInfo = cur.fetchone()
            questionID = instanceInfo[0]
            typeID = instanceInfo[1]
            if typeID == "shortAnswer":
                try:
                    questionType = "Short Answer"
                    query1 = "SELECT question, image, answer, adminowner FROM short_answer_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query1 = "SELECT response FROM short_answer_ans WHERE userid = %s AND instanceid = %s"
                        cur.execute(query1, (session['personid'], instanceID))
                        response = cur.fetchone()[0]
                        try:
                            query5 = "SELECT username FROM person WHERE personid = '%s'"
                            cur.execute(query5 % questionInfo[3])
                            creator = cur.fetchone()[0]
                        except:
                            errorMessage = "Error Getting Question Creator"
                            print "Error Getting Question Creator"
                    except:
                        errorMessage = "Error Getting Short Anwser Response"
                        print "Error Getting Short Answer Response"
                except:
                    errorMessage = "Error Getting Short Answer Question"
                    print "Error Getting Short Answer Question"     
                    
            if typeID == "multipleChoice":
                try:
                    questionType = "Multiple Choice"
                    query1 = "SELECT question, image, answerid, adminowner FROM multiple_choice_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query2 = "SELECT choicetext, choiceid FROM choices WHERE questionid = '%s'"
                        cur.execute(query2 % questionID)
                        choiceInfo = cur.fetchall()
                        try:
                            query3 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                            cur.execute(query3 % questionInfo[2])
                            answerInfo = cur.fetchone()[0]
                            try:
                                query5 = "SELECT username FROM person WHERE personid = '%s'"
                                cur.execute(query5 % questionInfo[3])
                                creator = cur.fetchone()[0]
                                try:
                                    query1 = "SELECT choiceid FROM multiple_choice_ans WHERE userid = %s AND instanceid = %s"
                                    cur.execute(query1, (session['personid'], instanceID))
                                    responseAnswer = cur.fetchone()[0]
                                    try:
                                        query6 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                                        cur.execute(query6 % responseAnswer)
                                        response = cur.fetchone()[0]
                                    except:
                                        errorMessage = "Error Getting Multiple Choice Answer Response"
                                        print "Error Getting Multiple Choice Answer Response"
                                except:
                                    errorMessage = "Error Getting Multiple Choice Response"
                                    print "Error Getting Multiple Choice Response"
                            except:
                                errorMessage = "Error Getting Question Creator"
                                print "Error Getting Question Creator"
                        except:
                            errorMessage = "Error Getting Answer"
                            print "Error Getting Answer" 
                    except:
                        errorMessage = "Error Getting Choices"
                        print "Error Getting Choices"  
                except:
                    errorMessage = "Error Getting Multiple Choice Question"
                    print "Error Getting Multiple Choice Question"  
                    
            if typeID == "map":
                try:
                    questionType = "Map"
                    query1 = "SELECT question, image, answer, adminowner FROM map_selection_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query5 = "SELECT username FROM person WHERE personid = '%s'"
                        cur.execute(query5 % questionInfo[3])
                        creator = cur.fetchone()[0]
                        try:
                            query1 = "SELECT xco, yco FROM map_selection_ans WHERE userid = %s AND instanceid = %s"
                            cur.execute(query1, (session['personid'], instanceID))
                            response1 = cur.fetchone()
                            response = "(" + str(response1[0]) + ", " + str(response1[1]) + ")"
                        except:
                            errorMessage = "Error Getting Map Response"
                            print "Error Getting Map Response"
                    except:
                        errorMessage = "Error Getting Question Creator"
                        print "Error Getting Question Creator"
                except:
                    errorMessage = "Error Getting Map Question"
                    print "Error Getting map Question"  
        except:
            errorMessage = "Error Getting QuestionId"
            print "Error Getting QuestionID"
            
        return render_template('viewResponse.html', question=questionInfo, creator=creator, choices=choiceInfo, answerMC=answerInfo, questionType=questionType, questionID=questionID, error=errorMessage, instanceID=instanceID, response=response)

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)
