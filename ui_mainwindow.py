# -*- coding: latin-1 -*-
from PyQt4 import QtCore, QtGui
import platform, shutil
import os
from ui_vboxlogin import Ui_VBoxLogIn
from ui_parambox import Ui_ParamBox

class Ui_MainWindow(QtGui.QMainWindow):
	def __init__(self, debug, parent=None):
		#super(Ui_clickdial, self).__init__()
		self.debug = debug
		if (self.debug):
			print os.name 
			print os.environ.get("HOME")
		homedir = os.path.expanduser('~')
		if (platform.system() == "Linux"):
			if (self.debug):
				print "Linux"
			self.confdir = homedir + "/.clickdial"    		
		if (platform.system() == "Windows"):
			if (self.debug):
				print "Windows"
				print platform.release()
			self.confdir = homedir + "/clickdial"
		if (self.debug):
			print self.confdir
		try:
			os.stat(self.confdir)
		except:
			os.mkdir(self.confdir)
			if (self.debug):
				print os.getcwd()
			shutil.copytree(os.getcwd()+ "/pixmaps", self.confdir+"/pixmaps")
		#if (os.name == "windows"):
		#    import win32com.client
		#print os.environ.get("XDG_CURRENT_DESKTOP")
		QtGui.QMainWindow.__init__(self)
		self.setWindowTitle("ClickDial")
		self.resize(450, 700)       
		self.setWindowModality(QtCore.Qt.NonModal)
		self.center()
		self.setWindowIcon(QtGui.QIcon(self.confdir+"/pixmaps/icon.png"))
		self.setupUi()
	
	def setupUi(self):
		self.hideWin = 0
		trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon(self.confdir+"/pixmaps/icon.png"), self)
		menu = QtGui.QMenu()
		exitAction = menu.addAction("Quitter")
		exitAction.triggered.connect(self.close)
		trayIcon.setContextMenu(menu)
		QtCore.QObject.connect (trayIcon, QtCore.SIGNAL ('activated (QSystemTrayIcon::ActivationReason)'), self.trayicon_activated)
		trayIcon.show()

		self.statusbar = self.statusBar()
		self.statusbar.showMessage('En Ligne')
		if (self.debug):
			print "Creation VBoxMain"
		self.vbox_login = Ui_VBoxLogIn(self, self.debug)
		self.setCentralWidget(self.vbox_login)
		#self.vbox_main = Ui_VBoxMain(self, self.debug)
		#self.setCentralWidget(self.vbox_main)
	
	def trayicon_activated(self):
		print "activate"
		if (self.hideWin == 0):
			self.hide()
			self.hideWin = 1
		else:
			self.show()
			self.hideWin = 0

	def uiParam(self):
		self.ui_parambox = Ui_ParamBox(self)
		self.ui_parambox.show()
	
	def updateStatusBar(self, msg):
		self.statusBar().showMessage(msg)
		
	def center(self):     
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		
	def updatePBar(self, val):
		self.vbox_login.pbar.setValue(val)
		if (val == 20):
			self.vbox_main.load_directoryperso()
		if (val == 40):
			self.vbox_main.load_directory_ents()
		if (val == 60):
			self.vbox_main.load_contacts()
		if (val == 80):
			if (os.name == "nt" and self.vbox_main.click.OUTLOOK == 1):
				if (self.vbox_main.click.OUTLOOK_CONTACTS == 1):
					self.vbox_main.load_directoryoutlook()
				for i in range(len(self.vbox_main.click.OUTLOOK_CONTACTS_SHARED)):
					self.vbox_main.load_directoryoutlookSharedContacts(self.vbox_main.treeList_directoryoutlookcontactsshared[i], self.vbox_main.click.OUTLOOK_CONTACTS_SHARED[i])
			#		self.vbox_main.click.OUTLOOK = 0
			#	else:
			#		self.vbox_main.click.OUTLOOK = 1
		if (val == 100):
			self.vbox_main.load_history()
			self.vbox_main.displayDirectoryEnts()
		menubar = QtGui.QMenuBar(self)
		menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
		menubar.setObjectName("menubar")

		menuFile = QtGui.QMenu(menubar)
		menuFile.setObjectName("menuFile")
		self.setMenuBar(menubar)

		exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Quitter', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(self.close)
		
		paramAction = QtGui.QAction(self)
		paramAction.setShortcut('Ctrl+P')
		paramAction.setText("Parametres")
		paramAction.triggered.connect(self.uiParam)

		menuFile.addSeparator()
		menuFile.addAction(paramAction)
		menuFile.addAction(exitAction)
		menubar.addAction(menuFile.menuAction())

		menuFile.setTitle(QtGui.QApplication.translate("ClickDial", "Outils", None, QtGui.QApplication.UnicodeUTF8))

	def finishLoad(self):
		self.setCentralWidget(self.vbox_main)
