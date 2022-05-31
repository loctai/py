from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
import subprocess
import random
import threading
import time

app=Flask(__name__,template_folder='.')
CORS(app)

def searchUser(id, users):
	return [element for element in users if float(element['id']) == float(id)]

def runEXE():
	cmd = subprocess.Popen(['BillAccept.exe', "http://bill.io"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = cmd.communicate()
	with open("readme.txt",'w',encoding = 'utf-8') as f:
		f.write("out::: "+ str(out))
		f.write('\n')
		f.write("err::: "+ str(err))
	return True

def readData():
	users = []
	_size = os.path.getsize("users.json")
	if(_size) == 0:
		with open("users.json",'w',encoding = 'utf-8') as f:
			f.write('[]')

	with open("users.json", "r", ) as jsonFile:
		users = json.load(jsonFile)
	return users

def writeData(_data):
	with open("users.json",'w',encoding = 'utf-8') as f:
		f.write(json.dumps(_data))

def processData(_id, _amount):
	users = readData()
	if _id is not None and _amount is not None:
		user = searchUser(_id, users)
		if(len(user) == 0):
			users.append({
				"id": int(_id),
				"amount": float(_amount)
			})
		else:
			user[0]["amount"] += float(_amount)
		writeData(users)
		# runEXE()
	return users

@app.route('/', methods= ['GET', 'POST']) 
def home():
	return jsonify({'status': True} )

@app.route('/deposit', methods=['POST']) 
def _shell():	
	_id = request.args.get("id")
	_amount = request.args.get("amount")
	response = processData(_id, _amount)
	return jsonify({'value': response} )

@app.route('/get', methods=['GET']) 
def getValue():
	_id = request.args.get("id")
	users = readData()
	user = searchUser(_id, users) 
	return jsonify({'value': user} )

if __name__ == '__main__':
	app.run(debug=False, host="0.0.0.0", port=8001) 
