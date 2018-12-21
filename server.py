from flask import Flask
from flask import jsonify 
from flask import request
from bson.json_util import dumps
from dotenv import load_dotenv
from bson.objectid import ObjectId


import pymongo
import os

app = Flask(__name__) 
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



@app.route('/create',methods=['POST'])
def create_user():
  user_name = request.form['username']
  user_email = request.form['useremail']
  db.users.insert_one({
   'username':user_name,
   'useremail':user_email
  })
  return jsonify(request.form)


@app.route('/read',methods=['GET'])
def read_user():
  users = dumps(db.users.find({}))
  return users;

@app.route('/update/<userId>',methods=['PUT'])
def update_user(userId):
  db.users.update_one({'_id':ObjectId(userId)},{'$set':{'username':request.form['username'],'useremail':request.form['useremail']}})
  return jsonify({"status":"update succeed!"});

@app.route('/delete/<userId>',methods=['DELETE'])
def delete_user(userId):
  db.users.delete_one({'_id':ObjectId(userId)})
  return jsonify({"status":"delete succeed!"})
  
@app.route("/")
def hello():
    return "user"

@app.route("/health-check")
def health_check():
    return jsonify({"health":"ok"})

if __name__ == "__main__":
    db_connect()
    app.run()