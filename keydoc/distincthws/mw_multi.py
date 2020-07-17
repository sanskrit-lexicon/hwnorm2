"""mw_multi.py
 Specify documents from headword list.
 For mw, take into account the 'ABCE' record types
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline

def extract_keys(filein,dictlo):
 # headwords from xxx.txt
 f = codecs.open(filein,"r","utf-8")
 recs = []
 n = 0 # number of lines read
 nout = 0 # Number of lines written
 for line in f:
  if not line.startswith('<L>'):
   continue
  line = line.rstrip('\r\n')
  d = parseheadline(line)
  if ('L' in d) and ('k1' in d):
   L = d['L']
   key = d['k1']
  else:
   print('extract_keys_error (L)',line)
   exit(1)
  if ('e' in d) and (dictlo not in ['cae','pw']):
   e =  d['e']
   cat = 'H' +e
  else:
   cat = 'H1'
  n = n + 1
  # Remove unacceptable characters -- none are expected
  if re.search(r'[^a-zA-Z0-9,.|~]',key):
   key1 = re.sub(r'[^a-zA-Z0-9,.|~]','',key)
   print("WARNING: Unknown Characters in key",key," => ",key1)
   key = key1
  rec = (key,cat,L)
  recs.append(rec)
 print('extract_keys:',n,"records in",filein)
 return recs

def extract_keys_a(recsin):
 # state variables
 d = {} 
 e = {}
 key0 = ''  # previous key
 n = 0
 keyarr = []  # keys in order of entrance into d
 for key,hcode,lnum in recs:
  n = n + 1
  #if n > 100:
  # break   
  if key0 == '':
   d[key] = [key]
   keyarr.append(key)
   key0 = key
   if not re.search(r'[1-4]$',hcode): # validity check on first record
    print('extract_keys_a WARNING: unexpected hcode=',key,hcode,lnum)
   continue
  if re.search(r'[ABCE]$',hcode):
   if key not in d[key0]:
    d[key0].append(key)
    if key not in d:
     d[key] = d[key0]
   continue
  if not re.search(r'[1-4]$',hcode): # validity check 
   print('extract_keys_a WARNING: unexpected hcode=',key,hcode,lnum)
  if key not in d:
   d[key] = [key]
   key0 = key
   keyarr.append(key)
  else:
   key0 = key
 return d,keyarr

def extract_keys_b(d0,keyarr0):
 emptyset = set()
 multikey = [k for k in keyarr0 if len(d0[k])>1]
 d = {}
 for i1,k1 in enumerate(multikey):
  if d0[k1] == []:
   continue
  keys = set(d0[k1])
  found = False
  for i2,k2 in enumerate(multikey):
   if i2<=i1:
    continue
   keys2 = set(d0[k2])
   isect = keys.intersection(keys2)
   if isect != emptyset:
    keys = keys.union(keys2)
    #print('merging',k2,d0[k2],'into',k1,d0[k1],'yields',keys)
    d0[k2] = []
    d0[k1] = []
    found = True
  for k in keys:
   if (k != k1) and (k in d0) and (len(d0[k]) == 1):
    d0[k] = []
  if found:
   d[k1] = list(keys)
   #print('changing',k1,d0[k1],'to',d[k1]) 
 keyarr = []
 for k in keyarr0:
  if d0[k] != []:
   d[k] = d0[k]
   keyarr.append(k)
  elif k in d:
   #print('dropping key',k)
   keyarr.append(k)   
  else:
   #print('Dropping singleton key',k)
   pass
 return d,keyarr
  
def write(fileout,d,keyarr):
 with codecs.open(fileout,"w","utf-8") as f:
  nmulti = 0
  for key in keyarr:
   doclist = d[key]
   doclist = sorted(doclist)  # arbitrary -- not required
   out = ','.join(doclist)
   if len(doclist) > 1:
    f.write(out + '\n')
    nmulti = nmulti + 1
 print('keydoc1:',nmulti,"records written to",fileout)

if __name__=="__main__": 
 dictlo = sys.argv[1] # xxx
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[3] # extract_keys_a.txt
 recs = extract_keys(filein,dictlo)
 d0,keyarr0 = extract_keys_a(recs)
 d,keyarr = extract_keys_b(d0,keyarr0)
 write(fileout,d,keyarr)
