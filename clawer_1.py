# for web page parsing
import requests
from bs4 import BeautifulSoup

# for browser opening
import webbrowser

# for threading
from threading import Thread

# for UI
#import tkinter as tk
from tkinter import Tk, Text, BOTH, W, N, E, S, NW, END
from tkinter import Frame, Button, Label, Entry
from tkinter import StringVar

import queue
import threading
import time

class Application(Frame):
	
	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		
		self.createWidgets()
		#self.sniffUrl()
		self.count_down()
	
	def createWidgets(self):
		# set title
		self.parent.title("page sniffer")
		self.pack(fill=BOTH, expand=1)
		
		self.columnconfigure(1, weight=1)
		self.columnconfigure(3, pad=7)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(5, pad=7)

		global t_url
		global l_DnCnt_2
		global v_DnCnt_2
		global t_targetStr
		global t_filterStr
		v_DnCnt_2 = StringVar()
		
		self.l_DnCnt_1 = Label(self)
		self.l_DnCnt_1["text"] = "重試時間"
		self.l_DnCnt_1.grid(sticky=W, pady=4, padx=5, row=0, column=0)
		
		self.l_DnCnt_2 = l_DnCnt_2= Label(self)
		v_DnCnt_2.set("60")
		self.l_DnCnt_2["textvariable"] = v_DnCnt_2
		self.l_DnCnt_2.grid(sticky=W, pady=4, padx=5, row=0, column=1)
		
		self.l_url_text = Label(self)
		self.l_url_text["text"] = "監測網址"
		self.l_url_text.grid(sticky=W, pady=4, padx=5, row=1, column=0)
		
		self.t_url = t_url = Entry(self, width=50)
		self.t_url.delete(0, END)
		self.t_url.insert(0,"http://www.coolpc.com.tw/phpBB2/portal.php")
		self.t_url.grid(sticky=W, pady=4, padx=5, row=1, column=1, columnspan=3)
		
		self.l_targetStr = Label(self)
		self.l_targetStr["text"] = "目標字串"
		self.l_targetStr.grid(sticky=W, pady=4, padx=5, row=2, column=0)
		
		self.t_targetStr = t_targetStr = Entry(self, width=10)
		self.t_targetStr.delete(0, END)
		self.t_targetStr.insert(0,"限時")
		self.t_targetStr.grid(sticky=W, pady=4, padx=5, row=2, column=1)
		
		self.l_filterStr = Label(self)
		self.l_filterStr["text"] = "排除字串"
		self.l_filterStr.grid(sticky=E, pady=4, padx=5, row=2, column=2)
		
		self.t_filterStr = t_filterStr = Entry(self, width=10)
		self.t_filterStr.delete(0, END)
		self.t_filterStr.insert(0,"已搶畢")
		self.t_filterStr.grid(sticky=E, pady=4, padx=5, row=2, column=3)
		
		self.b_Restart = Button(self)
		self.b_Restart["text"] = "立即重試"
		self.b_Restart["command"] = self.rb_click
		self.b_Restart.grid(sticky=W, pady=4, padx=5, row=5, column=1)
		
		self.QUIT = Button(self, text="QUIT", fg="red",
			command=self.parent.destroy)
		self.QUIT.grid(sticky=W, pady=4, padx=5, row=5, column=5)
	
	

	def setDnCnt(sec):
		l_DnCnt_2.text(sec)
	
	def rb_click(self):
		"""
		aaa = t_filterStr.get()
		#aaa.decode
		print(aaa.encode('unicode-escape').decode())
		"""
		self.queue = queue.Queue()
		ThreadedTask(self.queue).start()
		self.master.after(100, self.process_queue)
		v_DnCnt_2.set(str(59))
	def process_queue(self):
		try:
			msg = self.queue.get(0)
			# Show result of the task if needed
		except queue.Empty:
			self.master.after(100, self.process_queue)
	
	def count_down(self):
		sec = int(v_DnCnt_2.get())
		if (0 == sec) :
			self.queue = queue.Queue()
			ThreadedTask(self.queue).start()
			self.master.after(100, self.process_queue)
			v_DnCnt_2.set(str(59))
		else:
			sec=sec-1
			v_DnCnt_2.set(str(sec))
		
		self.master.after(1000, self.count_down)

	
class ThreadedTask(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
	def run(self):
		self.sniffUrl()
		self.queue.put("Task finished")
	def sniffUrl(self):
		url = t_url.get()
		urlLi = url.rsplit('/', 1)
		urlBase = urlLi[0] + "/"
		urlFile = urlLi[1]
		res = requests.get(urlBase+urlFile)
		
		targetStr = t_targetStr.get()
#		u'\u9650\u6642' #限時
		filterStr = t_filterStr.get()
#		u'\u8def\u9650'
#		u'\u5df2\u6436\u7562' #已搶
		
		soup = BeautifulSoup( res.text, "html.parser")
		
		for divTree in soup.findAll("div", id="center_8"):
			for article in divTree.select('a[href]'):
				if article.text.find(targetStr) != -1 & article.text.find(filterStr) == -1:
					print (article.text)
					print (urlBase+article['href'])
					webbrowser.open(urlBase+article['href'], new=0, autoraise=True)

def main():
	root = Tk()
	root.geometry("400x300+300+300")
	app = Application(root)
	root.mainloop()

if __name__ == '__main__':
	main()
