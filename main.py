from http.client import BAD_REQUEST, FORBIDDEN, INTERNAL_SERVER_ERROR, METHOD_NOT_ALLOWED, NOT_FOUND, UNAUTHORIZED
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import create_table_students, create_table_users, get_db
import students_models
import users_models
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
bcrypt = Bcrypt(app)

@app.route('/auth')
@auth.login_required
def get_response():
    data = {
            
            'status': 200,
            'data': 'You are logged in'
        
        }
    
    resp = jsonify(data)
    resp.status_code = 200
    
    return resp

@auth.verify_password
def authenticate(username, password):
    try:
        if username and password:
            db = get_db()
            cursor = db.cursor()
            query = "SELECT password FROM tbl_users WHERE username = ?"
            cursor.execute(query, [username])
            hash = cursor.fetchone()
            if len(hash) == 1:
                pwd = bytes(str(hash[0]), 'utf-8')
                check = bcrypt.check_password_hash(pwd, password)
                return check
            else:
                print('salah login')
                return False
        else:
            print('belum di isi')
            return False
    except:
        print('koreksi kode')
        return False

@app.route('/students', methods=['GET'])
@auth.login_required
def get_students():
    result = students_models.get_students()
    
    data = {
            
            'status': 200,
            'data': result
        
        }
    
    resp = jsonify(data)
    resp.status_code = 200
    
    return resp

@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    result = users_models.get_users()    
    data = {
            
            'status': 200,
            'data': result
        
        }
    
    resp = jsonify(data)
    resp.status_code = 200
    
    return resp

@app.route('/students/<id>', methods=['GET'])
@auth.login_required
def get_student_by_id(id):
    try:
        result = students_models.get_students_by_id(id)
        data = {
                
                'status': 200,
                'data': result
            
            }
        
        resp = jsonify(data)
        resp.status_code = 200
        
        return resp
    except TypeError:
        data = {
                
                'status': 404,
                'message': "Data Not Found"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 404
        
        return resp
    except:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp

@app.route('/users/<id>', methods=['GET'])
@auth.login_required
def get_users_by_id(id):
    try:
        result = users_models.get_users_by_id(id)
        data = {
                
                'status': 200,
                'data': result
            
            }
        
        resp = jsonify(data)
        resp.status_code = 200
        
        return resp
    except TypeError:
        data = {
                
                'status': 404,
                'message': "Data Not Found"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 404
        
        return resp
    except:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp

@app.route('/joinall', methods=['GET'])
@auth.login_required
def get_joinall():
    result = users_models.get_joinall()
    
    data = {
            
            'status': 200,
            'data': result
        
        }
    
    resp = jsonify(data)
    resp.status_code = 200
    
    return resp 

@app.route('/joinone/<id>', methods=['GET'])
@auth.login_required
def get_joinone(id):
    try:
        result = users_models.get_joinone(id)
        data = {
                
                'status': 200,
                'data': result
            
            }
        
        resp = jsonify(data)
        resp.status_code = 200
        
        return resp
    except:
        data = {
                
                'status': 404,
                'message': "Data Not Found"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 404
        
        return resp

@app.route('/students', methods=['POST'])
@auth.login_required
def insert_students():
    try:
        students_details = request.json
        nim = students_details['nim']
        nama = students_details['nama']
        jurusan = students_details['jurusan']
        alamat = students_details['alamat']
        result = students_models.insert_students(nim, nama, jurusan, alamat)
        if result == True:
            data = {
                
                    'status': 201,
                    'message': 'Success!'
                
                }
            
            resp = jsonify(data)
            resp.status_code = 201
            
            return resp
        else:
            data = {
                    
                    'status': 403,
                    'message': "nim is taken"
                
                }
            
            resp = jsonify(data)
            resp.status_code = 403
            
            return resp
    except:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp

@app.route('/users', methods=['POST'])
@auth.login_required
def insert_users():
    try:
        users_details = request.json
        username = users_details['username']
        password = users_details['password']
        students_id = users_details['students_id']
        result = users_models.insert_users(username, password, students_id)
        if result == True:
            data = {
                
                    'status': 201,
                    'message': 'Success!'
                
                }
            
            resp = jsonify(data)
            resp.status_code = 201
            
            return resp
        else:
            data = {
                    
                    'status': 404,
                    'message': "Foreign Key is Not Found !"
                
                }
            resp = jsonify(data)
            resp.status_code = 404
            return resp
    except TypeError:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp
    except ValueError:
        data = {
                
                'status': 403,
                'message': "username or students_id is taken"
            
            }
        resp = jsonify(data)
        resp.status_code = 403
        
        return resp

@app.route('/students/<id>', methods=['PUT'])
@auth.login_required
def update_students(id):
    try:
        students_details = request.json
        id = students_details['id']
        nim = students_details['nim']
        nama = students_details['nama']
        jurusan = students_details['jurusan']
        alamat = students_details['alamat']
        result = students_models.update_students(id, nim, nama, jurusan, alamat)
        if result == True:
            data = {
                
                    'status': 200,
                    'message': 'Success!'
                
                }
            
            resp = jsonify(data)
            resp.status_code = 200
            
            return resp
        else:
            data = {
                    
                    'status': 403,
                    'message': "nim is taken"
                
                }
            
            resp = jsonify(data)
            resp.status_code = 403
            
            return resp
    except:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp

@app.route('/users/<id>', methods=['PUT'])
@auth.login_required
def update_users(id):
    try:
        users_details = request.json
        id = users_details['id']
        username = users_details['username']
        password = users_details['password']
        students_id = users_details['students_id']
        result = users_models.update_users(id, username, password, students_id)
        if result == True:
            data = {
                
                    'status': 200,
                    'message': 'Success!'
                
                }
            
            resp = jsonify(data)
            resp.status_code = 200
            
            return resp
        else:
            data = {
                    
                    'status': 404,
                    'message': "Foreign Key is Not Found !"
                
                }
            resp = jsonify(data)
            resp.status_code = 404
            return resp
    except TypeError:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp
    except ValueError:
        data = {
                
                'status': 403,
                'message': "username or students_id is taken"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 403
        
        return resp

@app.route('/students/<id>', methods=['DELETE'])
@auth.login_required
def delete_students(id):
    try:
        result = students_models.delete_students(id)
        if result == True:
            data = {
                    
                    'status': 200,
                    'message': "Success!"
                
                }
            
            resp = jsonify(data)
            resp.status_code = 200
            
            return resp
        else:
            data = {
                    
                    'status': 403,
                    'message': "Cannot Delete, table tbl_students Still Has Foreign Key in Table tbl_user"
                
                }
            resp = jsonify(data)
            resp.status_code = 403
            return resp
    except:
        data = {
                
                'status': 404,
                'message': "Data Not Found"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 404
        
        return resp

@app.route('/users/<id>', methods=['DELETE'])
@auth.login_required
def delete_users(id):
    try:
        result = users_models.delete_users(id)
        
        data = {
                
                'status': 200,
                'message': "Success!"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 200
        
        return resp
    except:
        data = {
                
                'status': 404,
                'message': "Data Not Found"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 404
        
        return resp

@app.errorhandler(404)
def not_found(error=NOT_FOUND):
    message = {
        
            'status': 404,
            'message': 'Not Found: ' + request.url
        }
    
    resp = jsonify(message)
    resp.status_code = 404
    
    return resp

@app.errorhandler(403)
def not_found(error=FORBIDDEN):
    message = {
        
            'status': 403,
            'message': 'Forbidden Access'
        }
    
    resp = jsonify(message)
    resp.status_code = 403
    
    return resp

@app.errorhandler(405)
def servererror(error=METHOD_NOT_ALLOWED):
    message = {
        
            'status': 405,
            'message': 'method not allowed'
        }
    
    resp = jsonify(message)
    resp.status_code = 405
    
    return resp

@app.errorhandler(500)
def servererror(error=INTERNAL_SERVER_ERROR):
    message = {
        
            'status': 500,
            'message': 'internal server error'
        }
    
    resp = jsonify(message)
    resp.status_code = 500
    
    return resp

@app.errorhandler(400)
def servererror(error=BAD_REQUEST):
    message = {
        
            'status': 400,
            'message': 'Bad Request'
        }
    
    resp = jsonify(message)
    resp.status_code = 400
    
    return resp

@app.errorhandler(401)
def servererror(error=UNAUTHORIZED):
    message = {
        
            'status': 401,
            'message': 'Unauthorized Login'
        }
    
    resp = jsonify(message)
    resp.status_code = 401
    
    return resp

if __name__ == "__main__":
    create_table_students()
    create_table_users()
    #print(get_data())
    app.run(debug=True)
