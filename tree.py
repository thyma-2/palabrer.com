from time import time

to_ret = ""

class node:
	def __init__(self, content, abstract, author, statut):
		self.author = author
		self.content = content
		self.abstract = abstract
		self.statut = statut
		self.children = []
		self.like = []
		self.dislike = []
		self.id = str(int(time()))

	def __str__(self):
		ret = self.author +'\t' + self.content + '\t' + self.abstract + '\t' + str(self.statut) + '\t'
		for i in self.like:
			ret += i + '\t'
		ret += '\t'
		for i in self.dislike:
			ret += i + '\t'
		ret += '\t' + self.id
		for i in self.children:
			ret += '\n' + self.id + '\t' +  str(i)
		return ret

	def append_node(self, parentid, node):
		if parentid == self.id:
			self.children.append(node)
			return
		for i in self.children:
			i.append_node(parentid, node)

	def find_node(self, idd):
		if self.id == idd:
			return self
		for i in self.children:
			a = i.find_node(idd)
			if a != None:
				return a
		return None

	def create_html(self, x, y, name):
		global to_ret
		if self.statut == 0:
			color = "white"
		elif self.statut == 1:
			color = "blue"
		else:
			color = "red"
		to_ret += '''
	<li>
        <form action="/addNode/'''+name+'_'+self.id + '''">
            <a>
                <div style="top: '''  + str(250*y) + '''; left:'''+ str(250*x) + ''';position : absolute; z-index: 1;visibility: show;">
                    <h4 style="border:''' + color + ''';border-width:3px;border-style:solid;">''' +   self.abstract + ''' </h4>       
                </div>
            </a>
            <div style="top: '''  + str(250*y) + '''; left:'''+ str(250*x) + ''';position : absolute; z-index: 1;visibility: show;">
                <ul>
                    <li>
						<a href="../like/''' + name+'_'+self.id+'''">
         <img alt="Qries" src="../static/like.png"
         width="20" height="20"> ''' + str(len(self.like)) + '''
                        <a href="../dislike/''' + name + '_' + self.id +'''">
         <img alt="Qries" src="../static/dislike.png"
         width="20" height="20"> ''' + str(len(self.dislike)) + '''
						<a> author : ''' + self.author + '''</a>
						<a> </a>
                        <a>''' + self.content + '''</a>
						<a> </a>
                        <a> abstract </a>
                        <a><textarea id="abstract", name="abstract", rows="10", cols="30"></textarea></a>
                        <a>content</a>
                        <a><textarea id="content" name="content", rows="20", cols="30"></textarea></a>
						<a> check if you agree : <input type="checkbox" id="agree" name="agree" value="agree"></a>
                        <a><input type="submit" value="submit"></a></li>
                    </li>
                </ul>
            </div>
        </form>
    </li>'''
		for i in range (0,len(self.children)):
			if i > 0:	
				x += 1
			x = self.children[i].create_html(x, y+1, name)
		return x


if __name__ == "__main__":
	a = node("aaa", "1111", "b", 0)
	b = node("bbb", "2222", "b", 1)
	c = node("ccc", "3333", "b", 1)
	d = node("ddd", "4444", "b", 1)
	e = node("eee", "5555", "b", 2)
	f = node("fff", "6666", "b", 2)
	g = node("ggg", "7777", "b", 2)
	a.children.append(b)
	a.children.append(c)
	a.children.append(d)
	b.children.append(f)
	b.children.append(e)
	c.children.append(g)
	a.create_html(0,0)
	print('<link rel="stylesheet" href="debats.css"><ul class="dropdownmenu">')
	print(to_ret)
	print('</ul>')
