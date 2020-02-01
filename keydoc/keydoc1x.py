"""keydoc1alt.py
 add 'alternate' headwords from
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline

class HWDoc(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  parts = line.split('\t')
  # dochws is list of dictionary headwords defining a document
  #   each headword in dochws is a 'pointer' to the document.
  # docptrs is list of **additional** pointers that 'point to' the
  # document specified by dochws.
  #
  self.dochws = re.split(r'[,:]',parts[0])
  if len(parts) == 1:
   #a = []
   #for x in self.dochws:
   # a.append(x)
   #self.docptrs = a
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
  line = line.rstrip('\r\n')
  d = parseheadline(line)
  self.d = d  
 
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
   print('keydoc1x addx error: %s not a headwords'%k1P)
  else:
   rec = d[k1P]  # would be an error if k1P not in d
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
 #d0,keyarr0 = extract_keys_a(recs)
 #d,keyarr = extract_keys_b(d0,keyarr0)
 write(fileout,recs)
