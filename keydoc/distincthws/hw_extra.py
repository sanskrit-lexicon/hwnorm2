"""hw_extra.py
 add 'alternate' headwords from csl-orig/v02/xxx/xxx_hwextra.txt
 Also, initialize multidocs
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
import os

def init_hws(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip('\r\n') for x in f if not x.startswith(';')]
 print(len(recs),"records from",filein)
 return recs

def unused_init_multihws(filein):
 if not os.path.exists(filein):
  return []
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip('\r\n').split(',') for x in f if not x.startswith(';')]
 print(len(recs),"records from",filein)
 return recs

class Hwextra0(object):
 def __init__(self,line):
  self.line = line.rstrip('\r\n')
  d = parseheadline(self.line)
  try:
   self.k1 = d['k1']  # the alternate
   self.k1P = d['k1P'] # the 'parent'
  except:
   print('Hwextra0 parse error', self.line)
   exit(1)
  self.multi=False

def init_hwextra(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = [Hwextra0(line) for line in f if not line.startswith(';')]
 print(len(recs),"records from",filein)
 return recs

def addx(recs,xrecs):
 # modify some rec in recs
 d = {}
 for rec in recs:
  for hw in rec.dochws:
   d[hw] = rec
 #
 for xrec in xrecs:
  k1 = xrec.d['k1']
  k1P = xrec.d['k1P']
  if k1P not in d:
   print('keydoc1x addx error: %s not a headword'%k1P)
  else:
   rec = d[k1P]  # would be an error if k1P not in d
   if k1 not in rec.docptrs:
    rec.docptrs.append(k1)

def mark_multi(xrecs,hws):
 d = {}
 for hw in hws:
  d[hw] = True
 for xrec in xrecs:
  k1P = xrec.k1P
  k1 = xrec.k1
  if k1P not in d:
   print('ERROR: parent headword not found',k1P, '(alternate = %s)'%k1)
   exit(1)
  if (xrec.k1 in d):
   xrec.multi = True
   #print('mark_multi:',xrec.k1,xrec.k1P)
   
def write(fileout,filemulti,xrecs):
 # d is for checking the 'k1P' parent
 n = 0
 f = codecs.open(fileout,"w","utf-8")
 f1 = codecs.open(filemulti,"w","utf-8")
 nmulti = 0
 for xrec in xrecs:
  k1P = xrec.k1P
  k1 = xrec.k1
  if xrec.multi:
   nmulti = nmulti + 1
   out = '; %s %s' %(k1P,k1)
   f.write(out + '\n')
   out = '%s,%s' %(k1P,k1)
   f1.write(out + '\n')
  else:
   out = '%s %s' %(k1P,k1)
   f.write(out + '\n')
  n = n + 1
 f.close()
 f1.close()
 print(n,"records written to",fileout)
 print(nmulti,"written to",filemulti)

if __name__=="__main__": 
 dictlo = sys.argv[1] # xxx
 filein = sys.argv[2] #  alternate headword spellings (xxx_hwextra.txt)
 fileinx = sys.argv[3] # distinct headwords for xxx
 fileout = sys.argv[4] # 
 filemulti = sys.argv[5]  # multiple headwords, if any
 xrecs = init_hwextra(fileinx)
 if len(xrecs) == 0:
  if os.path.exists(fileout):
   os.remove(fileout)
  if os.path.exists(filemulti):
   os.remove(filemulti)
 else:
  hws = init_hws(filein)
  #multihws = init_multihws(filemulti)
  mark_multi(xrecs,hws)
  write(fileout,filemulti,xrecs)
