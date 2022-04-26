from flask import Flask, render_template, request, jsonify, make_response
from time import time
from login import *
from os import listdir
import tree

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
			if "agree" in request.args:
				n = tree.node(request.args["content"], request.args["abstract"], login, 1)
			else:
				n = tree.node(request.args["content"], request.args["abstract"], login, 2)
			debats[debat].append_node(parentid, n)
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
			n = debats[debat].find_node(idd)
			if login in n.like:
				n.like.remove(login)
			else:
				n.like.append(login)
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
            n = debats[debat].find_node(idd)
            if login in n.dislike:
                n.dislike.remove(login)
            else:
                n.dislike.append(login)
        return '<meta http-equiv="Refresh" content="0; url=/debate/' + debat+'.html">'
    else:
        return '<meta http-equiv="Refresh" content="0; url=/">'

def save():
	for i in debats:
		f = open("database/debats/" + i, "w")
		f.write (str(debats[i]))
		f.close()
	return "a"

def restore():
	for d in listdir("database/debats"):
		f = open("database/debats/" + d, "r")
		lines = f.readlines()
		f.close()
		i = 0
		for l in lines:
			l = l[0:-1]
			if i == 0:
				author, content, abstract, statut, like, dislike, idd = l.split("\t")
				statut = int(statut)
				like = like.split(" ")
				dislike = dislike.split(" ")
				n = tree.node(content, abstract, author, statut)
				n.id = idd
				n.like = like[0:-1]
				n.dislike = dislike[0:-1]
				debats[d] = n
				i += 1
			else:
				parentid, author, content, abstract, statut, like, dislike, idd = l.split("\t")
				statut = int(statut)
				like = like.split(" ")[0:-1]
				dislike = dislike.split(" ")[0:-1]
				n = tree.node(content, abstract, author, statut)
				n.id = idd
				n.like = like
				n.dislike = dislike
				debats[d].append_node(parentid, n)


@app.route('/debate/<string:link>')
def get_debate(link):
	if check_cookie(request.cookies.get('log', 0)) == True:
		debat, trash = link.split(".")
		tree.to_ret = '<link rel="stylesheet" href="debats.css"><ul class="dropdownmenu">'
		if debat in debats:
			debats[debat].create_html(0,0, debat)
			tree.to_ret += "</ul>"
			return tree.to_ret
		else:
			return '<meta http-equiv="Refresh" content="0; url=/home.html">'
	else:
		return '<meta http-equiv="Refresh" content="0; url=/">'

@app.route('/createDebate', methods=['GET', 'POST'])
def createDebate():
	if request.args["name"] in debats:
		return "you can't choose this name, it's already took"
	login, b ,c = request.cookies.get('log',0).split(" ")
	debats[request.args["name"]] = tree.node(request.args["content"], request.args["abstract"], login, 0)
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
