""" get_sqlite.py
   03-14-2026 ejf
   access keydoc_glob1.sqlite for a given input
   usage: python get_sqlite.py slp1
"""
from __future__ import print_function
import sys,re,codecs;
import sqlite3
from hwnorm1c import normalize_key
if __name__ == "__main__":
 key = sys.argv[1]
 sqlitefile = 'keydoc_glob1.sqlite'
 conn = sqlite3.connect(sqlitefile) # open connection
 cursor = conn.cursor()  # prepare cursor for further use
 tabname = 'keydoc_glob1';
 # "select * from {$this->dict} where key='$key'";
 #query = f"SELECT data from {tabname} WHERE key='{key}'"
 normkey = normalize_key(key)
 query = f"SELECT * from {tabname} WHERE key='{normkey}'"
 cursor.execute(query)
 rows = cursor.fetchall()
 nrows = len(rows)
 print(f'nrows = {nrows}')
 for row in rows:
  print(f'row = {row}')
 conn.close()  # close the connection
