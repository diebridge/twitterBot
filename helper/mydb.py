import sqlite3
import os
from pathlib import Path

db = sqlite3.connect(f'{Path(__file__).parent.parent}/files/tweets.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS MyTable3(id INTEGER PRIMARY KEY, keyword TEXT, name TEXT, geo TEXT, image TEXT, source TEXT, timestamp TEXT, text TEXT UNIQUE, rt INTEGER)''')
db.commit()