"""keydoc_norm.py
 Specify documents from headword list.
  
"""
from __future__ import print_function
import sys, re,codecs
from hwnorm1c import normalize_key
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
  self.normptrs = []  # new attribute
  self.dup = False  
 def normstr(self):
  hwstr = ','.join(self.dochws)
  ptrstr = ','.join(self.normptrs)
  ans = '%s<-%s' %(hwstr,ptrstr)
  return ans

def init_hwdoc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWDoc(x) for x in f if not x.startswith(';')]
 return recs

def normalize_recs(recs):
 for rec in recs:
  docptrs = rec.docptrs
  allptrs = rec.dochws + docptrs
  for key in allptrs:
   norm = normalize_key(key)
   if norm not in rec.normptrs:
    rec.normptrs.append(norm)
 
def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  n = 0
  for rec in recs:
   if rec.dup:
    # This has been merged into another record
    continue
   n = n + 1
   dochws_str = ','.join(rec.dochws)
   normptrs = rec.normptrs
   normptrs_str = ','.join(normptrs)
   out = '%s\t%s' %(dochws_str,normptrs_str)
   f.write(out + '\n')
 print(n,"records written to",fileout)

def init_normrecs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  d = {}
  for line in f:
   line = line.rstrip('\r\n')
   (key,norm) = line.split('\t')
   d[key] = norm
 return d

def mergerecs(recs,dbg=False):
 if dbg:
  oldarr = [r.normstr() for r in recs]
  old = ' + '.join(oldarr)
 newrec = recs[0]
 for rec in recs[1:]:
  rec.dup = True
  for hw in rec.dochws:
   if hw not in newrec.dochws:
    newrec.dochws.append(hw)
  for hw in rec.normptrs:
   if hw not in newrec.normptrs:
    newrec.normptrs.append(hw)
 if dbg: # dbg
  new = newrec.normstr()
  print('mergerecs old:',old)
  print('          new:',new)

def check(recs,dbg=False):
 """ check if any two normptrs have common members
     Recursive
 """
 #dbg=True
 d = {}
 ndup = 0
 dupnorms = []
 for rec in recs:
  if rec.dup:
   continue
  for norm in rec.normptrs:
   if norm in d:
    if dbg: print('check:',norm,'in two documents')
    d[norm].append(rec)
    ndup = ndup + 1
    dupnorms.append(norm)
   else:
    d[norm] = [rec]
 print('check: %s records have common pointer'%ndup)
 for norm in dupnorms:
  mergerecs(d[norm],dbg)
 if ndup != 0:
  check(recs)
if __name__=="__main__": 
 dictlo = sys.argv[1]
 filein = sys.argv[2] #  keydoc1x.txt
 fileout = sys.argv[3] # keydoc1x_norm.txt
 recs = init_hwdoc(filein)
 normalize_recs(recs)
 check(recs,dbg=False)
 write(fileout,recs)
