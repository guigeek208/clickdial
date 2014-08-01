import sys
from PyQt4 import QtCore, QtGui
import urllib2, urllib, cookielib
import time
import re
import os
import xml.dom.minidom
from xml.dom.minidom import Document
from datetime import datetime, date
from socket import *

class ConPresenceSrv (QtCore.QThread):
	def __init__(self, login, pwd, serverHost, serverPort, click):
		QtCore.QThread.__init__(self)
		self.connected = 0 # Hors connexion
		self.Terminated = False
		self.login = login
		self.pwd = pwd
		self.serverHost = serverHost
		self.serverPort = serverPort
		self.click = click      
		#click.liststore_contacts.append(["test", "", True])
	
	def transfer (self, name, line, dn):
		self.socket.send("<sender>" + name + "</sender><line>" + line + "</line><action>transfer</action><to>" + dn + "</to>\n")
		
	def run (self):
		print 'Start Threading'
		self.connected = 1 # En cours de connexion
		if (self.click.CONNECTED == 1):
			self.emit(QtCore.SIGNAL('updateStatusBar'), "-3", "1")
		if (self.click.CONNECTED == 0):
			self.emit(QtCore.SIGNAL('updateStatusBar'), "-3", "0")
		try:
			self.socket = socket(AF_INET, SOCK_STREAM)
			self.socket.setsockopt(SOL_TCP, SO_KEEPALIVE, True)
			self.socket.connect((self.serverHost, self.serverPort))
		except: 
			if self.socket: 
				self.socket.close() 
				print "Could not open socket"
				if (self.click.CONNECTED == 1):
					self.emit(QtCore.SIGNAL('updateStatusBar'), "-2", "1")
				if (self.click.CONNECTED == 0):
					self.emit(QtCore.SIGNAL('updateStatusBar'), "-2", "0")
				return
		if (self.logIn(self.login, self.pwd) == False):
			return
		self.socket.settimeout(None)
		print self.socket.gettimeout()
		data = self.socket.recv(1024)
		print data
		while not self.Terminated:
			data = self.socket.recv(1024)
			arr = data.split('\n')
			for i in range(len(arr)):
				regex = re.compile("<sender>(\w+)</sender><line>(\d+)</line><status>(\d)</status>")
				r = regex.match(arr[i])
				#print arr[i]
				if (r):
					self.emit(QtCore.SIGNAL('updateStatus'), r.group(2), r.group(3))
		self.socket.close()             

	def stop(self):
		print "stop"
		self.Terminated = True

	def logIn(self, login, pwd):
		data = self.socket.recv(1024)
		print (data)
		self.socket.send("USER " + login + "\n")
		self.socket.send("PASS " + pwd + "\n")
		data = self.socket.recv(1024)
		print data
		if (data == "LOGIN OK\n"):
			print "Connected"
			self.connected = 2  
			print self.click.CONNECTED
			self.emit(QtCore.SIGNAL('updateStatus'), "*", "0")
			if (self.click.CONNECTED == 1):
				self.emit(QtCore.SIGNAL('updateStatusBar'), "1", "1")
			if (self.click.CONNECTED == 0):
				self.emit(QtCore.SIGNAL('updateStatusBar'), "1", "0")
			return True
		else :
			print "Not Connected"
			self.emit(QtCore.SIGNAL('updateStatus'), "*", "-1")
			if (self.click.CONNECTED == 1):
				self.emit(QtCore.SIGNAL('updateStatusBar'), "-1", "1")
			if (self.click.CONNECTED == 0):
				self.emit(QtCore.SIGNAL('updateStatusBar'), "-1", "0")                
			return False
