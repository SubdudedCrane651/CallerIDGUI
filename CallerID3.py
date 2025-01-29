from ast import Break
import time
import threading
import queue
#pip install pyserial
import serial,glob,os
from PySide6.QtWidgets import QApplication, QWidget,QPushButton,QPlainTextEdit
from PySide6.QtCore import QFile
from callerid import Ui_Form
from PySide6 import QtCore, QtGui
from PySide6.QtGui import QTextCursor,QIcon
import sys
import signal
import smtplib
import sqlite3
from datetime import datetime

dev = "COM"
#dev  = "/dev/ttyACM*"
#scan = glob.glob(dev)
scan=dev
rate = "115200"
global phonenumber
phonenumber=""
global name
name=""
global NMBR
NMBR=False
global sametxt
sametxt=""
global thefirst
thefirst=True
TestTxt = "NMBR = 5147422840\r\nNAME = RICHRD'S CELL\r\n"
global importweb
importweb=False
info = ["",""]
email = ["","","",""]
global command
command = ""
global ser
global line
line=""
global line2
line2=""
commands = ["HELP","ADD","EMAIL","SPEAK","TEST","REPORT","QUIT"]

def f(thesame):
    globals().update(locals())

def s(ser):
    globals().update(locals()) 

def lg(line):
    globals().update(locals())

def sendmail(phonenumber,name,calldate):
    con = sqlite3.connect('CallerID.db')

    corsur = con.execute("SELECT * FROM mail WHERE ID = 1")
      
    for row in corsur:
        address=str(row[1])
        host=str(row[2])
        port=int(row[3])
        password=str(row[4])

    con.close()

    smtpobj = smtplib.SMTP(host, port)
    if password !="" and password !="password":
      smtpobj.ehlo()
      smtpobj.starttls()
      smtpobj.ehlo()

    senderemail_id=address
    receiveremail_id=address
    senderemail_id_password=password

    # Authentication for signing to gmail account
    if password !="" and password !="password":
      smtpobj.login(senderemail_id, senderemail_id_password)

    SUBJECT="Call received from "+name+" with "+phonenumber
    MESSAGE=name + " called the " + calldate + " with number " + phonenumber
    #message = f'From: {address}\n\nTo: {address}\n\nSubject: {SUBJECT}\n\n{MESSAGE}'

    message = f'From: From CallerID <{address}>\nTo: To Person <{address}>\nSubject: {SUBJECT}\n\n{MESSAGE}'

    print(message)

    smtpobj.sendmail(senderemail_id,receiveremail_id,message)
    time.sleep(2)
    # Hereby terminate the session
    smtpobj.quit()

    #mail = "echo  \""+ name + " Called the " + calldate + " with number " + phonenumber+"\" | mail -s \""+ name + " with number "+ phonenumber+" Called the " + calldate+"\" "+address
    #subprocess.call(mail, shell=True)

def CheckNumbers(phonenumber,name):

    con = sqlite3.connect('CallerID.db')

    corsur = con.execute("SELECT * FROM checknumbers WHERE RealNumber = '"+phonenumber+"'")
    
    for row in corsur:
      name=str(row[2])
    
    con.close()

    return name

def SaveCall(phonenumber,name):

  phonenumber=phone_format(str(phonenumber))

  con = sqlite3.connect('CallerID.db')

  d = datetime.now()

  calldate = d.strftime("%Y-%b-%d %H:%M:%S")

  con.execute("INSERT INTO phonecalls (name,phonenumber,calldate,Fax) VALUES ('"+str(name).replace("'","''")+"','"+phonenumber+"','"+str(calldate)+"',False)")

  con.commit()
  #print("Records created successfully")
  text = "\nCall detected\n"
  text +="Date Time: "+calldate+"\n"
  text +="Name: "+name+"\n"
  text +="Phonenumber: "+str(phonenumber)+"\n\n"
  print(text)
  window.plainTextEdit.insertPlainText(text)
  cursor = window.plainTextEdit.textCursor()
  cursor.movePosition(QTextCursor.MoveOperation.End)
  window.plainTextEdit.setTextCursor(cursor)   

  con.close()
  sendmail(phonenumber,name,calldate)
  CreateHtml()
  init()

def init():
    ser.write(str("ATZ\r\nAT+VCID=1\r\nWaiting for Call\r\n").encode())
def test():
  ser.write(str(TestTxt).encode())

def phone_format(n):                                                                                                                                  
  return format(int(n[:-1]), ",").replace(",", "-") + n[-1]

def mail(email):

  address=email[0]
  host=email[1]
  port=email[2]
  password=email[3]

  con = sqlite3.connect('CallerID.db')

  con.execute("UPDATE `mail` SET `address` = '"+address+"',`host` = '"+host+"' \
  ,`port` = '"+port+"',`password` = '"+password+"' WHERE (`ID` = '1');")

  con.commit()

  con.close()

  print("\nemail address "+address+" configured")
  print("and host "+host)
  print("port "+port)
  print("password: "+password+"\n")


def add(info):

  con = sqlite3.connect('CallerID.db')

  con.execute("INSERT INTO `checknumbers` (`RealName`,`RealNumber`,`Fax`) VALUES \
('"+info[0]+"','"+info[1]+"',0);")

  con.commit()

  con.close()

  print("\n"+info[0]+" with "+info[1]+" added to checknumbers\n")
  

def  LastCall():

    con1 = sqlite3.connect("CallerID.db")

    cur1 = con1.cursor()

    cur1.execute("SELECT * FROM phonecalls ORDER BY ID DESC LIMIT 1")

    rows = cur1.fetchall()    

    for row in rows:
        name=str(row[1])
        phonenumber=str(row[2])

    con1.close()

    text="Appel de "+name+" au "+phonenumber+"\n\n"
    window.plainTextEdit.insertPlainText(text)
    cursor = window.plainTextEdit.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    window.plainTextEdit.setTextCursor(cursor)   


def CreateHtml():
    
    html=""

    con = sqlite3.connect('CallerID.db')

    corsur = con.execute("SELECT * FROM phonecalls ORDER BY ID DESC")
     
    html = "<!DOCTYPE html>"
    html += "<html xmlns =\"http://www.w3.org/1999/xhtml\">"
    html += "<head>"
    html += "<title>CallerID</title>"
    html += "<meta name =\"viewport\" content =\"width=device-width, initial-scale=1\" />"
    html += "<meta http-equiv =\"content-type\" content = \"text/html; charset=utf-8\" />"
    html += "<meta charset =\"utf-8\" />"
    html += "<link href=\"plugins.css\" rel=\"stylesheet\"/>"
    html += "<link href =\"style.css\" rel =\"stylesheet\" />"
    html += "</head>"
    html += "<body>"
    html += "<div class=\"post-item border\">"
    html += "<div class=\"post-item-wrap\">"
    html += "<h1 align =\"center\" ><span lang=\"en-ca\">Calls Received</span></h1>"
    html += "<table border =\"0\" width= \"100%\" height= \"48\">"
    html += "<tr>"
    html += "<td width=\"11%\" height=\"17\" style=\"border-bottom-style: solid\" bgcolor= \"#5D7B9D\">"
    html += "<span lang=\"en-ca\"><font color=\"#FFFFFF\">Date</font></span></td>"
    html += "<td width=\"11%\" height= \"17\" style=\"border-bottom-style: solid\" bgcolor=\"#5D7B9D\">"
    html += "<span lang=\"en-ca\"><font color=\"#FFFFFF\">Number</font></span></td>"
    html += "<td width=\"11%\" height=\"17\" style=\"border-bottom-style: solid\" bgcolor=\"#5D7B9D\">"
    html += "<span lang=\"en-ca\"><font color=\"#FFFFFF\">Name</font></span></td>"
    html += "</tr>"

    DoBkgrnd = True

    for row in corsur:
      name=str(row[1])
      phonenumber=str(row[2])
      calldate=str(row[3])

      if (DoBkgrnd):

         html += "<tr>"
         html += "<td width = \"11%\" height = \"19\" bgcolor = \"#F7F6F3\">" + calldate + "</td>"
         html += "<td width = \"11%\" height = \"19\" bgcolor = \"#F7F6F3\">" + phonenumber + "</td>"
         html += "<td width = \"11%\" height = \"19\" bgcolor = \"#F7F6F3\">" + name + "</td>"
         html += "</tr>"

         DoBkgrnd=False

      else:

          html += "<tr>"
          html += "<td width = \"11%\" height = \"19\">" + calldate + "</td>"
          html += "<td width = \"11%\" height = \"19\">" + phonenumber + "</td>"
          html += "<td width = \"11%\" height = \"19\">" + name + "</td>"
          html += "</tr>"

          DoBkgrnd=True

    html += "</table>"
    html += "</div>"
    html += "</div>"
    html += "</body>"
    html += "</html>"
    
    con.close()

    with open('CallerID.html','w+',encoding='utf-8') as File:
      File.write(html)

    text="""CallerID.html created just click on file to view\n\n"""
    window.plainTextEdit.insertPlainText(text)
    cursor = window.plainTextEdit.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    window.plainTextEdit.setTextCursor(cursor)   


def Help():
   text="""  test -   To test the program
  init -     To initialize the serial port and get ready for calls
  report -   Create an html report file
  add -      Add to checknumbers database
             ex:add John Doe:15147422840 
  email -    Configure email address for email
             email address:host:port:password 
             ex: email info@domain.com:smtp.gmail.com:587:password
  lastcall - Last call received        
  speak -    Speak last call
  quit  -    Quit the program\n\n"""
   window.plainTextEdit.insertPlainText(text) 
   cursor = window.plainTextEdit.textCursor()
   cursor.movePosition(QTextCursor.MoveOperation.End)
   window.plainTextEdit.setTextCursor(cursor)   

def Speak():
   import lastcallspeak
   sys.modules.pop('lastcallspeak')
   LastCall()

def Report():
   import datatkinter
   sys.modules.pop('datatkinter')
   CreateHtml()
          
def CheckCalls(line):
  print(line.find("QUIT"))
  while line.find("QUIT")==-1:
    try:
        line = ser.readline().decode('ascii')
        if line:
          for com in commands:
              if line.find(com+"\r\n")==-1:
                pass
              else:
                pass
                break
    
    # Uncomment the next line to display the input from the serial port in hex format
    #     for x in line: print ("%s") % (x.encode('hex')),
          if line.find("NMBR =")>-1:
            global phonenumber  
            phonenumber=line.replace("NMBR = ","")
            global NMBR
            NMBR = True
          elif NMBR and line.find("NAME =")>-1:
            name=line.replace("NAME = ","")
            phonenumber=phonenumber.strip("\r\n")
            name = name.strip("\r\n")
            name=CheckNumbers(phonenumber,name)
            SaveCall(phonenumber,name)
            NMBR=False

          elif line.find("EMAIL")>-1:
            first=line.split(" ")
            second=first[1].split(":")
            #address
            email[0]=second[0]
            #host
            email[1]=second[1]
            #port
            email[2]=second[2]
            #password
            email[3]=second[3].replace("\r\n","")
            mail(email)

          elif line.find("ADD")>-1:
            first=line.split(" ")
            second=first[2].split(":")
            info[0]=first[1] +" "+ second[0].replace("\r\n","")
            info[1]=second[1].replace("\r\n","")
            add(info)

          elif line.find("INIT")>-1:
            init()

          elif line.find("TEST")>-1:
            test()

          elif line.find("QUIT")>-1:
            pass

          elif line.find("SPEAK")>-1:
            Speak()

          elif line.find("LASTCALL")>-1:
            LastCall()           

          elif line.find("REPORT")>-1:
            Report()            

          elif line.find("HELP")>-1:
            Help()

          line=line.replace("\r\r\n","\r\n")
          if line2 != line and line !="\n":  
            print(line)
            # TextEdit.moveCursor(window,QTextCursor.End)
            window.plainTextEdit.insertPlainText(line)
          else:
            pass
        # last_work_time = now
    except KeyboardInterrupt:
        sys.exit()
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Username or Password are not accepted")
    except Exception as e:
      print(str(e))

    
class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.ico'))
        self.plainTextEdit.installEventFilter(self)
        self.LastCall_Button.clicked.connect(LastCall)
        self.Speak_Button.clicked.connect(Speak)
        self.Report_Button.clicked.connect(Report)
        self.Init_Button.clicked.connect(init)
        self.Help_Button.clicked.connect(Help)

    def eventFilter(self,obj,event):
        global line
        global line2
        if event.type() == QtCore.QEvent.KeyPress and obj is self.plainTextEdit:
            if event.key() == QtCore.Qt.Key_Return and self.plainTextEdit.hasFocus():
                line=line+"\r\n"
                line2=line
                if line.find("QUIT")>-1:
                  sys.exit()
                time.sleep(1)
                ser.write(str(line).encode())
                #print(line,'Enter pressed')
                line=""
            elif int(event.key()) < 256:
                line=line+str(chr(event.key()))
                lg(line)
                print(chr(event.key()))
            elif event.key() == QtCore.Qt.Key_Backspace:
                strlength= len(line)
                line= line[:strlength-1] +  line[strlength+1:]   
        return super().eventFilter(obj, event)

if __name__=="__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app= QApplication(sys.argv)
    
    if (len(scan) == 0):
       dev  = '/dev/ttyUSB*'
       scan = glob.glob(dev)
       if (len(scan) == 0):
           dev  = 'COM*'
           scan = glob.glob(dev)
           if (len(scan) == 0):
                print("Unable to find any ports scanning for /dev/[ttyACM*|ttyUSB*]" + dev) 
                sys.exit()
            
    serport = scan

    if (len(sys.argv) > 1):
            l = len(sys.argv) - 1
            while(l>0):
                if (sys.argv[l][0] == 'C'): serport = sys.argv[l]
                else:                       rate    = sys.argv[l]
                l = l - 1

    if serport == "COM":     
            for n in range(1,20):
                try:
                    serport="COM"+str(n)
                    ser = serial.Serial(port=serport,baudrate=rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
                    print("connected to: " + ser.portstr)
                    s(ser)
                    break
                except:
                    pass
    else:
        ser = serial.Serial(port=serport,baudrate=rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)

    if not os.path.isfile('CallerID.db'):

            con = sqlite3.connect('CallerID.db')

            con.execute('''CREATE TABLE IF NOT EXISTS [checknumbers] (
            [ID] INTEGER PRIMARY KEY, 
            [RealNumber] [CHAR(15)], 
            [RealName] [CHAR(125)], 
            [Fax] BOOLEAN)''')
            con.commit()

            con.execute('''CREATE TABLE IF NOT EXISTS [mail] (
            [ID] INTEGER PRIMARY KEY, 
            [address] [CHAR(125)],
            [host] [CHAR(25)],
            [port] [CHAR(5)],
            [password] [CHAR(125)])''')
            con.commit()

            con.execute('''CREATE TABLE IF NOT EXISTS [phonecalls] (
            [ID] INTEGER PRIMARY KEY, 
            [name] [CHAR(125)], 
            [phonenumber] [CHAR(20)], 
            [calldate] DATETIME, 
            [Fax] BOOLEAN)''')
            con.commit()

            con.execute("""INSERT INTO `checknumbers` (`RealNumber`, `RealName`, `Fax`) VALUES
        ('15147422840', 'RLS Technologies',0);""")
            con.commit()

            con.execute("""INSERT INTO `mail` (`address`,`host`,`port`,'password') VALUES
        ('info@address.com','smtp.gmail.com','587','password');""")
            con.commit()

            con.close()

            os.system("chmod 777 CallerID.db")
           
    init()
    work_thread = threading.Thread(args=(line,),target=CheckCalls)
    work_thread.daemon=True
    work_thread.start()

    window=MainWindow()
    window.setWindowTitle("CallerID")
    #window.plainTextEdit.setPlainText("Hello World")
    window.show()

    sys.exit(app.exec())

