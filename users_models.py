from db import get_db
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

# ambil semua data users
def get_users():
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_users"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    
    for row in cursor.fetchall():
        result.append(dict(zip(columns, row))) #konversi ke dictionary
        
    return result

# join tbl_students dan tbl_users
def get_joinall():
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_users INNER JOIN tbl_students ON tbl_users.students_id = tbl_students.id"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    
    for row in cursor.fetchall():
        result.append(dict(zip(columns, row))) #konversi ke dictionary
        
    return result

# ambil data students berdasarkan id
def get_joinone(id):
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_users INNER JOIN tbl_students ON tbl_users.students_id = tbl_students.id WHERE tbl_users.id = ?"
    cursor.execute(query, [id])
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    result.append(dict(zip(columns, cursor.fetchone()))) #konversi ke dictionary
        
    return result

# ambil data students berdasarkan id
def get_users_by_id(id):
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_users WHERE id = ?"
    cursor.execute(query, [id])
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    result.append(dict(zip(columns, cursor.fetchone()))) #konversi ke dictionary
        
    return result

# menambahkan data users
def insert_users(username, password, students_id):
    db = get_db()
    cursor = db.cursor()
    cquery = "SELECT id FROM tbl_students WHERE id = %s" % students_id
    cursor.execute(cquery)
    if cursor.fetchone() == None:
        return False
    else:
        if valuser(username) == True and validstd(students_id) == True:
            password = bcrypt.generate_password_hash(password)
            query = "INSERT INTO tbl_users(username, password, students_id) VALUES (?,?,?)"
            password = password.decode('utf-8')
            cursor.execute(query, [username, password, students_id])
            db.commit()
            return True
        else:
            raise ValueError

# mengubah data users
def update_users(id, username, password, students_id):
    db = get_db()
    cursor = db.cursor()
    cquery = "SELECT id FROM tbl_students WHERE id = %s" % students_id
    cursor.execute(cquery)
    # print(cursor.fetchone())
    if cursor.fetchone() == None:
        return False
    else:
        if valuser(username) == True and validstd(students_id) == True:
            password = bcrypt.generate_password_hash(password)
            query = "UPDATE tbl_users SET username = ?, password = ?, students_id = ? WHERE id = ?"
            password = password.decode('utf-8')
            cursor.execute(query, [username, password, students_id, id])
            db.commit()
            return True
        else:
            raise ValueError

# menghapus data users
def delete_users(id):
    db = get_db()
    cursor = db.cursor()
    query = "DELETE FROM tbl_users WHERE id = ?"
    cursor.execute(query, [id])
    if cursor.fetchone() == None:
        return False
    else:
        db.commit()
        return True

# validate username taken or not yet
def valuser(username):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM tbl_users WHERE username = ?"
    cursor.execute(query, [username])
    if cursor.fetchone() == None:
        return True
    else:
        return False

# validate students_id taken or not yet
def validstd(students_id):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM tbl_users WHERE students_id = ?"
    cursor.execute(query, [students_id])
    if cursor.fetchone() == None:
        return True
    else:
        return False
