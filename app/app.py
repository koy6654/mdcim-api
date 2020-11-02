from flask import *
from flask_cors import CORS

from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

from functools import wraps

import json
# from JSONEncoder import JSONEncoder, MongoEngineJSONEncoder

app = Flask(__name__)
CORS(app)
app.debug=True
# app.json_encoder=MongoEngineJSONEncoder

# sql과 비교
# insert, insert_one, insert_many = insert
# find = select
# delete = delete
# update = update

# localhost:5000에서 받아와서 3000에 표시해주는게 fetch
# localhost:3000에서 클릭으로 5000으로 보내주는건 form 활용 (form의 action을 localhost:5000이 아닌 http://127.0.0.1:5000으로 해야할 것)

def use_db(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        client = MongoClient('mdc-mongodb',27017)
        db=client['mdcim']
        
        g=f.__globals__
        g['db'] = db
        result = f(*args, **kwargs)
        client.close()

        return result
    return wrap

# test
@app.route('/')
def index():
    return redirect("http://127.0.0.1:3000")

@app.route('/devicesettings/network', methods=['GET', 'POST'])
@use_db
def network():
    network = db.network
    ipv4=request.form.get('ipv4')
    subnetmask=request.form.get('subnetmask')
    gateway=request.form.get('gateway')

    print("Address : "); print(ipv4)
    print("Subnetmask : "); print(subnetmask)
    print("Gateway : "); print(gateway)

    # network.insert_one({"ipv4":ipv4, "subnetmask":subnetmask, "gateway":gateway})
    network.update_one({"_id":ObjectId("5f8fc0c7862d12531bdc4751")}, {'$set':{"ipv4":ipv4, "subnetmask":subnetmask, "gateway":gateway}})

    return redirect(url_for('index'))



# @app.route('/register', methods=['GET', 'POST'])
# @use_db
# def register():
#     users=db.users
#     username = request.form.get('username')
#     email = request.form.get('email')
#     password = request.form.get('password')
#     users.insert_one({"username":username, "email":email, "password":password})
#     return redirect(url_for('index'))

# @app.route('/login', methods=['GET' , 'POST'])
# @use_db
# def login():
#     users=db.users
#     username = request.form.get('username')
#     password = request.form.get('password')
#     userfind=users.find()
#     for i in userfind:
#         if i['username'] == username:
#             print('로그인 성공')
#             return redirect(url_for('index'))
#         else:
#             print(i['username'])
#             print('아니야')
#     return redirect(url_for('index'))

# @app.route('/fetchtest')
# def fetchtest():
#     data={'id':{"_id":"1"}, 'title':'this is title' , 'body': 'this is body'}
#     return jsonify([data])

# @app.route('/userlist')
# @use_db
# def userlist():
#     users=db.users
#     userfind=users.find()
#     userlist = []
#     for i in userfind:
#         i = json.loads(json_util.dumps(i))
#         userlist.append(i)
#     # print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
#     # print(userlist)
#     # print(type(userlist))
#     return jsonify(userlist)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5001)