# -*- coding: latin-1 -*-
from PyQt4 import QtCore, QtGui
import urllib2
import re
import os
import xml.dom.minidom
#if (os.name == "nt"):
#	import codecs, win32com.client
from conpresencesrv import ConPresenceSrv
from ui_vboxup import Ui_VBoxUp

class Ui_VBoxMain(QtGui.QWidget):
	def __init__(self, parent, debug):
		self.debug = debug
		if (self.debug):
			print "init VBoxMain"
		self.parent = parent
		QtGui.QWidget.__init__(self)
		
		self.click = self.parent.click       
		
		self.list_contacts_ents_name = []
		self.list_contacts_ents_num = []
		self.list_outlook_contacts_num = []
		self.list_outlook_contacts_name = []
		self.list_outlook_contacts_shared_num = []
		self.list_outlook_contacts_shared_name = []
		self.listperso_num = []
		self.listperso_name = []
		self.HISTORY_names = []
		self.HISTORY_nums = []
		self.contacts_name = []
		self.contacts_num = []

		self.setupUi()
		if (self.click.PRESENCE==1):  
			self.con = ConPresenceSrv(self.click.UID, self.click.PWD, self.click.PRESENCESRV, self.click.PRESENCESRVPORT, self.click)
			self.connect(self.con, QtCore.SIGNAL("updateStatus"), self.changeItemTreeWidgetContacts)
			self.connect(self.con, QtCore.SIGNAL("updateStatusBar"), self.updateStatusBar)
			self.con.start()
		else:
			self.ui_vboxup.pushbutton_transfer.hide()
			self.ui_vboxup.pushbutton_holdon.hide()
			self.con = None
		
	
	def load_directoryperso(self):
		if (self.debug):
			print "load directory perso"
		try:
			fh = open(self.parent.ui_mainwindow.confdir+'/clickdial_directory.txt', 'r')
		except:
			return False
		for line in fh.readlines():
			ligne = line.split('\n')
			words = ligne[0].split('|')
			self.listperso_name.append(words[0])
			self.listperso_num.append(words[1])
			QtGui.QTreeWidgetItem(self.treeList_directoryperso, [words[0], words[1]])
		fh.close()
		
	def load_directory_ents(self):
		if (self.debug):
			print "load directory ents"
		#url = self.click.XMLSRV
		url = 'http://'+self.click.HOST+':8080/ccmcip/xmldirectorylist.jsp'
		#setdefaulttimeout(5)
		try:
			req = urllib2.Request(url)
			r = urllib2.urlopen(req)
		except:
			return False
		resp = r.read()
		self.list_contacts_ents_name = []
		self.list_contacts_ents_num = []
		doc = xml.dom.minidom.parseString(resp)
		for node in doc.getElementsByTagName('DirectoryEntry'):  # visit every node <bar />
			elts = xml.dom.minidom.parseString(node.toxml().encode('utf-8'))
			for node2 in elts.getElementsByTagName('Name'):
				if (node2.firstChild != None): 
					regex = re.compile("^\s*(.+)\s*$")
					r = regex.match(node2.childNodes[0].data)
					if (r):
						name = r.group(1)	   
			for node2 in elts.getElementsByTagName('Telephone'):
				if (node2.firstChild != None): 
					regex = re.compile("^\s*(.+)\s*$")
					r = regex.match(node2.childNodes[0].data)
					if (r):
						num = r.group(1)
						regex = re.compile("\d(\d+)")
						r = regex.match(num)
						if (r):
							if (r.group(1) != ''):				
								self.list_contacts_ents_num.append(r.group(1))
								self.list_contacts_ents_name.append(name)
								QtGui.QTreeWidgetItem(self.treeList_directoryents, [name, num])
		return True

#	def itemsOutlook(self, contacts):
#		items = contacts.Items
#		item = items.GetFirst ()
#		while item:
#			yield item
#			item = items.GetNext () 
#
#	def load_directoryoutlook(self):
#		if (self.debug):
#			print "Loading Outlook Contacts"
#		constants = win32com.client.constants
#		#FIELDS = ['FullName', 'BusinessTelephoneNumber', 'Email1Address']
#		DecodeUnicodeString = lambda x: codecs.latin_1_encode(x)[0]
#		try:
#			o = win32com.client.Dispatch("Outlook.Application")
#		except:
#			self.treeList_directoryoutlook.hide()
#			return False
#		mapi = o.GetNamespace("MAPI")
#		outlook = win32com.client.gencache.EnsureDispatch ("Outlook.Application")
#		ns = outlook.GetNamespace ("MAPI")
#		for contact in self.itemsOutlook (ns.GetDefaultFolder (constants.olFolderContacts)):
#			if contact.Class == constants.olContact:
#				regex = re.compile("\(*(\d\d)\)*\s*(\d\d)\s*(\d\d)\s*(\d\d)\s*(\d\d)\s*")
#				r = regex.match(str(contact.BusinessTelephoneNumber))
#				if (r):
#					businessphonenumber = r.group(1)+r.group(2)+r.group(3)+r.group(4)+r.group(5)
#					print contact.FullName+"  "+businessphonenumber
#					self.list_outlook_contacts_name.append (contact.FullName)
#					self.list_outlook_contacts_num.append(businessphonenumber)
#				r = regex.match(str(contact.MobileTelephoneNumber))
#				if (r):
#					mobilephonenumber = r.group(1)+r.group(2)+r.group(3)+r.group(4)+r.group(5)
#					print contact.FullName+"  "+mobilephonenumber
#					self.list_outlook_contacts_name.append (contact.FullName+" (Mobile)")
#					self.list_outlook_contacts_num.append (mobilephonenumber)    
#		o = None
#		for i in range(len(self.list_outlook_contacts_name)):
#			item = QtGui.QTreeWidgetItem(self.treeList_directoryoutlook, [self.list_outlook_contacts_name[i], self.list_outlook_contacts_num[i]])
#		return True
#
#	def load_directoryoutlookSharedContacts(self, tree_list, mail):
#		list_outlook_name = []
#		list_outlook_num = []
#		if (self.debug):
#			print "Loading Outlook Contacts"
#		constants = win32com.client.constants
#		#FIELDS = ['FullName', 'BusinessTelephoneNumber', 'Email1Address']
#		DecodeUnicodeString = lambda x: codecs.latin_1_encode(x)[0]
#		try:
#			o = win32com.client.Dispatch("Outlook.Application")
#		except:
#			self.tree_list.hide()
#			return False
#		mapi = o.GetNamespace("MAPI")
#		outlook = win32com.client.gencache.EnsureDispatch ("Outlook.Application")
#		ns = outlook.GetNamespace ("MAPI")
#		rec = ns.CreateRecipient(mail)
#		for contact in self.itemsOutlook (ns.GetSharedDefaultFolder (rec, constants.olFolderContacts)): 
#			if contact.Class == constants.olContact:
#				regex = re.compile("\(*(\d\d)\)*\s*(\d\d)\s*(\d\d)\s*(\d\d)\s*(\d\d)\s*")
#				r = regex.match(str(contact.BusinessTelephoneNumber))
#				if (r):
#					businessphonenumber = r.group(1)+r.group(2)+r.group(3)+r.group(4)+r.group(5)
#					print contact.FullName+"  "+businessphonenumber
#					list_outlook_name.append (contact.FullName)
#					list_outlook_num.append(businessphonenumber)
#				r = regex.match(str(contact.MobileTelephoneNumber))
#				if (r):
#					mobilephonenumber = r.group(1)+r.group(2)+r.group(3)+r.group(4)+r.group(5)
#					print contact.FullName+"  "+mobilephonenumber
#					list_outlook_name.append (contact.FullName+" (Mobile)")
#					list_outlook_num.append (mobilephonenumber)    
#		o = None
#		for i in range(len(list_outlook_name)):
#			print list_outlook_name[i]
#			print list_outlook_num[i]
#			item = QtGui.QTreeWidgetItem(tree_list, [list_outlook_name[i], list_outlook_num[i]])
#		self.list_outlook_contacts_shared_num.append(list_outlook_num)
#		self.list_outlook_contacts_shared_name.append(list_outlook_name)
#		return True

	def load_history(self):
		if (self.debug):
			print "load history"
		try:
			fh = open(self.parent.ui_mainwindow.confdir+'/clickdial.his', 'r')
		except:
			return False
		for line in fh.readlines():
			ligne = line.split('\n')
			words = ligne[0].split(';')
			if (len(words[0])>5):
				regex = re.compile("(\d)(\d+)")
				r = regex.match(words[0])
				if (r):
					num = str(r.group(2))
					self.HISTORY_nums.append(num)
			else:
				num = str(words[0])
				self.HISTORY_nums.append(num)
			found = 0
			
			it = QtGui.QTreeWidgetItemIterator(self.treeList_directoryperso)
			while (it.value() is not None and found==0):
				if (it.value().text(1) == num):
					name = it.value().text(0)
					found = 1
				it += 1
			it = QtGui.QTreeWidgetItemIterator(self.treeList_directoryents)
			while (it.value() is not None and found==0):
				if (it.value().text(1) == num):
					name = it.value().text(0)
					found = 1
				it += 1
			for i in range(len(self.contacts_num)):
				if (self.contacts_num[i] == num):
					name = self.contacts_name[i]
					found = 1
			
			if (found == 1):
				self.HISTORY_names.append(name)
				item = QtGui.QTreeWidgetItem([name, words[1]])    
			else:
				self.HISTORY_names.append("")        
				item = QtGui.QTreeWidgetItem([num, words[1]])
			item.setSizeHint(0, QtCore.QSize(20, 10))
			self.treeList_history.insertTopLevelItem(0, item)
		fh.close()
		
	def load_contacts(self):
		if (self.debug):
			print "load_contacts"
		try:
			fh = open(self.parent.ui_mainwindow.confdir+'/clickdial_contacts.txt', 'r')
		except:
			return False
		for line in fh.readlines():
			ligne = line.split('\n')
			words = ligne[0].split('/')
			item = QtGui.QTreeWidgetItem(self.treeList_contacts, [words[0]])
			item.setTextAlignment(1, QtCore.Qt.AlignLeft)
			item.setIcon(0, QtGui.QIcon('pixmaps/status-offline.png'))
			self.contacts_name.append(words[0])
			self.contacts_num.append(words[1])
		fh.close()

	def displayDirectoryEnts(self):
		for i in range(self.qtab.count()):
			self.qtab.removeTab(i)	
		alltab = 0

		#for i in range(len(self.list_contacts_ents_name)-1):
			#QtGui.QTreeWidgetItem(self.treeList_directoryents, [self.list_contacts_ents_name[i], self.list_contacts_ents_num[i]])
		#if (self.click.XML == 1):
		if len(self.list_contacts_ents_name) > 0:
			self.qtab.addTab(self.treeList_directoryents, "Entreprise")
			self.tabXML = alltab
			alltab += 1
			#self.nbTabs = self.nbTabs + 2
		if len(self.listperso_name) > -1:
			self.qtab.addTab(self.treeList_directoryperso, "Personnel")
			self.tabPerso = alltab
			alltab += 1
			#self.nbTabs = self.nbTabs + 1
#		if (os.name == "nt" and self.click.OUTLOOK == 1):
#			if (self.click.OUTLOOK_CONTACTS == 1):
#				self.load_directoryoutlook()
#				self.qtab.addTab(self.treeList_directoryoutlook, "Outlook")
#				self.tabOUTLOOK = alltab
#				alltab += 1
#			for i in range(len(self.click.OUTLOOK_CONTACTS_SHARED)):
#				regex = re.compile("(.+)@.+")
#				r = regex.match(self.click.OUTLOOK_CONTACTS_SHARED[i])
#				if (r):
#					nom = str(r.group(1))
#				else:
#					nom = self.click.OUTLOOK_CONTACTS_SHARED[i]
#				self.load_directoryoutlookSharedContacts(self.treeList_directoryoutlookcontactsshared[i], self.click.OUTLOOK_CONTACTS_SHARED[i])
#				self.qtab.addTab(self.treeList_directoryoutlookcontactsshared[i], "Outlook "+nom)
#				alltab += 1
#				#self.nbTabs = self.nbTabs+1
		self.qtab.show()
	
	def setupUi(self):
		if (self.debug):
			print "setupUi"
		self.setObjectName("ClickDial")
		self.vbox_main = QtGui.QVBoxLayout()       
		self.setLayout(self.vbox_main)
		
		self.ui_vboxup = Ui_VBoxUp(self, self.click)
		self.vbox_main.addWidget(self.ui_vboxup, 0)
		#self.nbTabs = 0
		#Â List Tree Perso
		self.treeList_directoryperso = QtGui.QTreeWidget()
		self.treeList_directoryperso.setObjectName("treeList_directoryperso")
		self.treeList_directoryperso.setColumnCount(2)
		self.treeList_directoryperso.setHeaderLabels(["Nom", "Numero"])
		self.treeList_directoryperso.connect(self.treeList_directoryperso, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.itemSelectionChangedTreeListDirPerso)
		#self.treeList_directoryperso.connect(self.treeList_directoryperso, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.itemSelectionChangedTreeList)
		self.treeList_directoryperso.connect(self.treeList_directoryperso, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.itemDoubleClickedTreeListDirPerso)
		self.treeList_directoryperso.viewport().installEventFilter(self)
		self.treeList_directoryperso.setColumnWidth(0, 170)
		
		 #Â List Tree Ents
		self.treeList_directoryents = QtGui.QTreeWidget()
		self.treeList_directoryents.setObjectName("treeList_directoryents")
		self.treeList_directoryents.setColumnCount(2)
		self.treeList_directoryents.setHeaderLabels(["Nom", "Numero"])
		self.treeList_directoryents.connect(self.treeList_directoryents, QtCore.SIGNAL("itemSelectionChanged()"), self.itemSelectionChangedTreeListDirEnts)
		self.treeList_directoryents.connect(self.treeList_directoryents, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.itemSelectionChangedTreeListDirEnts)
		self.treeList_directoryents.viewport().installEventFilter(self)
		self.treeList_directoryents.setColumnWidth(0, 160)
		
		if (os.name == "nt" and self.click.OUTLOOK == 1):
			#Â List Tree Ents
			if (self.click.OUTLOOK_CONTACTS == 1):
				self.treeList_directoryoutlook = QtGui.QTreeWidget()
				self.treeList_directoryoutlook.setObjectName("treeList_directoryoutlook")
				self.treeList_directoryoutlook.setColumnCount(2)
				self.treeList_directoryoutlook.setHeaderLabels(["Nom", "Numero"])
				self.treeList_directoryoutlook.connect(self.treeList_directoryoutlook, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.itemSelectionChangedTreeList)
				self.treeList_directoryoutlook.viewport().installEventFilter(self)
				self.treeList_directoryoutlook.setColumnWidth(0, 160)

			self.treeList_directoryoutlookcontactsshared = []
			for i in range(len(self.click.OUTLOOK_CONTACTS_SHARED)):
				treeList_directoryoutlookcontactsshared = QtGui.QTreeWidget()
				treeList_directoryoutlookcontactsshared.setObjectName("treeList_directoryoutlookcontactsshared")
				treeList_directoryoutlookcontactsshared.setColumnCount(2)
				treeList_directoryoutlookcontactsshared.setHeaderLabels(["Nom", "Numero"])
				self.treeList_directoryoutlook.connect(treeList_directoryoutlookcontactsshared, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.itemSelectionChangedTreeList)
				treeList_directoryoutlookcontactsshared.viewport().installEventFilter(self)
				treeList_directoryoutlookcontactsshared.setColumnWidth(0, 160)
				self.treeList_directoryoutlookcontactsshared.append(treeList_directoryoutlookcontactsshared)
			
			#self.load_directoryoutlook()
		
		#Â QTab contenant les 2 list tree
		self.qtab = QtGui.QTabWidget()
		
		#Â List Tree Contacts
		self.treeList_contacts = QtGui.QTreeWidget()
		self.treeList_contacts.setObjectName("treeList_contacts")
		self.treeList_contacts.setColumnCount(1)
		self.treeList_contacts.setHeaderLabel("")
		self.treeList_contacts.connect(self.treeList_contacts, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.mousePressEventContacts)
		self.treeList_contacts.viewport().installEventFilter(self)
		if (self.click.PRESENCE==0):
			self.treeList_contacts.hide()
		#self.load_contacts()
			
		#Â Splitter contenant le Qtab et la list Tree Contacts
		self.splitterHorizontal = QtGui.QSplitter(QtCore.Qt.Horizontal)
		self.splitterHorizontal.addWidget(self.qtab)
		self.splitterHorizontal.addWidget(self.treeList_contacts)
		QtGui.QSplitter.moveSplitter(self.splitterHorizontal, 180, 1)

		self.treeList_history = QtGui.QTreeWidget()
		self.treeList_history.setObjectName("treeList_history")
		self.treeList_history.setColumnCount(2)
		self.treeList_history.setHeaderLabels(["Numero", "Date"])
		self.treeList_history.connect(self.treeList_history, QtCore.SIGNAL("itemSelectionChanged()"), self.itemSelectionChangedTreeListHistory)
		self.treeList_history.setColumnWidth(0, 250)
		#self.load_history()

		self.splitterVertical = QtGui.QSplitter(QtCore.Qt.Vertical)
		self.splitterVertical.addWidget(self.splitterHorizontal)
		self.splitterVertical.addWidget(self.treeList_history)
		QtGui.QSplitter.moveSplitter(self.splitterVertical, 300, 1)
		
		self.vbox_main.addWidget(self.splitterVertical, 1)
		#QtCore.QMetaObject.connectSlotsByName(self)
	
	def mousePressEventContacts(self, event):
		print "mousePressEvent"   
	
	def eventFilter(self, object, event):
		if (object.parent().objectName() == "treeList_contacts"):
			if(event.type() == QtCore.QEvent.MouseButtonPress):
				if event.button() == QtCore.Qt.RightButton:
					print "right"
					menu = QtGui.QMenu(self)
					callAction = menu.addAction("Appeler")
					callAction.triggered.connect(self.callActionContacts)
					transferAction = menu.addAction("Transferer")
					action = menu.exec_(self.treeList_contacts.mapToGlobal(event.pos())) 
					return True
		if (object.parent().objectName() == "treeList_directoryperso"):
			if(event.type() == QtCore.QEvent.MouseButtonPress):
				if event.button() == QtCore.Qt.RightButton:
					print "right"
					menu = QtGui.QMenu(self)
					callAction = menu.addAction("Appeler")
					callAction.triggered.connect(self.callActionDirPerso)
					addAction = menu.addAction("Ajouter")
					delAction = menu.addAction("Supprimer")
					action = menu.exec_(self.treeList_directoryperso.mapToGlobal(event.pos())) 
					return True
		if (object.parent().objectName() == "treeList_directoryents"):
			if(event.type() == QtCore.QEvent.MouseButtonPress):
				if event.button() == QtCore.Qt.RightButton:
					print "right"
					menu = QtGui.QMenu(self)
					callAction = menu.addAction("Appeler")
					callAction.triggered.connect(self.callActionDirEnts)
					action = menu.exec_(self.treeList_directoryents.mapToGlobal(event.pos())) 
					return True
		return False 
	
	def callActionContacts(self):  
		item = self.treeList_contacts.currentItem()
		print "callAction "+item.text(0)
		for i in range(len(self.contacts_name)):
			if (self.contacts_name[i] == item.text(0)):
				self.click.start_call(self.contacts_num[i], False)
		#self.click.start_call(item.text(1))
		
	def callActionDirPerso(self):  
		item = self.treeList_directoryperso.currentItem()
		print "callAction "+item.text(1)
		if (self.ui_vboxup.qcheckAnonymous.checkState() == 2):
			bool = True
		else:
			bool = False
		self.click.start_call(str(self.click.PREFIX)+item.text(1), bool)
	
	def callActionDirEnts(self):  
		item = self.treeList_directoryents.currentItem()
		print "callAction "+item.text(1)
		if (self.ui_vboxup.qcheckAnonymous.checkState() == 2):
			bool = True
		else:
			bool = False
		self.click.start_call(str(self.click.PREFIX)+item.text(1), bool)
	
	def changeItemTreeWidgetContacts(self, num, status):  
		#print "changeStatusContacts "+num+" "+status      
		regex = re.compile("(\d+)\s")
		r = regex.match(self.click.LINE)
		if (r):
			if (r.group(1) == num):  
				if (status == "0"):
					QtGui.QAbstractButton.setEnabled(self.ui_vboxup.pushbutton_call, True)
				if (status == "2" or status == "1"):
					QtGui.QAbstractButton.setEnabled(self.ui_vboxup.pushbutton_call, False)
		if (num == "*"):
			name = "*"
		else:
			for i in range(len(self.contacts_num)):
				if (self.contacts_num[i] == num):
					name = self.contacts_name[i]
					break
		#widgetitem1 = QtGui.QBoxLayout.itemAt(self.vbox_main, 1)
		#splitter1 = QtGui.QWidgetItem.widget(widgetitem1)
		#splitter2 = QtGui.QSplitter.widget(splitter1,0)
		#tree = QtGui.QSplitter.widget(splitter2,1)
		found = 0
		it = QtGui.QTreeWidgetItemIterator(self.treeList_contacts)
		while it.value() is not None:
			if ((status == "-1") and (name == it.value().text(0) or name == "*")):
				it.value().setIcon(0, QtGui.QIcon('pixmaps/status-offline.png'))
				found = 1
			if ((status == "0") and (name == it.value().text(0) or name == "*")):
				it.value().setIcon(0, QtGui.QIcon('pixmaps/status-online.png'))
				found = 1
			if ((status == "1") and (name == it.value().text(0) or name == "*")):
				it.value().setIcon(0, QtGui.QIcon('pixmaps/status-ringing.png'))
				found = 1
			if ((status == "2") and (name == it.value().text(0) or name == "*")):
				it.value().setIcon(0, QtGui.QIcon('pixmaps/status-inacall.png'))
				found = 1       
			it += 1
		if (found == 1):
			return True
		else:
			return False    

	def updateStatusBar(self, presenceStatus, webdialStatus):
		#print "updateStatusBar"
		if (webdialStatus == "0"):
			QtGui.QAbstractButton.setEnabled(self.ui_vboxup.pushbutton_call, False)
			if (presenceStatus == "0"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : Hors Ligne                                  WebDial : Hors Ligne")
			if (presenceStatus == "1"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : En Ligne                                  WebDial : Hors Ligne")
			if (presenceStatus == "-1"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : Echec d'identification                      WebDial : Hors Ligne")
			if (presenceStatus == "-2"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : Echec de connexion                          WebDial : Hors Ligne")
			if (presenceStatus == "-3"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : En cours de connexion                       WebDial : Hors Ligne")
		if (webdialStatus == "1"):
			QtGui.QAbstractButton.setEnabled(self.ui_vboxup.pushbutton_call, True)
			if (presenceStatus == "0"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : Hors Ligne                                  WebDial : En Ligne")
			if (presenceStatus == "1"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : En Ligne                                    WebDial : En Ligne")
			if (presenceStatus == "-1"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : Echec d'identification                      WebDial : En Ligne")
			if (presenceStatus == "-2"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : Echec de connexion                          WebDial : En Ligne")
			if (presenceStatus == "-3"):
				self.parent.ui_mainwindow.updateStatusBar("Presence : En cours de connexion                       WebDial : En Ligne")

	def itemSelectionChangedTreeListDirPerso(self):
		item = self.treeList_directoryperso.currentItem()
		self.ui_vboxup.lineEditPrefix.setText(str(self.click.PREFIX))
		self.ui_vboxup.lineEdit.setText(item.text(1))
	
	def itemDoubleClickedTreeListDirPerso(self):
		print "DoubleClicked"
		item = self.treeList_directoryperso.currentItem()
		self.click.start_call(item.text(1))
		
	def itemSelectionChangedTreeListDirEnts(self):
		item = self.treeList_directoryents.currentItem()
		self.ui_vboxup.lineEdit.setText(item.text(1))
		self.ui_vboxup.lineEditPrefix.setText("")
   
	def itemSelectionChangedTreeListHistory(self):        
		item = self.treeList_history.currentItem()
		num = item.text(0)
		for i in range(len(self.HISTORY_names)):
			if (self.HISTORY_names[i] == item.text(0)):
				num = self.HISTORY_nums[i]
				found = 1
				break
		#self.ui_vboxup.lineEditPrefix.setText("")
		self.ui_vboxup.lineEdit.setText(num)   

	def itemSelectionChangedTreeList(self, item):
		self.ui_vboxup.lineEdit.setText(item.text(1))
