import sublime, sublime_plugin
from threading import Timer
import threading

atshape = "line-vertical"
baseline = 0
forceshapelimit = 5
game = 0
maxshapes = 0
shapeheight = 0
shapewidth = 0
solidifiedRegions = []
text = []

class playCommand(sublime_plugin.TextCommand):

	def run(self, edit, direction="down", gamestate=1, reset=0):

		if reset==1:
			self.view.run_command("reset")

		global baseline
		global shapeheight
		global shapewidth

		x1 = int(self.view.substr(self.view.find("(?<=cx\=)[\d]*", 0)))
		y1 = int(self.view.substr(self.view.find("(?<=cy\=)[\d]*", 0)))

		baseline = y1

		if gamestate==0:
			#game started
			global game
			game = 1
			x1 = 1
			y1 = 1
			sublime.set_timeout(self.descend, 2000)
			self.write("G", 2555)
			self.write("A", 2560)
			self.write("M", 2565)
			self.write("E", 2571)
			self.write("O", 2581)
			self.write("N", 2586)


		if direction == "down" and y1 < (29-shapeheight):
			y1 += 1
		elif direction == "up" and y1 > 1:
			self.rotate()
		elif direction == "left" and x1 > 1:
			x1 -= 1
		elif direction == "right" and x1 < (25-shapewidth):
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
		global atshape
		global shapeheight
		global shapewidth
		if y > 0:
			if atshape == "line-vertical":
				shapeheight = 6
				shapewidth = 1
				while i <= 5:
					z.append("("+str((y+1)*100+y+x)+", "+str((y+1)*100+y+x+1)+")")
					i += 1
					y += 1
			elif atshape == "line-horizontal":
				shapeheight = 1
				shapewidth = 6
				while i <= 5:
					z.append("("+str((y+1)*100+y+x)+", "+str((y+1)*100+y+x+1)+")")
					i += 1
					x += 1
		return z

	def descend(self):
		global baseline
		global maxshapes
		global shapeheight
		global forceshapelimit
		self.view.run_command("play",{"direction" : "down"})
		#print "descending"
		if baseline < (29-shapeheight):			
			sublime.set_timeout(self.descend, 1000)
		elif baseline == (29-shapeheight):
			self.solidify()
			maxshapes +=1
			if maxshapes < forceshapelimit:
				self.view.run_command("play",{"gamestate":0})
			else:
				self.gameover()

	def solidify(self):
		global solidifiedRegions
		solidifiedRegions += self.view.get_regions("player1")
		self.view.add_regions("solidifiedplayer1", solidifiedRegions, "source", sublime.DRAW_EMPTY)

	def rotate(self):
		global atshape
		global baseline
		global shapeheight
		if atshape == "line-vertical":
			atshape = "line-horizontal"
		elif atshape == "line-horizontal" and baseline < 23:
			atshape = "line-vertical"

	def gameover(self):
		global text
		global game
		game = 0
		text = []
		self.write("G", 330)
		self.write("A", 335)
		self.write("M", 340)
		self.write("E", 346)
		self.write("O", 355)
		self.write("V", 360)
		self.write("E", 366)
		self.write("R", 371)

	def write(self, letter, p):
		global text
		sp = self.view.find_all(" ")
		if letter == "G":
			#G ["(10, 11)","(11, 12)","(12, 13)","(13, 14)","(111, 112)","(212, 213)","(313, 314)","(414, 415)","(415, 416)","(416, 417)","(417, 418)","(316, 317)","(215, 216)","(214, 215)"]
			text += ["("+str(p)+", "+str(p+1)+")","("+str(p+1)+", "+str(p+2)+")","("+str(p+2)+", "+str(p+3)+")","("+str(p+3)+", "+str(p+4)+")","("+str(p+101)+", "+str(p+102)+")","("+str(p+202)+", "+str(p+203)+")","("+str(p+303)+", "+str(p+304)+")","("+str(p+404)+", "+str(p+405)+")","("+str(p+405)+", "+str(p+406)+")","("+str(p+406)+", "+str(p+407)+")","("+str(p+407)+", "+str(p+408)+")","("+str(p+306)+", "+str(p+307)+")","("+str(p+205)+", "+str(p+206)+")","("+str(p+204)+", "+str(p+205)+")"]
		elif letter == "A":
			#A ["(419, 420)","(318, 319)","(217, 218)","(116, 117)","(15, 16)","(16, 17)","(17, 18)","(18, 19)","(119, 120)","(220, 221)","(321, 322)","(422, 423)","(218, 219)","(219, 220)"]
			text += ["("+str(p+404)+", "+str(p+405)+")","("+str(p+303)+", "+str(p+304)+")","("+str(p+202)+", "+str(p+203)+")","("+str(p+101)+", "+str(p+102)+")","("+str(p)+", "+str(p+1)+")","("+str(p+1)+", "+str(p+2)+")","("+str(p+2)+", "+str(p+3)+")","("+str(p+3)+", "+str(p+4)+")","("+str(p+104)+", "+str(p+105)+")","("+str(p+205)+", "+str(p+206)+")","("+str(p+306)+", "+str(p+307)+")","("+str(p+407)+", "+str(p+408)+")","("+str(p+203)+", "+str(p+204)+")","("+str(p+204)+", "+str(p+205)+")"]
		elif letter == "M":
			#M ["(424, 425)","(323, 324)","(222, 223)","(121, 122)","(20, 21)","(122, 123)","(224, 225)","(124, 125)","(24, 25)","(125, 126)","(226, 227)","(327, 328)","(428, 429)"]
			text += ["("+str(p+404)+", "+str(p+405)+")","("+str(p+303)+", "+str(p+304)+")","("+str(p+202)+", "+str(p+203)+")","("+str(p+101)+", "+str(p+102)+")","("+str(p)+", "+str(p+1)+")","("+str(p+102)+", "+str(p+103)+")","("+str(p+204)+", "+str(p+205)+")","("+str(p+104)+", "+str(p+105)+")","("+str(p+4)+", "+str(p+5)+")","("+str(p+105)+", "+str(p+106)+")","("+str(p+206)+", "+str(p+207)+")","("+str(p+307)+", "+str(p+308)+")","("+str(p+408)+", "+str(p+409)+")"]
		elif letter == "N":
			#M ["(424, 425)","(323, 324)","(222, 223)","(121, 122)","(20, 21)","(122, 123)","(224, 225)","(124, 125)","(24, 25)","(125, 126)","(226, 227)","(327, 328)","(428, 429)"]
			text += ["("+str(p+404)+", "+str(p+405)+")","("+str(p+303)+", "+str(p+304)+")","("+str(p+202)+", "+str(p+203)+")","("+str(p+101)+", "+str(p+102)+")","("+str(p)+", "+str(p+1)+")","("+str(p+102)+", "+str(p+103)+")","("+str(p+204)+", "+str(p+205)+")","("+str(p+306)+", "+str(p+307)+")","("+str(p+4)+", "+str(p+5)+")","("+str(p+105)+", "+str(p+106)+")","("+str(p+206)+", "+str(p+207)+")","("+str(p+307)+", "+str(p+308)+")","("+str(p+408)+", "+str(p+409)+")"]
		elif letter == "E":
			#E ["(430, 431)","(431, 432)","(432, 433)","(433, 434)","(329, 330)","(228, 229)","(229, 230)","(230, 231)","(231, 232)","(127, 128)","(26, 27)","(27, 28)","(28, 29)","(29, 30)"]
			text += ["("+str(p+404)+", "+str(p+405)+")","("+str(p+405)+", "+str(p+406)+")","("+str(p+406)+", "+str(p+407)+")","("+str(p+407)+", "+str(p+408)+")","("+str(p+303)+", "+str(p+304)+")","("+str(p+202)+", "+str(p+203)+")","("+str(p+203)+", "+str(p+204)+")","("+str(p+204)+", "+str(p+205)+")","("+str(p+205)+", "+str(p+206)+")","("+str(p+101)+", "+str(p+102)+")","("+str(p)+", "+str(p+1)+")","("+str(p+1)+", "+str(p+2)+")","("+str(p+2)+", "+str(p+3)+")","("+str(p+3)+", "+str(p+4)+")"]
		elif letter == "O":
			#O ["(36, 37)","(37, 38)","(38, 39)","(39, 40)","(140, 141)","(241, 242)","(342, 343)","(443, 444)","(442, 443)","(441, 442)","(440, 441)","(339, 340)","(238, 239)","(137, 138)"]
			text += ["("+str(p)+", "+str(p+1)+")","("+str(p+1)+", "+str(p+2)+")","("+str(p+2)+", "+str(p+3)+")","("+str(p+3)+", "+str(p+4)+")","("+str(p+104)+", "+str(p+105)+")","("+str(p+205)+", "+str(p+206)+")","("+str(p+306)+", "+str(p+307)+")","("+str(p+407)+", "+str(p+408)+")","("+str(p+406)+", "+str(p+407)+")","("+str(p+405)+", "+str(p+406)+")","("+str(p+404)+", "+str(p+405)+")","("+str(p+303)+", "+str(p+304)+")","("+str(p+202)+", "+str(p+203)+")","("+str(p+101)+", "+str(p+102)+")"]
		if letter == "V":
			print "here"
			#V ["(41, 42)","(142, 143)","(243, 244)","(345, 346)","(447, 448)","(347, 348)","(247, 248)","(146, 147)","(45, 46)"]
			text += ["("+str(p)+", "+str(p+1)+")","("+str(p+101)+", "+str(p+102)+")","("+str(p+202)+", "+str(p+203)+")","("+str(p+304)+", "+str(p+305)+")","("+str(p+406)+", "+str(p+407)+")","("+str(p+306)+", "+str(p+307)+")","("+str(p+206)+", "+str(p+207)+")","("+str(p+105)+", "+str(p+106)+")","("+str(p+4)+", "+str(p+5)+")"]
		if letter == "R":
			#R
			text += ["("+str(p)+", "+str(p+1)+")","("+str(p+1)+", "+str(p+2)+")","("+str(p+2)+", "+str(p+3)+")","("+str(p+3)+", "+str(p+4)+")","("+str(p+101)+", "+str(p+102)+")","("+str(p+202)+", "+str(p+203)+")","("+str(p+203)+", "+str(p+204)+")","("+str(p+204)+", "+str(p+205)+")","("+str(p+205)+", "+str(p+206)+")","("+str(p+104)+", "+str(p+105)+")","("+str(p+303)+", "+str(p+304)+")","("+str(p+404)+", "+str(p+405)+")","("+str(p+305)+", "+str(p+306)+")","("+str(p+407)+", "+str(p+408)+")"]
		r = []
		for region in sp:
			if str(region) in text:
				r.append(region)
		self.view.add_regions("gameoverregion", r, "source", sublime.DRAW_EMPTY)

class resetCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global solidifiedRegions
		global maxshapes
		global text
		text = []
		solidifiedRegions = []
		maxshapes = 0
		self.view.erase_regions("solidifiedplayer1")
		self.view.erase_regions("gameoverregion")