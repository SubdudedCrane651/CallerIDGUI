# to speech conversion
from email.mime import audio
import sys
# sys.path.append("c:\users\rchrd\appdata\local\packages\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\localcache\local-packages\python39\site-packages")
from gtts import gTTS, tts
#pip install playsound==1.2.2
#from playsound import playsound
import pygame
import sqlite3
import time
# This module is imported so that we can
# play the converted audio
import os
import json
import mysql.connector
import time


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

# Saving the converted audio in a mp3 file named
# welcome
audio_file = "call.mp3"
  # Remove old file if it exists and is not locked
# Remove old file if it exists

# Generate new audio
if mytext !="":
  myobj = gTTS(text=mytext, lang=language, slow=False)
  time.sleep(0.10)  # Wait a bit before trying again
  myobj.save(audio_file)  

  # Play audio
  pygame.mixer.init()
  pygame.mixer.music.load(audio_file)
  pygame.mixer.music.play()
  # Wait for playback to finish
  while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # RELEASE THE FILE LOCK
  pygame.mixer.music.stop()
  pygame.mixer.quit()

    # Now safe to delete
  for _ in range(20):
        try:
            os.remove(audio_file)
            break
        except PermissionError:
            time.sleep(0.1)

