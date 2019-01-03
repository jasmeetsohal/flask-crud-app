from flask import Flask , render_template
from flask import jsonify 
from flask import request
from bson.json_util import dumps
from dotenv import load_dotenv
from bson.objectid import ObjectId


import pymongo
import os

app = Flask(__name__ ,static_folder='public', template_folder='views') 
load_dotenv()

load_dotenv(verbose=True)

load_dotenv(dotenv_path='.env')

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

connection = pymongo.MongoClient("ds155080.mlab.com", 55080)
db = connection[DB_NAME]

def db_connect():
  try:
    if db.authenticate(DB_USER, DB_PASSWORD):
      print("MongoDB connection Succeed!")
      return True
  except:
    print("Failed to connect MongoDB!")
    return False


@app.route('/')
def landing_page():
  return render_template('index.html')



@app.route('/create',methods=['POST'])
def create_user():
  user = {'username':request.form['username'],'useremail':request.form['useremail']}
  print user
  db_response = db.users.insert_one(user)
  if db_response.inserted_id:
    response = {"status":"insert succeed!"}
  else:
    response = {"status":"insertion failed"}
  return jsonify(response),200


@app.route('/read',methods=['GET'])
def read_user():
  users = dumps(db.users.find({}))
  return users;

@app.route('/update/<userId>',methods=['PUT'])
def update_user(userId):
  db_response = db.users.update_one({'_id':ObjectId(userId)},{'$set':{'username':request.form['username'],'useremail':request.form['useremail']}})
  if db_response.matched_count == 1 and db_response.modified_count == 1:
    response = {"status":"update succeed!"}
  else:
    response = {"status":"no record found"}
        
  return jsonify(response),200

@app.route('/delete/<userId>',methods=['DELETE'])
def delete_user(userId):
  db_response = db.users.delete_one({'_id':ObjectId(userId)})
  if db_response.deleted_count == 1:
    response = {"status":"delete succeed!"}
  else:
    response = {"status":"no record found"}
    
  return jsonify(response),200
  

@app.route("/health-check")
def health_check():
    return jsonify({"health":"ok"})

if __name__ == "__main__":
    db_connect()
    app.run(debug=True)