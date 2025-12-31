# to speech conversion
from email.mime import audio
import sys
# sys.path.append("c:\users\rchrd\appdata\local\packages\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\localcache\local-packages\python39\site-packages")
from gtts import gTTS
#pip install playsound==1.2.2
from playsound import playsound
import sqlite3
import time
# This module is imported so that we can
# play the converted audio
import os
import json
import mysql.connector

# The text that you want to convert to audio
mytext=""
name=""
phonenumber=""

def load_mysql_config(path="config.json"):
    with open(path, "r") as file:
        data = json.load(file)
        return data["mysql"]

# Load MySQL config from JSON
config = load_mysql_config()

if config["host"] == "SQLite":
      SQLite=True
else:
      SQLite=False  

if SQLite:
    
          con = sqlite3.connect('CallerID.db')

          corsur = con.execute("SELECT * FROM phonecalls ORDER BY ID DESC LIMIT 1")

          for row in corsur:
            name = str(row[1])
            phonenumber = str(row[2])
            dateandtime = str(row[3])

else:        

            # Connect to MySQL
            con1 = mysql.connector.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                port=config.get("port", 3306)
            )

            cur1 = con1.cursor()
            cur1.execute("SELECT * FROM phonecalls ORDER BY ID DESC LIMIT 1")
            row = cur1.fetchone()  

name = phonenumber = dateandtime = ""

if row:
  if SQLite:
     name=str(row[1])
     phonenumber=str(row[2])
     datetime=str(row[3])
  else:
     name=str(row[2])
     phonenumber=str(row[1])
     datetime=str(row[3])  

if SQLite:
      con.close()
else:
      con1.close() 
#mytext = "Call from "+name+" at "+phonenumber
mytext = "Appel de "+name+" au "+phonenumber
# Language in which you want to convert
language = 'fr'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
if mytext !="":
  myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome
  audio_file = "call.mp3"
  try:
    os.remove(audio_file)
  except:
    pass
  myobj.save(audio_file)
# Playing the converted file
  # audio_file = os.path.dirname(__file__) + "\call.mp3"
  playsound(audio_file,True)