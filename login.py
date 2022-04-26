from time import time
import re

def to_vigenere(string, key):
	ret = ""
	lenkey = len(key)
	for i in range(len(string)):
		ret += chr(ord(string[i]) + ord(key[i % lenkey]))
	return ret

def from_vigenere(string, key):
	ret = ""
	lenkey = len(key)
	for i in range(len(string)):
		ret += chr(ord(string[i]) - ord(key[i % lenkey]))
	return ret

def check_cookie(string):
	if string == 0:
		return False
	login, mdp, tmp = string.split(" ")
	if time() - int(tmp) < 7200:
		mdp = from_vigenere(mdp, tmp)
		return check_mdp(login + " " + mdp + "\n")
	return False

def check_mdp(log):
    f = open("database/logs.txt", "r")
    lines = f.readlines()
    f.close()
    for line in lines:
        if line == log:
            return True
    return False

def check_register(login, mdp, mdp2, mail):
	if mdp != mdp2:
		return "both password should be same"
	if len(mdp) < 6 or len(mdp) > 16:
		return "len of password should be betwen 6 and 16"
	if not (any(char.isdigit() for char in mdp) and any(char.isupper() for char in mdp) and any(char.islower() for char in mdp)) or any(char == ' ' for char in mdp):
		return "password should have one number, one uppercase, one lowercase and should not have space"
	#########################
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	if mail != "" and not re.fullmatch(regex, mail):
		return "invalide mail"
	#########################
	if any(char == ' ' for char in login):
		return "login should not have space"
	f = open("database/logs.txt", "r")
	lines = f.readlines()
	f.close()
	for line in lines:
		_login, _mdp = line.split(" ")
		if _login == login:
			return "login already exist"
	return True

if __name__ =="__main__":
	print(check_register("test", "aaaaaa", "aaaaaa", ""))
