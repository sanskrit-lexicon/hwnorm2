"""hws.py
 extract distinct headwords from one dictionary digitization file.
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline

def extract_keys(filein,dictlo):
 # headwords from xxx.txt
 f = codecs.open(filein,"r","utf-8")
 recs = []
 dkeys = {}
 n = 0 # number of lines read
 nout = 0 # Number of lines written
 for line in f:
  if not line.startswith('<L>'):
   continue
  line = line.rstrip('\r\n')
  d = parseheadline(line)
  key = d['k1']
  n = n + 1
  # Remove unacceptable characters -- none are expected
  if re.search(r'[^a-zA-Z0-9,.|~]',key):
   key1 = re.sub(r'[^a-zA-Z0-9,.|~]','',key)
   print("WARNING: Unknown Characters in key",key," => ",key1)
   key = key1
  if key in dkeys:
   continue ## key is a duplicate
  dkeys[key]=True
  rec = key
  recs.append(rec)
 print('extract_keys:',n,"records in",filein)
 return recs
 
def write(fileout,keyarr):
 with codecs.open(fileout,"w","utf-8") as f:
  nmulti = 0
  for key in keyarr:
   f.write(key + '\n')
 print('keydoc1:',len(keyarr),"records written to",fileout)

if __name__=="__main__": 
 dictlo = sys.argv[1] # xxx
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[3] # extract_keys_a.txt
 keys = extract_keys(filein,dictlo)
 write(fileout,keys)
