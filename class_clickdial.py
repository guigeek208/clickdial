# -*- coding: latin-1 -*-
import urllib2, urllib, cookielib
import httplib
import re
import xml.dom.minidom
from xml.dom.minidom import Document
from PyQt4 import QtGui

class ClickDial:
    def  __init__(self, vboxlogin, debug):
        self.debug = debug
        if (self.debug):
            print "init ClickDial"
        self.vboxlogin= vboxlogin
        #self.URL = None
        self.HOST = None
        self.URL2 = '/webdialer/services/WebdialerSoapService?wsdl'
        self.PWD = None
        self.UID = None
        self.MOBILITY = None
        self.DEVICE = None
        self.DEVICES = None
        self.LINE = None
        self.LINES = None
        self.CONNECTED = None
        self.PRESENCE = 0
        self.PRESENCESRV = None
        self.PRESENCESRVPORT = None
        self.XML = 0
        self.XMLSRV = None
        self.PREFIX = "0"
        self.ZIMBRA = 0
        self.ZIMBRA_CONTACTS_SHARED = []
        self.OUTLOOK = 0
        self.OUTLOOK_CONTACTS= 0
        self.OUTLOOK_CONTACTS_SHARED = []
        self.cj = cookielib.CookieJar()
        self.load_settings()
        if (self.URL2 is None or self.PWD is None or self.UID is None or self.DEVICE is None or self.LINE is None):
            msgBox = QtGui.QMessageBox.warning(self.vboxlogin, "ClickDial",
                                "Erreur verifiez vos parametres",
                                QtGui.QMessageBox.Ok);

    def load_settings(self):
        if (self.debug):
            print "Load Settings"
        try:
            f = open(self.vboxlogin.ui_mainwindow.confdir+'/clickdial.conf', 'r')
        except:
            msgBox = QtGui.QMessageBox.warning(self.vboxlogin, "ClickDial",
                                "Aucun configuration chargee",
                                QtGui.QMessageBox.Ok);
            return False
        file = f.read()
        doc = xml.dom.minidom.parseString(file)
        for node in doc.getElementsByTagName('configuration'):
            elts = xml.dom.minidom.parseString(node.toxml())
            regex = re.compile("\s*(.+)\s*")
            r = regex.match(str(elts.getElementsByTagName('cucm')[0].childNodes[0].data))
            if (r):
                self.HOST = r.group(1)
            # Parcoure les utilisateurs
            for node2 in elts.getElementsByTagName('user'):
                elts2 = xml.dom.minidom.parseString(node2.toxml())
                r = regex.match(str(elts2.getElementsByTagName('login')[0].childNodes[0].data))
                if (r):
                    self.UID = r.group(1)
                r = regex.match(str(elts2.getElementsByTagName('pwd')[0].childNodes[0].data))
                if (r):
                    self.PWD = r.group(1)
                r = regex.match(str(elts2.getElementsByTagName('device')[0].childNodes[0].data))
                if (r):
                    self.DEVICE = r.group(1)
                r = regex.match(str(elts2.getElementsByTagName('line')[0].childNodes[0].data))
                if (r):
                    self.LINE = r.group(1)

            # Parcoure les infos du presence
            for node2 in elts.getElementsByTagName('presence'):
                elts2 = xml.dom.minidom.parseString(node2.toxml())    
                r = regex.match(str(elts2.getElementsByTagName('status')[0].childNodes[0].data))
                if (r):
                    self.PRESENCE = int(r.group(1))
                    if (self.PRESENCE == 1):
                        r = regex.match(str(elts2.getElementsByTagName('addr')[0].childNodes[0].data))
                        if (r):
                            self.PRESENCESRV = r.group(1)
                        r = regex.match(str(elts2.getElementsByTagName('port')[0].childNodes[0].data))
                        if (r):
                            try:
                                self.PRESENCESRVPORT = int(r.group(1))
                            except:
                                self.PRESENCESRVPORT = None

            # Parcoure les infos du srvxml
            for node2 in elts.getElementsByTagName('directory'):
                elts2 = xml.dom.minidom.parseString(node2.toxml())
                for node3 in elts.getElementsByTagName('srvxml'):
                    elts3 = xml.dom.minidom.parseString(node3.toxml())    
                    r = regex.match(str(elts3.getElementsByTagName('status')[0].childNodes[0].data))
                    if (r):
                        self.XML = int(r.group(1))
                    if (self.XML == 1):
                        r = regex.match(str(elts3.getElementsByTagName('addr')[0].childNodes[0].data))
                        if (r):
                            self.XMLSRV = r.group(1)
                for node3 in elts.getElementsByTagName('outlook'):
                    elts3 = xml.dom.minidom.parseString(node3.toxml())    
                    r = regex.match(str(elts3.getElementsByTagName('status')[0].childNodes[0].data))
                    if (r):
                        self.OUTLOOK = int(r.group(1))
                    if (self.OUTLOOK == 1):
                        r = regex.match(str(elts3.getElementsByTagName('contacts')[0].childNodes[0].data))
                        if (r):
                            self.OUTLOOK_CONTACTS = int(r.group(1))
                        for i in range(len(elts3.getElementsByTagName('contactsShared'))):
                            self.OUTLOOK_CONTACTS_SHARED.append(str(elts3.getElementsByTagName('contactsShared')[i].childNodes[0].data))
                        
                for node3 in elts.getElementsByTagName('zimbra'):
                    elts3 = xml.dom.minidom.parseString(node3.toxml())    
                    r = regex.match(str(elts3.getElementsByTagName('status')[0].childNodes[0].data))
                    if (r):
                        self.ZIMBRA = int(r.group(1))
                    if (self.ZIMBRA == 1):
                        for i in range(len(elts3.getElementsByTagName('contacts'))):
                            self.ZIMBRA_CONTACTS_SHARED.append(str(elts3.getElementsByTagName('contacts')[i].childNodes[0].data))

            r = regex.match(str(elts.getElementsByTagName('prefix')[0].childNodes[0].data))
            if (r):
                self.PREFIX = int(r.group(1))

    def save_settings(self):
        # Create the minidom document
        doc = Document()
        # Create the <wml> base element
        #maincard.setAttribute("id", "main")
        fxml = doc.createElement("configuration")
        doc.appendChild(fxml)

        cucm = doc.createElement("cucm")
        cucm.appendChild(doc.createTextNode(self.URL))
        fxml.appendChild(cucm)
        
        user = doc.createElement("user")
        login = doc.createElement("login")
        user.appendChild(login)
        login.appendChild(doc.createTextNode(self.UID))
        pwd = doc.createElement("pwd")
        user.appendChild(pwd)
        pwd.appendChild(doc.createTextNode(self.PWD))
        device = doc.createElement("device")
        user.appendChild(device)
        device.appendChild(doc.createTextNode(self.DEVICE))
        line = doc.createElement("line")
        user.appendChild(line)
        line.appendChild(doc.createTextNode(self.LINE))
        fxml.appendChild(user)        
        
        presence = doc.createElement("presence")
        status = doc.createElement("status")
        presence.appendChild(status)
        if (self.PRESENCE != None):
            status.appendChild(doc.createTextNode(str(self.PRESENCE)))
        addr = doc.createElement("addr")
        presence.appendChild(addr)
        if (self.PRESENCESRV != None):
            addr.appendChild(doc.createTextNode(self.PRESENCESRV))
        else:
            addr.appendChild(doc.createTextNode(""))
        port=doc.createElement("port")
        presence.appendChild(port)
        if (self.PRESENCESRVPORT != None):
            port.appendChild(doc.createTextNode(str(self.PRESENCESRVPORT)))
        else:
            port.appendChild(doc.createTextNode(""))
        fxml.appendChild(presence)
        
        directory = doc.createElement("directory")
        srvxml = doc.createElement("srvxml")
        directory.appendChild(srvxml)
        status = doc.createElement("status")
        srvxml.appendChild(status)
        if (self.XML != None):
            status.appendChild(doc.createTextNode(str(self.XML)))
        else:
            status.appendChild(doc.createTextNode(""))
        addr = doc.createElement("addr")
        srvxml.appendChild(addr)
        if (self.XMLSRV != None):
            addr.appendChild(doc.createTextNode(self.XMLSRV))
        else:
            addr.appendChild(doc.createTextNode(""))
        outlook = doc.createElement("outlook")
        directory.appendChild(outlook)
        status = doc.createElement("status")
        outlook.appendChild(status)
        if (self.OUTLOOK != None):
            status.appendChild(doc.createTextNode(str(self.OUTLOOK)))
        else:
            status.appendChild(doc.createTextNode(""))
        contacts = doc.createElement("contacts")
        outlook.appendChild(contacts)
        if (self.OUTLOOK_CONTACTS != None):
            contacts.appendChild(doc.createTextNode(str(self.OUTLOOK_CONTACTS)))
        else:
            contacts.appendChild(doc.createTextNode(""))
        for i in range(len(self.OUTLOOK_CONTACTS_SHARED)):
            contactsShared = doc.createElement("contactsShared")
            outlook.appendChild(contactsShared)
            if (self.OUTLOOK_CONTACTS_SHARED[i] != None):
                contactsShared.appendChild(doc.createTextNode(str(self.OUTLOOK_CONTACTS_SHARED[i])))
            else:
                contactsShared.appendChild(doc.createTextNode(""))
        zimbra = doc.createElement("zimbra")
        directory.appendChild(zimbra)
        status = doc.createElement("status")
        zimbra.appendChild(status)
        if (self.ZIMBRA != None):
            status.appendChild(doc.createTextNode(str(self.ZIMBRA)))
        else:
            status.appendChild(doc.createTextNode(""))
        for i in range(len(self.ZIMBRA_CONTACTS_SHARED)):
            contacts = doc.createElement("contacts")
            zimbra.appendChild(contacts)
            if (self.ZIMBRA_CONTACTS_SHARED[i] != None):
                contacts.appendChild(doc.createTextNode(str(self.ZIMBRA_CONTACTS_SHARED[i])))
            else:
                contacts.appendChild(doc.createTextNode(""))
        fxml.appendChild(directory)
        
        prefix = doc.createElement("prefix")
        if (self.PREFIX != None):
            prefix.appendChild(doc.createTextNode(str(self.PREFIX)))
        else:
            prefix.appendChild(doc.createTextNode(""))
        fxml.appendChild(prefix)
        
        fh = open(self.vboxlogin.ui_mainwindow.confdir+'/clickdial.conf', 'w')
        fh.write(doc.toprettyxml())
        fh.close()    
    
    def _SOAP_post(self, SOAPAction,xml):
        """Handles making the SOAP request"""
        h = httplib.HTTPSConnection(self.HOST)
        headers={
            'Host':self.HOST,
           'Content-Type':'text/xml; charset=utf-8',
            'Content-Length':len(xml),
            'SOAPAction':'"%s"' % SOAPAction,
        }
        h.request ('POST', self.URL2, body=xml,headers=headers)
        r = h.getresponse()
        d = r.read()
        if r.status!=200:
            raise ValueError('Error connecting: %s, %s' % (r.status, r.reason))
        return d
    
    def _makeCall(self, dn, anonymous):
        if (self.DEVICE == None):
            self.MOBILITY = 'true'
        else:
            self.MOBILITY = 'false'
        regex = re.compile("(\d)(\d+)")
        r = regex.match(dn)
        if (r):    
            prefix = r.group(1)
            num = r.group(2)
        if (anonymous):
            dn = prefix+"3651"+num
        in_xml="""\
    <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:WebdialerSoap">
       <soapenv:Header/>
       <soapenv:Body>
          <urn:makeCallSoap soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
             <cred xsi:type="urn:Credential">
                <userID xsi:type="xsd:string">%s</userID>
                <password xsi:type="xsd:string">%s</password>
             </cred>
             <dest xsi:type="xsd:string">%s</dest>
             <prof xsi:type="urn:UserProfile">
                <user xsi:type="xsd:string">%s</user>
                <deviceName xsi:type="xsd:string">%s</deviceName>
                <lineNumber xsi:type="xsd:string">1</lineNumber>
                <supportEM xsi:type="xsd:boolean">%s</supportEM>
                <locale xsi:type="xsd:string"></locale>
             </prof>
          </urn:makeCallSoap>
       </soapenv:Body>
    </soapenv:Envelope>""" % (self.UID,self.PWD,dn,self.UID,self.DEVICE,self.MOBILITY)
        result_xml=self._SOAP_post("https://"+self.HOST+self.URL2,in_xml)
        doc=xml.dom.minidom.parseString(result_xml)
        #print result_xml
        return True
    
    def _stopCall(self):
        if (self.DEVICE == None):
            self.MOBILITY = 'true'
        else:
            self.MOBILITY = 'false'
        in_xml="""\
    <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:WebdialerSoap">
       <soapenv:Header/>
       <soapenv:Body>
          <urn:endCallSoap soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
             <cred xsi:type="urn:Credential">
                <userID xsi:type="xsd:string">%s</userID>
                <password xsi:type="xsd:string">%s</password>
             </cred>
             <prof xsi:type="urn:UserProfile">
                <user xsi:type="xsd:string">%s</user>
                <deviceName xsi:type="xsd:string">%s</deviceName>
                <supportEM xsi:type="xsd:boolean">%s</supportEM>
                <locale xsi:type="xsd:string"></locale>
             </prof>
          </urn:endCallSoap>
       </soapenv:Body>
    </soapenv:Envelope>""" % (self.UID,self.PWD,self.UID,self.DEVICE,self.MOBILITY)
        result_xml=self._SOAP_post("https://"+self.HOST+self.URL2,in_xml)
        doc=xml.dom.minidom.parseString(result_xml)
        #print result_xml
        return True
    
    def log_in(self):
        self.CONNECTED = 0
        self.DEVICES = []
        self.LINES = []
        """First call logon to get your token"""
        in_xml="""\
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:tns="urn:WebdialerSoap" 
    xmlns:types="urn:WebdialerSoap/encodedTypes" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soap:Body soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <tns:getProfileSoap>
                <cred href="#id1" /> 
                <userid xsi:type="xsd:string">%s</userid> 
            </tns:getProfileSoap>
            <tns:Credential id="id1" xsi:type="tns:Credential">
                <userID xsi:type="xsd:string">%s</userID> 
                <password xsi:type="xsd:string">%s</password> 
            </tns:Credential>
        </soap:Body>
    </soap:Envelope>""" % (self.UID,self.UID,self.PWD)
        result_xml=self._SOAP_post("https://"+self.HOST+self.URL2,in_xml)
        doc=xml.dom.minidom.parseString(result_xml)
        #print result_xml
        response=doc.getElementsByTagName('description')[0].firstChild.data
        print response
        if (response == "Success"):
            self.CONNECTED = 1
            multiref=doc.getElementsByTagName('multiRef')
            for node in multiref:
                #conf_name=node.getAttribute('name')
                #print conf_name
                alist=node.getElementsByTagName('deviceName')
                for a in alist:
                    device= a.childNodes[0].nodeValue
                    self.DEVICES.append(device)
                alist=node.getElementsByTagName('lines')
                for a in alist:
                    line= a.childNodes[0].firstChild.data
                    self.LINES.append(line)
            return True
        else:
            self.CONNECTED = 0
            return False