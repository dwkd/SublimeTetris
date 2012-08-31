import sublime, sublime_plugin
from threading import Timer
import threading

baseline = 0
solidifiedRegions = []
maxshapes = 0

class playCommand(sublime_plugin.TextCommand):

	def run(self, edit, direction="down", gamestate=1, reset=0):

		if reset==1:
			self.view.run_command("reset")

		global baseline

		x1 = int(self.view.substr(self.view.find("(?<=cx\=)[\d]*", 0)))
		y1 = int(self.view.substr(self.view.find("(?<=cy\=)[\d]*", 0)))

		baseline = y1

		if gamestate==0:
			y1 = 1
			sublime.set_timeout(self.descend, 2000)

		if direction == "down" and y1 < 23:
			y1 += 1
		#elif direction == "up" and y1 > 1:
		#	y1 -= 1
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

	def descend(self):
		global baseline
		global maxshapes
		self.view.run_command("play",{"direction" : "down"})
		#print "descending"
		if baseline < 23:			
			sublime.set_timeout(self.descend, 1000)
		elif baseline == 23:
			self.solidify()
			maxshapes +=1
			if maxshapes < 5:
				self.view.run_command("play",{"gamestate":0})
			else:
				self.gameover()

	def solidify(self):
		global solidifiedRegions
		solidifiedRegions += self.view.get_regions("player1")
		self.view.add_regions("solidifiedplayer1", solidifiedRegions, "source", sublime.DRAW_EMPTY)

	def gameover(self):
		sp = self.view.find_all(" ")
		text = ["(10, 11)","(11, 12)","(12, 13)","(13, 14)","(111, 112)","(212, 213)","(313, 314)","(414, 415)","(415, 416)","(416, 417)","(417, 418)","(316, 317)","(215, 216)","(214, 215)","(419, 420)","(318, 319)","(217, 218)","(116, 117)","(15, 16)","(16, 17)","(17, 18)","(18, 19)","(119, 120)","(220, 221)","(321, 322)","(422, 423)","(218, 219)","(219, 220)"]
		r = []
		for region in sp:
			if str(region) in text:
				r.append(region)
		self.view.add_regions("gameoverregion", r, "source", sublime.DRAW_EMPTY)


class resetCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global solidifiedRegions
		global maxshapes
		solidifiedRegions = []
		maxshapes = 0
		self.view.erase_regions("solidifiedplayer1")
		self.view.erase_regions("gameoverregion")