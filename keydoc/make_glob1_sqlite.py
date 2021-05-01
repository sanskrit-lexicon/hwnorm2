""" sqlite.py
   05-01-2021 ejf
   Create keydoc_glob1.sqlite from keydoc_glob1.txt
"""
from __future__ import print_function
import sys,re,codecs;
import sqlite3
import time  # for performance checks
def remove(fileout):
 import os
 if os.path.exists(fileout):
  os.remove(fileout)
  print("removed previous",fileout)

def get_dict_code(fileout):
 # assume fileout is xxx.sqlite
 m = re.search(r'^(.*?)[.]sqlite$',fileout)
 if not m:
  print('sqlite.py ERROR: cannot get dictionary code')
  print('fileout=',fileout)
  exit(1)
 code = m.group(1).lower() # should be lower case?
 print('sqlite.py: dictionary code=',code)
 return code

def create_table(c,conn,tabname):
 template = '''
CREATE TABLE %s (
 key TEXT NOT NULL,
 data TEXT NOT NULL
);
  ''' % tabname
 if False:  #dbg
  print('DBG: table template=')
  print(template)
 c.execute(template)
 conn.commit()

def create_index(c,conn,tabname):
 time0 = time.time()
 sqls = [
  'CREATE INDEX datum on %s(key)',
  'pragma table_info (%s)',
  'select count(*) from %s'
 ]
 for sql in sqls:
  sql1 = sql % tabname
  c.execute(sql1)
  conn.commit()
 time1 = time.time()
 timediff = time1 - time0
 print('create_index takes %0.2f seconds' %timediff)

def insert_batch(c,conn,tabname,rows):
 # rows is a list.
 # if rows is empty, nothing to do
 if len(rows) == 0:
  return
 # 2 columns -> three placeholders (?)
 sql = 'INSERT INTO %s VALUES (?,?)' % tabname
 c.executemany(sql,rows)
 conn.commit()

if __name__ == "__main__":
 time0 = time.time() # a real number

 filein = sys.argv[1]   # xxx.xml
 fileout = sys.argv[2]  # xxx.sqlite
 if len(sys.argv) > 3:
  mbatch = int(sys.argv[3])
 else:
  # default batch size. 
  # experiments with Wilson shows 10000 is about maximal for time.
  # it is also not that big regarding memory.
  mbatch = 10000
 # delete prior version of fileout, if it exists
 remove(fileout) 
 # establish connection to xxx.sqlite, 
 # also creates xxx.sqlite if it doesn't exist
 conn = sqlite3.connect(fileout)
 c = conn.cursor()  # prepare cursor for further use
 # create the 'keydoc_glob1' table in db
 tabname = 'keydoc_glob1';
 create_table(c,conn,tabname)
 
 f = codecs.open(filein,"r","utf-8")
 nlines = 0
 nrow = 0
 batch = []
 for line0 in f:
  nlines = nlines + 1
  line = line0.rstrip('\r\n')
  key,data = line.split('\t')
  row = (key,data)
  if len(batch) < mbatch:
   # add row to batch
   batch.append(row)
   nrow = nrow + 1
  else:
   # insert records of (full) batch, and commit?
   insert_batch(c,conn,tabname,batch)
   # reinit batch
   batch = []
   # add this row to batch
   batch.append(row)
   nrow = nrow + 1
 f.close()
 # insert last batch
 insert_batch(c,conn,tabname,batch)
 # create index
 create_index(c,conn,tabname)
 conn.close()  # close the connection to xxx.sqlite
 time1 = time.time()  # ending time
 print(nlines,'lines read from',filein)
 print(nrow,'rows written to',fileout)
 timediff = time1 - time0 # seconds
 print('%0.2f seconds for batch size %s' %(timediff,mbatch))
