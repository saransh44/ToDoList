from flask import Flask, render_template, request, session, jsonify, make_response
import MySQLdb

app = Flask(__name__)

# Deletes from SQLDatabase
def deleteFromDB(index):
    db = MySQLdb.connect("localhost", "root", "HerpDerp", "dbToDoList")
    cursor = db.cursor()
    # Prepare SQL query to DELETE required records
    sql = "DELETE FROM ToDoList WHERE id = '%d'" % (index)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    sql = "ALTER TABLE ToDoList drop ID"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    sql = "ALTER TABLE ToDoList ADD id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    cursor.execute("SELECT * FROM ToDoList")
    for row in cursor.fetchall():
        print ("After Delete: ", row[0], " ", row[1])
    # disconnect from server
    db.close()

# Adds Item to SQLDatabase
def pushToDB(push):
    db = MySQLdb.connect("localhost", "root", "HerpDerp", "dbToDoList")
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS ToDoList (
    TODOITEM LONGTEXT,
    id int(11) NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id)
    )"""
    cursor.execute(sql)

    sql = "INSERT INTO ToDoList(TODOITEM) \
                   VALUES ('%s')" % (push)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    cursor.execute("SELECT * FROM ToDoList")
    for row in cursor.fetchall():
        print ("In databases: ", row[0], " ", row[1])
    db.close()

# Updates a paticular entry in the SQLDatabase
def updateDB(id, updateTxt):
    db = MySQLdb.connect("localhost", "root", "HerpDerp", "dbToDoList")
    cursor = db.cursor()
    sql = "UPDATE ToDoList SET TODOITEM = '%s'" % (updateTxt) + "WHERE id = '%d'" % (id)

    cursor.execute(sql)

    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()

# Loads the html source of the to do list website
@app.route('/')
def index():
    app.secret_key = "hiya"
    return render_template('ToDoList.html')

# Recieves the data from the Ajax request and pushes it to the SQLdatanase
@app.route('/todo/create', methods=['POST'])
def create():
    print("In new /todo/create")
    # content = request.data.decode("utf8")
    content = request.form['items']
    pushToDB(content)
    if 'todolist' in session:
        todo = session['todolist']
        todo.append(content)
        session['todolist'] = todo
    else:
        session['todolist'] = [content]

    print(session['todolist'])
    result = {"result": "success"}
    result['data'] = session['todolist']
    return jsonify(session['todolist'])

# Reads the database and sends the data whenever the page is loaded
@app.route('/todo/read', methods=['GET'])
def read():
    if 'todolist' in session:
        return jsonify(session['todolist'])
    else:
        return jsonify([])

# Recieves the data from the Ajax request and updates the SQLdatanase
@app.route('/todo/update', methods=['PUT'])
def update():
    i = int(request.form['index'])
    content = request.form['updateTxt']
    data = session['todolist']
    data[int(i)] = content
    session['todolist'] = data
    updateDB(i, content)
    if 'todolist' in session:
        return jsonify(session['todolist'])

# Recieves the data from the Ajax request and deletes the corresponding data from the SQLdatanase
@app.route('/todo/delete', methods=["DELETE"])
def delete():
    print("from delete")

    i = request.form['index']
    size = request.form['dataSize']

    data = session['todolist']

    index = ((len(data)-1)-(int(size)-1)+int(i))
    # print(index)
    deleteFromDB(index+1)
    del data[(len(data)-1)-(int(size)-1)+int(i)]
    session['todolist'] = data

    print(session['todolist'])
    if 'todolist' in session:
        return jsonify(session['todolist'])

# Clears out the entire database
@app.route('/todo/clear', methods=['DELETE'])
def clear():
    if 'todolist' in session:
        print(session['todolist'])
        session['todolist'].clear()
        db = MySQLdb.connect("localhost", "root", "HerpDerp", "dbToDoList")
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS ToDoList")

        db.close()
        # print("New Session" + str(session['todolist']))
        session.pop('todolist')

    # Handling outcomes
    else:
        print("there is nothing")

    result = {"result": "success"}
    return jsonify(result)

# Running the application with debugging mode 
if __name__ == '__main__':
    app.run(debug = True)
