"""keydoc1x.py
 add 'alternate' headwords
 
"""
from __future__ import print_function
import sys, re,codecs
import os

class HWDoc(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  parts = line.split('\t')
  # dochws is list of dictionary headwords defining a document
  #   each headword in dochws is a 'pointer' to the document.
  # docptrs is list of **additional** pointers that 'point to' the
  # document specified by dochws.
  # we allow there to be  no docptrs
  self.dochws = re.split(r'[,:]',parts[0])
  if len(parts) == 1:
   self.docptrs = []
  else:
   self.docptrs = re.split(r'[,:]',parts[1])

def init_hwdoc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWDoc(x) for x in f if not x.startswith(';')]
 print(len(recs),"records from",filein)
 return recs

class Hwextra0(object):
 def __init__(self,line):
  # Each line has two headwords,
  # the 'main' or 'parent' headword and the alternate headword.
  # These two may be separated by space
  line = line.rstrip('\r\n')
  self.k1P,self.k1 = line.split(' ')
 
def init_hwextra(filein):
 if not os.path.exists(filein):
  print('init_hwextra : no such file',filein)
  return []
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = [Hwextra0(line) for line in f if not line.startswith(';')]
 print(len(recs),"records from",filein)
 return recs

def checkx1(xrec,d):
 k1 = xrec.k1
 k1P = xrec.k1P
 if k1P not in d:
  print('addx error: parent headword not found',k1,'parent=',k1P)
  exit(1)
 if k1 not in d:
  # k1 is a new headword for the dictionary
  xrec.use = True
  return
 rec = d[k1]
 dochws = set(rec.dochws)
 k1s = set([k1,k1P])
 if k1s.issubset(dochws):
  xrec.use = False
  return
 xrec.use = True
 print('checkx1 warning: alternate headword already found:',k1,k1P,rec.dochws,rec.docptrs)

def addx(recs,xrecs):
 # modify some rec in recs
 d = {}
 for irec,rec in enumerate(recs):
  for hw in rec.dochws:
   d[hw] = rec
 # check that none of the alternate headwords are present in recs
 # define the 'use' attribute.
 for xrec in xrecs:
  checkx1(xrec,d)
 # add k1P values to docptrs
 for xrec in xrecs:
  if not xrec.use:
   # don't use this
   continue
  k1 = xrec.k1
  k1P = xrec.k1P
  rec = d[k1P]  # would be an error if k1P not in d
  if k1 in rec.dochws:
   print('addx WARNING: hw already in dochws=',k1,rec.dochws,rec.docptrs)
  elif k1 not in rec.docptrs:
   rec.docptrs.append(k1)

def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   doc_str = ','.join(rec.dochws)
   docptrs = rec.docptrs
   #if set(rec.dochws) == set(docptrs):
   if docptrs == []:
    out = doc_str
   else:
    docptrs_str = ','.join(docptrs)
    out = '%s\t%s' %(doc_str,docptrs_str)
   f.write(out + '\n')
 print(len(recs),"records written to",fileout)

if __name__=="__main__": 
 dictlo = sys.argv[1] # xxx
 filein = sys.argv[2] #  keydoc1
 fileinx = sys.argv[3] # alternate headword spellings (xxx_hwextra.txt)
 fileout = sys.argv[4] # 
 recs = init_hwdoc(filein)
 xrecs = init_hwextra(fileinx)
 addx(recs,xrecs)
 write(fileout,recs)
