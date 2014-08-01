# -*- coding: latin-1 -*-
from PyQt4 import QtCore, QtGui
from threadprogressbar import ThreadProgressBar
from ui_vboxmain import Ui_VBoxMain
from class_clickdial import ClickDial

class Ui_VBoxLogIn(QtGui.QWidget):
	def __init__(self, ui_mainwindow, debug):
		super(Ui_VBoxLogIn, self).__init__()
		self.thread = ThreadProgressBar()
		self.thread.partDone.connect(ui_mainwindow.updatePBar)
		self.thread.procDone.connect(ui_mainwindow.finishLoad)
		self.debug = debug
		if (self.debug):
			print "init VBoxLogin"
		self.ui_mainwindow = ui_mainwindow
		#QtGui.QWidget.__init__(self)
		self.click = ClickDial(self, self.debug)
		self.setupUi()

	def setupUi(self):
		layout = QtGui.QVBoxLayout()
		self.setLayout(layout)
		widget1 = QtGui.QWidget()     
		widget1.setFixedSize(450,100)
		layout1 = QtGui.QVBoxLayout()
		widget1.setLayout(layout1)
		self.logo = QtGui.QLabel()
		self.logo.setPixmap(QtGui.QPixmap(self.ui_mainwindow.confdir+'/pixmaps/logo_clickdial.png'))
		#self.logo.setGeometry(400, 80, 80, 30)
		layout1.addWidget(self.logo)
		self.line = 0
		
		widget2 = QtGui.QWidget()
		self.layout2 = QtGui.QGridLayout()
		widget2.setLayout(self.layout2)
		widget2.setFixedSize(450,300)

		self.labelLogin = QtGui.QLabel("Nom d'utilisateur")
		self.lineEditLogin = QtGui.QLineEdit(self)
		self.lineEditLogin.setMaxLength(150)
		self.lineEditLogin.setMaximumWidth(150)
		if (self.click.UID!=None):
			self.lineEditLogin.setText(self.click.UID)
		self.layout2.addWidget(self.labelLogin, self.line, 0)
		self.layout2.addWidget(self.lineEditLogin, self.line, 1)
		self.line+=1
		
		self.labelPwd = QtGui.QLabel("Mot de passe")
		self.lineEditPwd = QtGui.QLineEdit(self)
		self.lineEditPwd.setMaxLength(150)
		self.lineEditPwd.setMaximumWidth(150)
		self.lineEditPwd.setEchoMode(QtGui.QLineEdit.Password)
		if (self.click.PWD!=None):
			self.lineEditPwd.setText(self.click.PWD)
		self.layout2.addWidget(self.labelPwd, self.line, 0)
		self.layout2.addWidget(self.lineEditPwd, self.line, 1)
		self.line+=1      
		
		self.labelAddrIp = QtGui.QLabel("Adresse IP du CUCM")
		self.lineEditAddrIp = QtGui.QLineEdit(self)
		self.lineEditAddrIp.setMaxLength(150)
		self.lineEditAddrIp.setMaximumWidth(150)
		if (self.click.HOST != None):
			self.lineEditAddrIp.setText(self.click.HOST)
		QtCore.QObject.connect (self.lineEditAddrIp, QtCore.SIGNAL ('editingFinished ()'), self.event_connect)
		self.layout2.addWidget(self.labelAddrIp, self.line, 0)
		self.layout2.addWidget(self.lineEditAddrIp, self.line, 1)
		self.line+=1
						
		self.qcombo_line = QtGui.QComboBox()
		if (self.click.LINE != None):
			self.qcombo_line.addItem(self.click.LINE)
		QtCore.QObject.connect (self.qcombo_line, QtCore.SIGNAL ('activated (int)'), self.event_qcombo_line_changed)
		self.layout2.addWidget(QtGui.QLabel("Ligne"), self.line, 0)
		self.layout2.addWidget(self.qcombo_line, self.line, 1)
		self.line+=1
	
		self.qcombo_periph = QtGui.QComboBox()
		if (self.click.DEVICE != None):
			self.qcombo_periph.addItem(self.click.DEVICE)	
		self.layout2.addWidget(QtGui.QLabel("Device"), self.line, 0)
		self.layout2.addWidget(self.qcombo_periph, self.line, 1)
		self.line+=1
		
#        self.labelRememberPwd = QtGui.QLabel("Memoriser le mot de passe")
#        self.checkRememberPwd = QtGui.QCheckBox()
#        self.layout2.addWidget(self.labelRememberPwd, self.line, 0)
#        self.layout2.addWidget(self.checkRememberPwd, self.line, 1)
#        self.line+=1
	
	
		self.qbuttonConnect = QtGui.QPushButton("Se Connecter")
		QtCore.QObject.connect (self.qbuttonConnect, QtCore.SIGNAL ('clicked()'), self.event_clicked_connect)
		self.layout2.addWidget(self.qbuttonConnect, self.line, 1)

		widget3 = QtGui.QWidget()     
		widget3.setFixedSize(450,200)

		layout.addWidget(widget1)
		layout.addWidget(widget2)
		layout.addWidget(widget3)
	
	def event_qcombo_line_changed(self):
		if (self.qcombo_line.currentText() == "Mobilite"):
			#print "test "
			self.qcombo_periph.addItem("Mobilite")
			self.qcombo_periph.setCurrentIndex(self.qcombo_periph.count()-1)
			self.qcombo_periph.setEnabled(False)
	
	def event_connect(self):
		self.click.UID = str(self.lineEditLogin.text())
		self.click.PWD = str(self.lineEditPwd.text())
		self.click.URL = str(self.lineEditAddrIp.text())
		if (self.click.log_in()):
			self.qcombo_periph.clear()
			self.qcombo_periph.addItem("Choisir")
			self.qcombo_line.clear()
			self.qcombo_line.addItem("Choisir")
			self.qcombo_line.setEnabled(True)
			self.qcombo_periph.setEnabled(True)
			for i in range(len(self.click.DEVICES)):
				self.qcombo_periph.addItem(self.click.DEVICES[i])
			for i in range(len(self.click.LINES)):
				self.qcombo_line.addItem(self.click.LINES[i])
			self.qcombo_line.addItem("Mobilite")

	def event_clicked_connect(self):
		self.click.UID = str(self.lineEditLogin.text())
		self.click.PWD = str(self.lineEditPwd.text())
		self.click.URL = str(self.lineEditAddrIp.text())
		if str(self.qcombo_line.currentText()) == "Mobilite":
			self.click.DEVICE = None
		else:
			self.click.DEVICE = str(self.qcombo_periph.currentText())
		if (self.click.CONNECTED == 0 or  self.click.CONNECTED == None):
			if (self.click.log_in()):   
				self.loading()
			else:
				label = QtGui.QLabel("")
				label.setPixmap(QtGui.QPixmap(self.ui_mainwindow.confdir+'/pixmaps/error.png'))
				self.layout2.addWidget(label, 1, 2)
				return
		else:
			self.loading()
	 
	def loading(self):
		self.widget_waiting = QtGui.QWidget()
		layout = QtGui.QVBoxLayout()
		self.widget_waiting.setLayout(layout)
		widget1 = QtGui.QWidget()     
		widget1.setFixedSize(450,100)
		layout1 = QtGui.QVBoxLayout()
		widget1.setLayout(layout1)
		self.logo = QtGui.QLabel()
		self.logo.setPixmap(QtGui.QPixmap(self.ui_mainwindow.confdir+'/pixmaps/logo_clickdial.png'))
		#self.logo.setGeometry(400, 80, 80, 30)
		layout1.addWidget(self.logo)
		
		widget2 = QtGui.QWidget()    
		widget2.setFixedSize(450,100)
		layout2 = QtGui.QVBoxLayout()
		widget2.setLayout(layout2)
		 
		self.pbar = QtGui.QProgressBar(widget2)
		self.pbar.setGeometry(130, 40, 200, 25)
		
		#self.labelLoading = QtGui.QLabel("Chargement en cours ...")
		#self.labelLoading.setGeometry(200, 150, 250, 25)
		#layout2.addWidget(QtGui.QLabel(""))
		#layout2.addWidget(QtGui.QLabel(""))
		#layout2.addWidget(self.labelLoading)


		widget3 = QtGui.QWidget()     
		widget3.setFixedSize(450,200)
		
		layout.addWidget(widget1)
		layout.addWidget(widget2)
		layout.addWidget(widget3)
		self.ui_mainwindow.setCentralWidget(self.widget_waiting)
		self.ui_mainwindow.vbox_main = Ui_VBoxMain(self, self.debug)
		self.thread.setup(self.ui_mainwindow)
		self.thread.start()
