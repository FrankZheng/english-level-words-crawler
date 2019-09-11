
import json
import sys
import sqlite3

create_words_sql = '''
    CREATE TABLE IF NOT EXISTS words(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      level INTEGER,
      word TEXT,
      explain TEXT,
      example TEXT,
      sound_mark TEXT) 
'''

def load_json(file_path):
    file = open(file_path, 'r')
    data = file.read()
    return json.loads(data)

def dump_db(words, db_path):
    #connect db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    #create table
    cursor.execute(create_words_sql)
    #insert data
    for word in words:
        insert = '''
        insert into words(level, word, explain, example, sound_mark) 
        values(?, ?, ?, ?, ?)''' 
        cursor.execute(insert, (word['level'], word['word'], word['explaination'], word['examples'], word['soundmark']))
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    words = load_json('./level_words.json')
    dump_db(words, './words.db')
    