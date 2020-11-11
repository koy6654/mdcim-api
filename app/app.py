from flask import *
from flask_cors import CORS

from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

import requests

from functools import wraps

import json

app = Flask(__name__)
CORS(app)
app.debug=True

# sql과 비교
# insert, insert_one, insert_many = insert
# find = select
# delete = delete
# update = update

def use_mongo(f):
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
@use_mongo
def network():
    network = db.network
    ipv4=request.form.get('ipv4')
    subnetmask=request.form.get('subnetmask')
    gateway=request.form.get('gateway')

    print("Address : "); print(ipv4)
    print("Subnetmask : "); print(subnetmask)
    print("Gateway : "); print(gateway)

    network.update_one({"_id":ObjectId("5fa395be4ca2273f77113fb1")}, {'$set':{"ipv4":ipv4, "subnetmask":subnetmask, "gateway":gateway}})

    return redirect(url_for('index'))

@app.route('/devicesettings/modbusschedules', methods=['GET', 'POST'])
# @use_mongo
def modbus_schedules():
    # modbus_schedules = db.modbus_schedules
    res = requests.get('http://192.168.126.129:5000/schedules')
    data = res.json()
    return jsonify(data)

@app.route('/devicesettings/modbusschedulesadd', methods=['POST'])
@use_mongo
def modbus_schedules_add():
    modbus = db.modbus
    code = request.form.get('modbus_code')
    id = request.form.get('modbus_id')
    host = request.form.get('modbus_host')
    port = request.form.get('modbus_port')
    interval = request.form.get('modbus_interval')
    description = request.form.get('modbus_description')
    key = request.form.get('modbus_template_key')
    note = request.form.get('modbus_template_note')
    type = request.form.get('modbus_template_type')

    modbus.insert_one({"id":id, "host": host, "port": port, "interval":interval, "description": description, "type":type})

    return 'Success'

@app.route('/devicesettings/modbusschedulesedit', methods=['POST'])
@use_mongo
def modbus_schedules_edit():
    modbus = db.modbus
    key = request.form.get('modbus_template_edit_key')
    note = request.form.get('modbus_template_edit_note')
    type = request.form.get('modbus_template_edit_type')



    return 'Success'


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