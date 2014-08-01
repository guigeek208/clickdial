# -*- coding: latin-1 -*-
from PyQt4 import QtCore, QtGui
import os
from conpresencesrv import ConPresenceSrv

class Ui_ParamBox(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self)
		self.parent = parent
		self.parent.setEnabled(False)
		self.setupUi()
		
	def setupUi(self):
		self.resize(500, 500)
		self.setWindowTitle("Parametres")
		self.center()
		self.qtab = QtGui.QTabWidget()
		self.vbox = QtGui.QVBoxLayout()       
		self.setLayout(self.vbox)
		self.qgroupbox1 = QtGui.QGroupBox()
		self.qgroupbox2 = QtGui.QGroupBox()
		self.vbox.addWidget(self.qtab)
		self.qtab.addTab(self.qgroupbox1, "Authentification")
		self.qtab.addTab(self.qgroupbox2, "Repertoire")
		#self.vbox.addWidget(self.qgroupbox1)
		#self.vbox.addWidget(self.qgroupbox2)
		
		#Â GroupBox 1 - Authentification
		self.qTab_Auth()
		
		#Â GroupBox 2 - Choix device
		self.qTab_Dir()
		
	def qTab_Auth(self):
		layout1 = QtGui.QGridLayout()
		self.qgroupbox1.setLayout(layout1)
		self.line = 0
		
		label_addr_webdial = QtGui.QLabel("Adresse du Webdialer")
		layout1.addWidget(label_addr_webdial, self.line, 0)
		self.lineEdit_addr_webdial = QtGui.QLineEdit(self)
		self.lineEdit_addr_webdial.setMaximumWidth(150)
		if self.parent.vbox_main.click.URL != None:
			self.lineEdit_addr_webdial.setText(self.parent.vbox_main.click.URL)
		layout1.addWidget(self.lineEdit_addr_webdial, self.line, 1)
		self.line+=1
		
		label_check_presence = QtGui.QLabel("Utilisation du presence")
		layout1.addWidget(label_check_presence, self.line, 0)
		self.check_presence = QtGui.QCheckBox()
		QtCore.QObject.connect (self.check_presence, QtCore.SIGNAL ('stateChanged (int)'), self.event_checked_Presence)
		layout1.addWidget(self.check_presence, self.line, 1)
		self.line+=1
		
		label_addr_presencesrv = QtGui.QLabel("Adresse du Presence")
		layout1.addWidget(label_addr_presencesrv, self.line, 0)
		self.lineEdit_addr_presencesrv = QtGui.QLineEdit(self)
		self.lineEdit_addr_presencesrv.setMaximumWidth(150)
		if self.parent.vbox_main.click.PRESENCESRV != None:
			self.lineEdit_addr_presencesrv.setText(self.parent.vbox_main.click.PRESENCESRV)
		layout1.addWidget(self.lineEdit_addr_presencesrv, self.line, 1)
		self.line+=1
		
		label_port_presencesrv = QtGui.QLabel("Port du Presence")
		layout1.addWidget(label_port_presencesrv, self.line, 0)
		self.lineEdit_port_presencesrv = QtGui.QLineEdit(self)
		self.lineEdit_port_presencesrv.setMaximumWidth(60)
		if (self.parent.vbox_main.click.PRESENCESRVPORT != None):
			self.lineEdit_port_presencesrv.setText(str(self.parent.vbox_main.click.PRESENCESRVPORT))
		self.lineEdit_port_presencesrv.setMaxLength(5)
		layout1.addWidget(self.lineEdit_port_presencesrv, self.line, 1)
		self.line+=1
		
		if (self.parent.vbox_main.click.PRESENCE != None):
			if (self.parent.vbox_main.click.PRESENCE==1):
				self.check_presence.setChecked(True)
				self.lineEdit_addr_presencesrv.setEnabled(True)
				self.lineEdit_port_presencesrv.setEnabled(True)
			else:
				self.check_presence.setChecked(False)
				self.lineEdit_addr_presencesrv.setEnabled(False)
				self.lineEdit_port_presencesrv.setEnabled(False)
		
		
		
		label_id = QtGui.QLabel("ID utilisateur")
		layout1.addWidget(label_id, self.line, 0)
		self.lineEdit_id = QtGui.QLineEdit(self)
		self.lineEdit_id.setMaximumWidth(150)
		if (self.parent.vbox_main.click.UID != None):
			self.lineEdit_id.setText(self.parent.vbox_main.click.UID)
		layout1.addWidget(self.lineEdit_id, self.line, 1)
		self.line+=1
		
		label_pwd = QtGui.QLabel("Mot de passe")
		layout1.addWidget(label_pwd, self.line, 0)
		self.lineEdit_pwd = QtGui.QLineEdit(self)
		self.lineEdit_pwd.setMaximumWidth(150)
		if (self.parent.vbox_main.click.PWD != None):
			self.lineEdit_pwd.setText(self.parent.vbox_main.click.PWD)
		self.lineEdit_pwd.setEchoMode(QtGui.QLineEdit.Password)
		QtCore.QObject.connect (self.lineEdit_pwd, QtCore.SIGNAL ('returnPressed ()'), self.event_clicked_auth)
		QtCore.QObject.connect (self.lineEdit_pwd, QtCore.SIGNAL ('editingFinished ()'), self.event_clicked_auth)
		layout1.addWidget(self.lineEdit_pwd, self.line, 1)
		self.line+=1
		
		#butt_auth_apply = QtGui.QPushButton("Valider")
		#layout1.addWidget(butt_auth_apply, self.line, 1)
		#QtCore.QObject.connect (butt_auth_apply, QtCore.SIGNAL ('clicked()'), self.event_clicked_auth)
		#self.line+=1

		label_line = QtGui.QLabel("Ligne")
		layout1.addWidget(label_line, self.line, 0)
		
		self.qcombo_line = QtGui.QComboBox()
		self.qcombo_line.addItem("Choisir")
		self.sizeLINES = 0
		
		if (self.parent.vbox_main.click.LINES != None):
			for i in range(len(self.parent.vbox_main.click.LINES)):
				self.qcombo_line.addItem(self.parent.vbox_main.click.LINES[i])
				self.sizeLINES = self.sizeLINES + 1
		if (self.parent.vbox_main.click.LINES != None and self.parent.vbox_main.click.LINE != None):
			if (self.parent.vbox_main.click.LINE != ''):
				for i in range(len(self.parent.vbox_main.click.LINES) + 1):
					if (self.qcombo_line.itemText(i) == self.parent.vbox_main.click.LINE):
						self.qcombo_line.setCurrentIndex(i)
						break
		if (self.parent.vbox_main.click.MOBILITY == True ):
			self.qcombo_line.addItem("Mobilite")
			self.qcombo_line.setCurrentIndex(2)
			
		self.qcombo_line.addItem("Mobilite")      
		QtCore.QObject.connect (self.qcombo_line, QtCore.SIGNAL ('activated (int)'), self.event_qcombo_line_changed)
		layout1.addWidget(self.qcombo_line, self.line, 1)
		self.line+=1
		
		self.qcombo_periph = QtGui.QComboBox()
		self.qcombo_periph.addItem("Choisir")
		self.sizeDEVICES = 0
		if (self.parent.vbox_main.click.DEVICES != None):
			for i in range(len(self.parent.vbox_main.click.DEVICES)):
				self.qcombo_periph.addItem(self.parent.vbox_main.click.DEVICES[i])
				self.sizeDEVICES = self.sizeDEVICES + 1
		if (self.parent.vbox_main.click.DEVICES != None and self.parent.vbox_main.click.DEVICE != None):        
			if (self.parent.vbox_main.click.DEVICE != ''):
				for i in range(len(self.parent.vbox_main.click.DEVICES) + 1):
					if (self.qcombo_periph.itemText(i) == self.parent.vbox_main.click.DEVICE):
						self.qcombo_periph.setCurrentIndex(i)
						break
		layout1.addWidget(self.qcombo_periph, self.line, 1)
		
		label_periph = QtGui.QLabel("Telephone")
		layout1.addWidget(label_periph, self.line, 0)
		self.line+=1
		
		layout1.addWidget(QtGui.QLabel("Prefixe"), self.line, 0)
		self.qlineEdit_prefix = QtGui.QLineEdit(self)
		self.qlineEdit_prefix.setMaximumWidth(25)
		self.qlineEdit_prefix.setText(str(self.parent.vbox_main.click.PREFIX))
		layout1.addWidget(self.qlineEdit_prefix, self.line, 1)
		self.line+=1
		
		butt_line_apply = QtGui.QPushButton("Valider")
		layout1.addWidget(butt_line_apply, self.line, 1)
		QtCore.QObject.connect (butt_line_apply, QtCore.SIGNAL ('clicked()'), self.event_clicked_line)

	def event_qcombo_line_changed(self):
		if (self.qcombo_line.currentText() == "Mobilite"):
			#print "test "
			self.qcombo_periph.addItem("Mobilite")
			self.qcombo_periph.setCurrentIndex(self.qcombo_periph.count()-1)
			self.qcombo_periph.setEnabled(False)

	def qTab_Dir(self):
		self.line = 0
		self.layout_main = QtGui.QVBoxLayout()
		self.qgroupbox2.setLayout(self.layout_main)
		
		# Main Layout
		
		self.layout1 = QtGui.QGridLayout()
		widget1 = QtGui.QWidget()  
		widget1.setLayout(self.layout1)         
		self.layout1.addWidget(QtGui.QLabel("Utilisation du serveur XML"), self.line, 0)
		self.check_srvXML = QtGui.QCheckBox()
		QtCore.QObject.connect (self.check_srvXML, QtCore.SIGNAL ('stateChanged (int)'), self.widgetsrvXML)
		self.layout1.addWidget(self.check_srvXML, self.line, 1)
		self.line+=1
		
		self.layout_main.addWidget(widget1)   

		#  Widget pour XML Serveur
		self.widget2 = QtGui.QWidget()
		self.layout2 = QtGui.QGridLayout()
		self.widget2.setLayout(self.layout2) 
		self.layout_main.addWidget(self.widget2)
		
		if (self.parent.vbox_main.click.XML==1):
			self.check_srvXML.setChecked(True)
			#self.widgetsrvXML()

		# Integration Mail
		self.layout3 = QtGui.QGridLayout()
		widget3 = QtGui.QWidget()  
		widget3.setLayout(self.layout3)         
		self.layout3.addWidget(QtGui.QLabel("Integration Mail"), self.line, 0)
		self.qcombo_mail = QtGui.QComboBox()
		QtCore.QObject.connect (self.qcombo_mail, QtCore.SIGNAL ('activated (int)'), self.event_qcombo_mail_changed)
		self.layout3.addWidget(self.qcombo_mail, self.line, 1)
		self.qcombo_mail.addItem("Aucun")
		self.qcombo_mail.addItem("Zimbra")

		self.widget_Outlook = None
		self.widget_Zimbra = None
		self.line+=1
		os.name = "nt"
		if (os.name == "nt"):
			self.qcombo_mail.addItem("Outlook")
		
		self.layout_main.addWidget(widget3)
		
		#  Widget pour Serveur de Mails
		self.widget4 = QtGui.QWidget()
		self.layout4 = QtGui.QGridLayout()
		self.widget4.setLayout(self.layout4) 
		self.layout_main.addWidget(self.widget4)
		self.layout_main.addStretch(1)

		if (self.parent.vbox_main.click.OUTLOOK == 1):
			self.qcombo_mail.setCurrentIndex(2)
			self.widgetOutlook()
		if (self.parent.vbox_main.click.ZIMBRA == 1):
			self.qcombo_mail.setCurrentIndex(1)
			self.widgetZimbra()

		butt_dir_apply = QtGui.QPushButton("Valider")
		self.layout_main.addWidget(butt_dir_apply)
		QtCore.QObject.connect (butt_dir_apply, QtCore.SIGNAL ('clicked()'), self.event_clicked_dir)
		

	def deleteLayout(self, layout):
		if layout is not None: 
			while layout.count(): 
				item = layout.takeAt(0) 
				widget = item.widget() 
				if widget is not None: 
					widget.deleteLater() 

	def widgetsrvXML(self):
		self.line = 0
		if QtGui.QCheckBox.checkState(self.check_srvXML) == 2:   
			self.lineEdit_addr_srvXML = QtGui.QLineEdit(self)
			#self.lineEdit_addr_srvXML.setMaximumWidth(250)
			if self.parent.vbox_main.click.XMLSRV != None:
				self.lineEdit_addr_srvXML.setText(self.parent.vbox_main.click.XMLSRV)
			self.layout2.addWidget(self.lineEdit_addr_srvXML, self.line, 0)
			self.line+=1
		else:
			self.deleteLayout(self.layout2)
			self.widget2.adjustSize()

	def widgetZimbra(self):	
		self.line = 0
		self.layout4.addWidget(QtGui.QLabel("Utilisation de Contacts partages Zimbra"), self.line, 0)
		self.check_zimbra_contact_shared = QtGui.QCheckBox()
		self.layout4.addWidget(self.check_zimbra_contact_shared, self.line, 1)
		self.line+=1
		self.layout4.addWidget(QtGui.QLabel("Nom des Contacts partages Zimbra"), self.line, 0)
		self.check_zimbra_contact_shared = QtGui.QLineEdit()
		self.layout4.addWidget(self.check_zimbra_contact_shared, self.line, 1)
		self.line+=1

	def widgetOutlook(self):
		self.line_contacts = 0
		#self.layout4.addWidget(QtGui.QLabel("Utilisation de Contacts Outlook"), self.line, 0)
		self.check_outlook_contact = QtGui.QCheckBox("Utilisation de Contacts Outlook")
		if (self.parent.vbox_main.click.OUTLOOK_CONTACTS == 1):
			self.check_outlook_contact.setChecked(True)	
		self.layout4.addWidget(self.check_outlook_contact, self.line_contacts, 0)
		self.line_contacts+=1
		self.listQline = []
		for i in range(len(self.parent.vbox_main.click.OUTLOOK_CONTACTS_SHARED)):
			print self.parent.vbox_main.click.OUTLOOK_CONTACTS_SHARED[i]
			qlineEdit = QtGui.QLineEdit(self.parent.vbox_main.click.OUTLOOK_CONTACTS_SHARED[i])
			self.layout4.addWidget(qlineEdit, self.line_contacts, 0)
			self.line_contacts+=1
			self.listQline.append(qlineEdit)

		self.layout4.addWidget(QtGui.QLabel("Ajouter un carnet d'adresses partages Outlook"), self.line_contacts, 0)
		self.pushbutton_add_contact = QtGui.QPushButton()
		self.pushbutton_add_contact.setIcon(QtGui.QIcon(self.parent.confdir+'/pixmaps/contact.png'))
		self.pushbutton_add_contact.setFixedSize(24, 24)
		QtCore.QObject.connect (self.pushbutton_add_contact, QtCore.SIGNAL ('clicked()'), self.add_shared_contact_outlook)
		self.linedit_outlook_contact_shared = QtGui.QLineEdit()
		self.layout4.addWidget(self.pushbutton_add_contact, self.line_contacts, 1)
		self.line_contacts+=1

	def add_shared_contact_outlook(self):
		print "test"
		qlineEdit = QtGui.QLineEdit("")
		self.layout4.addWidget(qlineEdit, self.line_contacts, 0)
		self.line_contacts+=1

	def event_qcombo_mail_changed(self):
		if (self.qcombo_mail.currentText() == "Aucun"):
			self.deleteLayout(self.layout4)
		if (self.qcombo_mail.currentText() == "Zimbra"):
			self.deleteLayout(self.layout4)
			self.widgetZimbra()
		if (self.qcombo_mail.currentText() == "Outlook"):			
			self.deleteLayout(self.layout4)
			self.widgetOutlook()
   
	def event_checked_Presence(self):
		if QtGui.QCheckBox.checkState(self.check_presence) == 2:
			self.lineEdit_addr_presencesrv.setEnabled(True)
			self.lineEdit_port_presencesrv.setEnabled(True)
		else:
			self.lineEdit_addr_presencesrv.setEnabled(False)
			self.lineEdit_port_presencesrv.setEnabled(False)

	def event_clicked_auth(self):
		print "Auth"
		self.parent.vbox_main.click.URL = str(self.lineEdit_addr_webdial.text())	
		self.parent.vbox_main.click.UID = str(self.lineEdit_id.text())
		self.parent.vbox_main.click.PWD = str(self.lineEdit_pwd.text())
		
		self.parent.vbox_main.click.log_in()
		if QtGui.QCheckBox.checkState(self.check_presence) == 2:
			self.parent.vbox_main.click.PRESENCESRV = str(self.lineEdit_addr_presencesrv.text())
			self.parent.vbox_main.click.PRESENCESRVPORT = int(self.lineEdit_port_presencesrv.text())
			self.lineEdit_addr_presencesrv.setEnabled(True)
			self.lineEdit_port_presencesrv.setEnabled(True)
			self.parent.vbox_main.ui_vboxup.pushbutton_transfer.show()
			self.parent.vbox_main.ui_vboxup.pushbutton_holdon.show()
			self.parent.vbox_main.click.PRESENCE = 1
			if (self.parent.vbox_main.con != None):
				self.parent.vbox_main.con.stop()
			self.parent.vbox_main.con = ConPresenceSrv(self.parent.vbox_main.click.UID, self.parent.vbox_main.click.PWD, self.parent.vbox_main.click.PRESENCESRV, self.parent.vbox_main.click.PRESENCESRVPORT, self.parent.vbox_main.click)
			self.parent.vbox_main.con.start()
			self.parent.vbox_main.treeList_contacts.show()
		else:
			print "No Presence"
			if (self.parent.vbox_main.click.PRESENCE == 1):
				self.lineEdit_addr_presencesrv.setEnabled(False)
				self.lineEdit_port_presencesrv.setEnabled(False)
				self.parent.vbox_main.ui_vboxup.pushbutton_transfer.hide()
				self.parent.vbox_main.ui_vboxup.pushbutton_holdon.hide()
				self.parent.vbox_main.click.PRESENCE = 0
				self.parent.vbox_main.con.stop()
			self.parent.vbox_main.treeList_contacts.hide()
		if QtGui.QCheckBox.checkState(self.check_srvXML) == 2:
			self.parent.vbox_main.click.XML = 1
			self.parent.vbox_main.click.XMLSRV = str(self.lineEdit_addr_srvXML.text())
			if (self.parent.vbox_main.load_directory_ents()):
				self.parent.vbox_main.qtab.addTab(self.parent.vbox_main.treeList_directoryents, "Entreprise")
				self.parent.vbox_main.tabXML = self.parent.vbox_main.nbTabs
				self.parent.vbox_main.nbTabs = self.parent.vbox_main.nbTabs + 1
		else:
			self.parent.vbox_main.click.XML = 0
			self.parent.vbox_main.qtab.removeTab(self.parent.vbox_main.tabXML)
			#self.parent.vbox_main.treeList_directoryents.hide() 
			
		self.connect(self.parent.vbox_main.con, QtCore.SIGNAL("updateStatus"), self.parent.vbox_main.changeItemTreeWidgetContacts)
		self.connect(self.parent.vbox_main.con, QtCore.SIGNAL("updateStatusBar"), self.parent.vbox_main.updateStatusBar)
		self.qcombo_periph.clear()
		self.qcombo_periph.addItem("Choisir")
		self.qcombo_line.clear()
		self.qcombo_line.addItem("Choisir")
		self.qcombo_line.setEnabled(True)
		self.qcombo_periph.setEnabled(True)
		for i in range(len(self.parent.vbox_main.click.DEVICES)):
			self.qcombo_periph.addItem(self.parent.vbox_main.click.DEVICES[i])
		for i in range(len(self.parent.vbox_main.click.LINES)):
			self.qcombo_line.addItem(self.parent.vbox_main.click.LINES[i])
		self.qcombo_line.addItem("Mobilite")	
		#self.qcombo_line.setEnabled(False)
		#self.qcombo_periph.setEnabled(False)
		
	def event_clicked_line(self):
		print "Line"
		if (QtGui.QCheckBox.checkState(self.check_presence)==2):
			self.parent.vbox_main.click.PRESENCESRV = str(self.lineEdit_addr_presencesrv.text())
			self.parent.vbox_main.click.PRESENCESRVPORT = int(self.lineEdit_port_presencesrv.text())
			self.lineEdit_addr_presencesrv.setEnabled(True)
			self.lineEdit_port_presencesrv.setEnabled(True)
			self.parent.vbox_main.ui_vboxup.pushbutton_transfer.show()
			self.parent.vbox_main.ui_vboxup.pushbutton_holdon.show()
			self.parent.vbox_main.click.PRESENCE = 1
			if (self.parent.vbox_main.con != None):
				self.parent.vbox_main.con.stop()
			self.parent.vbox_main.con = ConPresenceSrv(self.parent.vbox_main.click.UID, self.parent.vbox_main.click.PWD, self.parent.vbox_main.click.PRESENCESRV, self.parent.vbox_main.click.PRESENCESRVPORT, self.parent.vbox_main.click)
			self.parent.vbox_main.con.start()
			self.parent.vbox_main.treeList_contacts.show()
		else:	
			print "No Presence"
			self.parent.vbox_main.click.PRESENCESRV = None
			self.parent.vbox_main.click.PRESENCESRVPORT = None
			if (self.parent.vbox_main.click.PRESENCE == 1):
				self.lineEdit_addr_presencesrv.setEnabled(False)
				self.lineEdit_port_presencesrv.setEnabled(False)
				self.parent.vbox_main.ui_vboxup.pushbutton_transfer.hide()
				self.parent.vbox_main.ui_vboxup.pushbutton_holdon.hide()
				self.parent.vbox_main.click.PRESENCE = 0
				self.parent.vbox_main.con.stop()
				self.parent.vbox_main.treeList_contacts.hide()
		self.parent.vbox_main.click.URL = str(self.lineEdit_addr_webdial.text())
		self.parent.vbox_main.click.UID = str(self.lineEdit_id.text())
		self.parent.vbox_main.click.PWD = str(self.lineEdit_pwd.text())
		self.parent.vbox_main.click.DEVICE = str(self.qcombo_periph.currentText())
		self.parent.vbox_main.click.LINE = str(self.qcombo_line.currentText())
		self.parent.vbox_main.click.PREFIX = int(self.qlineEdit_prefix.text())
		self.parent.vbox_main.ui_vboxup.lineEditPrefix.setText(str(self.qlineEdit_prefix.text()))

	def event_clicked_dir(self):
		print "Dir"
		if QtGui.QCheckBox.checkState(self.check_srvXML) == 2:
			self.parent.vbox_main.click.XML = 1
			self.parent.vbox_main.click.XMLSRV = str(self.lineEdit_addr_srvXML.text())
			if len(self.parent.vbox_main.list_contacts_ents_name) == 0:
				self.parent.vbox_main.load_directory_ents()
		else:
			print "no dir"
			#self.parent.vbox_main.qtab.removeTab(0)
			self.parent.vbox_main.click.XML = 0
			self.parent.vbox_main.click.XMLSRV = None
		if (self.qcombo_mail.currentText() == "Aucun"):
			self.parent.vbox_main.click.ZIMBRA = 0
			self.parent.vbox_main.click.ZIMBRA_CONTACTS_SHARED = []
			self.parent.vbox_main.click.OUTLOOK = 0
			self.parent.vbox_main.click.OUTLOOK_CONTACTS_SHARED = []
		if (self.qcombo_mail.currentText() == "Zimbra"):
			self.parent.vbox_main.click.ZIMBRA = 1
		if (self.qcombo_mail.currentText() == "Outlook"):
			self.parent.vbox_main.click.OUTLOOK = 1
			if QtGui.QCheckBox.checkState(self.check_outlook_contact) == 2:
				self.parent.vbox_main.click.OUTLOOK_CONTACTS = 1
			else:
				self.parent.vbox_main.click.OUTLOOK_CONTACTS = 0	
		self.parent.vbox_main.displayDirectoryEnts()

	def center(self):     
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def closeEvent(self, event):
		self.parent.setEnabled(True)
		self.parent.vbox_main.click.save_settings()
