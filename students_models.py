from db import get_db

# ambil semua data students
def get_students():
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_students"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    
    for row in cursor.fetchall():
        result.append(dict(zip(columns, row))) #konversi ke dictionary
        
    return result

# ambil data students berdasarkan id
def get_students_by_id(id):
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_students WHERE id = ?"
    cursor.execute(query, [id])
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    result.append(dict(zip(columns, cursor.fetchone()))) #konversi ke dictionary
        
    return result

# menambahkan data students
def insert_students(nim, nama, jurusan, alamat):
    db = get_db()
    cursor = db.cursor()
    if valnim(nim) == True:
        query = "INSERT INTO tbl_students(nim, nama, jurusan, alamat) VALUES (?,?,?,?)"
        cursor.execute(query, [nim, nama, jurusan, alamat])
        db.commit()
        return True
    else: return False

# mengubah data students
def update_students(id, nim, nama, jurusan, alamat):
    db = get_db()
    cursor = db.cursor()
    if valnim(nim) == True:
        query = "UPDATE tbl_students SET nim = ?, nama = ?, jurusan = ?, alamat = ? WHERE id = ?"
        cursor.execute(query, [nim, nama, jurusan, alamat, id])
        db.commit()
        return True
    else: return False

# menghapus data students
def delete_students(id):
    db = get_db()
    cursor = db.cursor()
    query = "DELETE FROM tbl_students WHERE id = ?"
    cquery = "SELECT students_id FROM tbl_users WHERE students_id = %s" % id
    data = cursor.execute(cquery)
    result = []
    for row in data:
        result.append(row)
    if result == []:
        cursor.execute(query, [id])
        if len(cursor.fetchall()) == 1:
            db.commit()
            return True
        else:
            raise TypeError
    else:
        return False

# validate nim taken or not yet
def valnim(nim):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM tbl_students WHERE nim = ?"
    cursor.execute(query, [nim])
    if cursor.fetchone() == None:
        return True
    else:
        return False