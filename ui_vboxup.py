# -*- coding: latin-1 -*-
from PyQt4 import QtCore, QtGui
import re
from datetime import datetime

class Ui_VBoxUp(QtGui.QWidget):
	def __init__(self, ui_vboxmain, click):
		self.click = click
		self.tabSearch = 0
		self.ui_vboxmain = ui_vboxmain
		QtGui.QWidget.__init__(self)
		#self.setMaximumWidth(100)
		layout_main = QtGui.QVBoxLayout(self)
		
		# Buttons Layout
		widget_buttons = QtGui.QWidget()  
		layout = QtGui.QGridLayout()   
		widget_buttons.setLayout(layout)   
		#self.qcheckAnonymous = QtGui.QCheckBox("Anonyme")
		#layout.addWidget(self.qcheckAnonymous, 0, 0)
		
		self.lineEditPrefix = QtGui.QLineEdit(self)
		self.lineEditPrefix.setMaxLength(1)
		self.lineEditPrefix.setMaximumWidth(20)
		self.lineEditPrefix.setText(str(self.ui_vboxmain.click.PREFIX))
		layout.addWidget(self.lineEditPrefix, 0, 1)
		
		self.lineEdit = QtGui.QLineEdit(self)
		self.lineEdit.setMaximumWidth(150)
		layout.addWidget(self.lineEdit, 0, 2)
		QtCore.QObject.connect (self.lineEdit, QtCore.SIGNAL ('returnPressed()'), self.event_clicked_pickup)
		#void returnPressed ()
		self.pushbutton_call = QtGui.QPushButton(self)
		self.pushbutton_call.setIcon(QtGui.QIcon(self.ui_vboxmain.parent.ui_mainwindow.confdir+'/pixmaps/phone-pick-up.png'))
		self.pushbutton_call.resize(36, 36)
		QtCore.QObject.connect (self.pushbutton_call, QtCore.SIGNAL ('clicked()'), self.event_clicked_pickup)
		if (self.click.CONNECTED == 1):
			QtGui.QAbstractButton.setEnabled(self.pushbutton_call, True)
		else: 
			QtGui.QAbstractButton.setEnabled(self.pushbutton_call, False)
		layout.addWidget(self.pushbutton_call, 0, 3)
		
		self.pushbutton_hang = QtGui.QPushButton(self)
		self.pushbutton_hang.setIcon(QtGui.QIcon(self.ui_vboxmain.parent.ui_mainwindow.confdir+'/pixmaps/phone-hang-up.png'))
		self.pushbutton_hang.resize(36, 36)
		QtCore.QObject.connect (self.pushbutton_hang, QtCore.SIGNAL ('clicked()'), self.event_clicked_hangup)
		layout.addWidget(self.pushbutton_hang, 0, 4)
		
		self.pushbutton_transfer = QtGui.QPushButton(self)
		self.pushbutton_transfer.setIcon(QtGui.QIcon(self.ui_vboxmain.parent.ui_mainwindow.confdir+'/pixmaps/call-transfer.png'))
		self.pushbutton_transfer.resize(36, 36)
		QtCore.QObject.connect (self.pushbutton_transfer, QtCore.SIGNAL ('clicked()'), self.event_clicked_transfer)
		layout.addWidget(self.pushbutton_transfer, 0, 5)
		
		self.pushbutton_holdon = QtGui.QPushButton(self)
		self.pushbutton_holdon.setIcon(QtGui.QIcon(self.ui_vboxmain.parent.ui_mainwindow.confdir+'/pixmaps/pause.png'))
		self.pushbutton_holdon.resize(36, 36)
		QtCore.QObject.connect (self.pushbutton_holdon, QtCore.SIGNAL ('clicked()'), self.event_clicked_holdon)
		layout.addWidget(self.pushbutton_holdon, 0, 6)

		self.pushbutton_call_anonymous = QtGui.QPushButton(self)
		self.pushbutton_call_anonymous.setIcon(QtGui.QIcon(self.ui_vboxmain.parent.ui_mainwindow.confdir+'/pixmaps/call-anonymous.png'))
		self.pushbutton_call_anonymous.resize(36, 36)
		self.pushbutton_call_anonymous.setToolTip('Appelle en numero cache')
		QtCore.QObject.connect (self.pushbutton_call_anonymous, QtCore.SIGNAL ('clicked()'), self.event_clicked_pickup_anonymous)
		if (self.click.CONNECTED == 1):
			QtGui.QAbstractButton.setEnabled(self.pushbutton_call_anonymous, True)
		else: 
			QtGui.QAbstractButton.setEnabled(self.pushbutton_call_anonymous, False)
		layout.addWidget(self.pushbutton_call_anonymous, 0, 7)

		layout_main.addWidget(widget_buttons)
		
		# Search Layout
		widget_search = QtGui.QWidget()
		layout_search = QtGui.QGridLayout() 
		widget_search.setLayout(layout_search)
		layout_search.addWidget(QtGui.QLabel("Recherche"), 0, 1)
		self.searchLineEdit = QtGui.QLineEdit(self)
		self.searchLineEdit.setMaximumWidth(250)
		QtCore.QObject.connect (self.searchLineEdit, QtCore.SIGNAL ('returnPressed()'), self.event_search)
		QtCore.QObject.connect (self.searchLineEdit, QtCore.SIGNAL ('textEdited (const QString&)'), self.event_search)
		layout_search.addWidget(self.searchLineEdit, 0, 2)
		self.pushbutton_search = QtGui.QPushButton(self)
		self.pushbutton_search.setIcon(QtGui.QIcon(self.ui_vboxmain.parent.ui_mainwindow.confdir+'/pixmaps/search.png'))
		layout_search.addWidget(self.pushbutton_search, 0, 3)
		QtCore.QObject.connect (self.pushbutton_search, QtCore.SIGNAL ('clicked()'), self.event_search)
		self.pushbutton_deletesearch = QtGui.QPushButton(self)
		self.pushbutton_deletesearch.setIcon(QtGui.QIcon(self.ui_vboxmain.parent.ui_mainwindow.confdir+'/pixmaps/delete.png'))
		layout_search.addWidget(self.pushbutton_deletesearch, 0, 4)
		QtCore.QObject.connect (self.pushbutton_deletesearch, QtCore.SIGNAL ('clicked()'), self.event_delete_search)
		layout_main.addStretch(0)
		layout_main.addWidget(widget_search)

	def search(self, string):
		#if (self.ui_vboxmain.list_contacts_ents_name != None):
		self.searchList(self.ui_vboxmain.list_contacts_ents_name, self.ui_vboxmain.list_contacts_ents_num, string)
		#if (self.ui_vboxmain.listperso_name != None):
		self.searchList(self.ui_vboxmain.listperso_name, self.ui_vboxmain.listperso_num, string)
		self.searchList(self.ui_vboxmain.list_outlook_contacts_name, self.ui_vboxmain.list_outlook_contacts_num, string)
		for i in range(len(self.ui_vboxmain.list_outlook_contacts_shared_num)):
			self.searchList(self.ui_vboxmain.list_outlook_contacts_shared_name[i], self.ui_vboxmain.list_outlook_contacts_shared_num[i], string)
		
	def searchList(self, array_name, array_num, string):
		for i in range(len(array_name)):
			regex = re.compile("(.*"+string+".*)", re.IGNORECASE)
			r = regex.match(array_name[i])
			if (r):
				QtGui.QTreeWidgetItem(self.treeList_search, [array_name[i], array_num[i]])
		
	def event_search(self):
		if len(str(self.searchLineEdit.text())) > 0:
			if (self.tabSearch == 0):
				self.treeList_search = QtGui.QTreeWidget()
				self.ui_vboxmain.qtab.insertTab(0, self.treeList_search,QtGui.QIcon(self.ui_vboxmain.parent.ui_mainwindow.confdir+'/pixmaps/search.png'), "")
				self.treeList_search.setObjectName("treeList_search")
				self.treeList_search.setColumnCount(2)
				self.treeList_search.setHeaderLabels(["Nom", "Numero"])
				self.treeList_search.setColumnWidth(0, 160)
				self.treeList_search.connect(self.treeList_search, QtCore.SIGNAL("itemSelectionChanged()"), self.itemSelectionChangedTreeListSearch)	
				self.tabSearch = 1
			self.ui_vboxmain.qtab.setCurrentIndex(0)
			self.treeList_search.clear()
			self.search(str(self.searchLineEdit.text()))
		else:
			if (self.tabSearch == 1):
				self.ui_vboxmain.qtab.removeTab(0)
				self.tabSearch = 0

	def event_delete_search(self):
		if (self.tabSearch == 1):
			self.ui_vboxmain.qtab.removeTab(0)
			self.tabSearch = 0

	def itemSelectionChangedTreeListSearch(self):
		item = self.treeList_search.currentItem()
		regex = re.compile("(\d)(\d+)")
		r = regex.match(item.text(1))
		if (r):
			self.lineEditPrefix.setText(r.group(1))
			self.lineEdit.setText(r.group(2))

	def event_clicked_pickup(self):
		dn = self.lineEditPrefix.text() + self.lineEdit.text()
		#if (self.qcheckAnonymous.checkState() == 2):
		#	bool = True
		#else:
		#	bool = False
		self.click._makeCall(dn, False)
		self.add_history(dn)
		
	def event_clicked_pickup_anonymous(self):
		dn = self.lineEditPrefix.text() + self.lineEdit.text()
		#if (self.qcheckAnonymous.checkState() == 2):
		#	bool = True
		#else:
		#	bool = False
		self.click._makeCall(dn, True)
		self.add_history(dn)	
			
	def add_history(self, dn):
		now = datetime.now().strftime("%d/%m/%y %H:%M:%S")
		self.ui_vboxmain.HISTORY_nums.append(dn)
		found = 0	
		it = QtGui.QTreeWidgetItemIterator(self.ui_vboxmain.treeList_directoryperso)
		while (it.value() is not None and found==0):
			if (it.value().text(1) == dn):
				name = it.value().text(0)
				found = 1
			it += 1
		it = QtGui.QTreeWidgetItemIterator(self.ui_vboxmain.treeList_directoryents)
		while (it.value() is not None and found==0):
			if (it.value().text(1) == dn):
				name = it.value().text(0)
				found = 1
			it += 1
		for i in range(len(self.ui_vboxmain.contacts_num)):
			if (self.ui_vboxmain.contacts_num[i] == dn):
				name = self.ui_vboxmain.contacts_name[i]
				found = 1
			
		if (found == 1):
			self.ui_vboxmain.HISTORY_names.append(name)
			item = QtGui.QTreeWidgetItem([name, now])    
		else:
			self.ui_vboxmain.HISTORY_names.append("")        
			item = QtGui.QTreeWidgetItem([dn, now])
		item.setSizeHint(0, QtCore.QSize(20, 10))
		self.ui_vboxmain.treeList_history.insertTopLevelItem(0, item)

		f = open(self.ui_vboxmain.parent.ui_mainwindow.confdir+'/clickdial.his', 'a')
		f.write(dn + ';' + now + '\n')
		f.close()
   
	def event_clicked_hangup(self):    
		self.click._stopCall()
		
	def event_clicked_transfer(self):
		print "transfer"
		dn = self.lineEditPrefix.text() + self.lineEdit.text()
		self.ui_vboxmain.con.transfer("Guillaume", "4195", dn)
		
	def event_clicked_holdon(self):
		print "hold-on"
