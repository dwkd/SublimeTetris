import sublime, sublime_plugin

class playCommand(sublime_plugin.TextCommand):
	def run(self, edit, direction):
		x1 = int(self.view.substr(self.view.find("(?<=cx\=)[\d]*", 0)))
		y1 = int(self.view.substr(self.view.find("(?<=cy\=)[\d]*", 0)))
		if direction == "down" and y1 < 23:
			y1 += 1
		elif direction == "up" and y1 > 1:
			y1 -= 1
		elif direction == "left" and x1 > 1:
			x1 -= 1
		elif direction == "right" and x1 < 99:
			x1 += 1

		self.view.replace(edit, self.view.find("cx\=[\d]*", 0), "cx="+str(x1))
		self.view.replace(edit, self.view.find("cy\=[\d]*", 0), "cy="+str(y1))
		
		x = self.getLineCoords(x1,y1)
		a = self.view.find_all(" ")
		b = [] 
		i = 0;
		for g in a:
			if str(g) in x:
				b.append(g)
			i += 1
		self.view.add_regions("player1", b, "source", sublime.DRAW_OUTLINED)
		
	def getLineCoords(self, x, y):
		i = 0
		z = []
		if y > 0:
			while i <= 5:
				z.append("("+str((y+1)*100+y+x)+", "+str((y+1)*100+y+x+1)+")")
				i += 1
				y += 1
		return z
