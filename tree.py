from time import time

to_ret = ""

def find_node(l, idd):
    if l[7] == idd:
        return l
    for i in l[4]:
        return find_node(i, idd)
    return None

def create_html(l, x, y, name):
	global to_ret
	if l[3] == 0:
		color = "white"
	elif l[3] == 1:
		color = "blue"
	else:
		color = "red"
	plusx = 0
	for i in l[4]:
		x = create_html(i, x+plusx, y+1, name)
		plusx += 1
	to_ret += '''
<form action="/addNode/'''+name+'_'+l[7] + '''">
  <div class="dropdown" style="top:'''  + str(250*y) + '''; left:'''+ str(250*x) +''';position : absolute; z-index: 1;visibility: show;">

    <div class="dropdown-text" style="border:''' + color + ''';border-width:3px;border-style:solid;color:white;">'''+l[2]+ '''<br>----------------------------------</div>
    <input type="checkbox">
    <div class="dropdown-container" style="top:50; left:0;position : absolute; z-index: 1;visibility: show;">
      <div class="inline-block">
        <a href="../like/''' + name+'_'+l[7]+'''"> <img src="../static/like.png" width="20" height="20"> ''' + str(len(l[5])) + ''' </a> 
      </div>
      <div class="inline-block">
        <a href="../dislike/''' + name + '_' + l[7] +'''"> <img src="../static/dislike.png" width="20" height="20"> ''' + str(len(l[5])) + ''' </a>
      </div><br>

      ''' + l[1] + '''
      =======================
      abstract
      <textarea id="abstract", name="abstract", rows="10", cols="30"></textarea>
      content
      <textarea id="content" name="content", rows="20", cols="30"></textarea>
      check if you agree : <input type="checkbox" id="agree" name="agree" value="agree">
      <input type="submit" value="submit">
    </div>
  </div>
</form>'''
	return x

