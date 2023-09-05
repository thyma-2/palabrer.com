from flask import Flask, render_template, request, jsonify, make_response
from time import time
from login import *
from os import listdir
import tree
import pickle

app = Flask(__name__, static_url_path='/static')

debats = {}

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register.html')
def registerhtml():
	return render_template('register.html')

@app.route('/register.css')
def registercss():
	return render_template('register.css')

@app.route('/index.css')
def indexcss():
	return render_template('index.css')

@app.route('/readme.html')
def readmhtml():
	return render_template('readme.html')

@app.route('/debate/debats.css')
def debatscss():
	return render_template('debats.css')

@app.route('/home.html')
def home():
	if check_cookie(request.cookies.get('log', 0)) == True:
		return render_template('home.html')
	return '<meta http-equiv="Refresh" content="0; url=/">'


@app.route('/login', methods=['GET', 'POST'])
def login():
	if check_mdp(request.args["login"] + " " + request.args["password"] + '\n') == True:
		#logged[request.remote_addr] = (time(), request.args["login"])
		ret = make_response('<meta http-equiv="Refresh" content="0; url=/home.html">')
		tmp = str(int(time()))
		cookie = request.args["login"] + " " + to_vigenere(request.args["password"], tmp) + " " + tmp
		ret.set_cookie('log', cookie)
		return ret
	else:
		return "wrong login" + index()

def add_someone(a,b,c):
	f = open("database/logs.txt", "a")
	f.write(a + " " + b + '\n')
	f.close()
	if c != "":
		f = open("database/mails.txt", "a")
		f.write(a + " " + c + '\n')
		f.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
	a = check_register(request.args["uname"], request.args["mdp1"], request.args["mdp2"], request.args["mail"])
	if type(a) == str:
		return a
	add_someone(request.args["uname"], request.args["mdp1"], request.args["mail"])
	return "it worked now you can login"

@app.route('/addNode/<string:link>', methods=['GET', 'POST'])
def addNode(link):
	if check_cookie(request.cookies.get('log', 0)) == True:
		debat, parentid = link.split('_')
		if debat in debats:
			login, b ,c = request.cookies.get('log',0).split(" ")
			parent_node = tree.find_node(debats[debat], parentid)
			if "agree" in request.args:
				parent_node[4].append([login, request.args["content"], request.args["abstract"],  1, [], [], [], str(int(time()))])
			else:
				parent_node[4].append([login, request.args["content"], request.args["abstract"],  2, [], [], [], str(int(time()))])
			return '<meta http-equiv="Refresh" content="0; url=/debate/' + debat+'.html">'
		else:
			return '<meta http-equiv="Refresh" content="0; url=/">'
	else:
		return '<meta http-equiv="Refresh" content="0; url=/">'


@app.route('/like/<string:link>', methods=['GET', 'POST'])
def like(link):
	if check_cookie(request.cookies.get('log', 0)) == True:
		debat, idd = link.split('_')
		if debat in debats:
			login, b ,c = request.cookies.get('log',0).split(" ")
			n = find_node(debats[debat], idd)
			if n != None:
    				if login in n[5]:
	    				n[5].remove(login)
    				else:
    					n[5].append(login)
		return '<meta http-equiv="Refresh" content="0; url=/debate/' + debat+'.html">'
	else:
		return '<meta http-equiv="Refresh" content="0; url=/">'

@app.route('/list.html', methods=['GET'])
def list():
	ret = ""
	for i in debats:
		ret += '<a href="debate/' + i + '.html">' + debats[i].abstract + ' </a>, '
	return ret[0:-2]

@app.route('/dislike/<string:link>', methods=['GET', 'POST'])
def dislike(link):
    if check_cookie(request.cookies.get('log', 0)) == True:
        debat, idd = link.split('_')
        if debat in debats:
            login, b ,c = request.cookies.get('log',0).split(" ")
            n = find_node(debats[debat], idd)
            if login in n[6]:
                n[6].remove(login)
            else:
                n[6].append(login)
        return '<meta http-equiv="Refresh" content="0; url=/debate/' + debat+'.html">'
    else:
        return '<meta http-equiv="Refresh" content="0; url=/">'

def save():
	global debats
	f = open("database/debats.pkl", "wb")
	pickle.dump(debats, f)
	f.close()

def restore():
    global debats
    f = open("database/debats.pkl", "rb")
    debats = pickle.load(f)
    f.close()


@app.route('/debate/<string:link>')
def get_debate(link):
	debat, trash = link.split(".")
	tree.to_ret = '<link rel="stylesheet" href="debats.css"><ul class="dropdownmenu">'
	if debat in debats:
		tree.create_html(debats[debat], 0,0, debat)
		tree.to_ret += "</ul>"
		return tree.to_ret
	else:
		return '<meta http-equiv="Refresh" content="0; url=/home.html">'

@app.route('/createDebate', methods=['GET', 'POST'])
def createDebate():
	if request.args["name"] in debats:
		return "you can't choose this name, it's already took"
	login, b ,c = request.cookies.get('log',0).split(" ")
	debats[request.args["name"]] = [login, request.args["content"], request.args["abstract"],  0, [], [], [], str(int(time()))]
	return '<meta http-equiv="Refresh" content="0; url=/debate/' + request.args["name"] + '.html">'

@app.route('/joinDebate', methods=['GET','POST'])
def joindebat():
	return '<meta http-equiv="Refresh" content="0; url=/debate/' + request.args["name"] + '.html">'

def getip():
	return request.remote_addr

if __name__=="__main__":
	restore()
	app.run(host="0.0.0.0", port=80)
	save()
