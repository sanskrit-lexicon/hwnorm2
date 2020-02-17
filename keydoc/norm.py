"""norm.py
 compute normalized spellings
  
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

def init_hwdoc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWDoc(x) for x in f if not x.startswith(';')]
 return recs

def normalize_recs(recs):
 normrecs = []
 for rec in recs:
  docptrs = rec.docptrs
  allptrs = rec.dochws + docptrs
  for key in allptrs:
   norm = normalize_key(key)
   if norm != key:
    normrec = (key,norm)
    normrecs.append(normrec)
 return normrecs
 
def write(fileout,normrecs):
 with codecs.open(fileout,"w","utf-8") as f:
  for key,norm in normrecs:
   out = '%s\t%s' %(key,norm)
   f.write(out + '\n')
 print(len(normrecs),"records written to",fileout)

def init_normextra(filein,recs):
 recsout = []
 try:
  with codecs.open(filein,"r","utf-8") as f:
   for line in f:
    if line.startswith(';'):
     continue
    line = line.rstrip()
    key,norm = re.split(r'[: \t]',line)
    recsout.append((key,norm))
 except:
  pass
 print('norm:',len(recsout),'records from',filein)
 return recsout
  
if __name__=="__main__": 
 dictlo = sys.argv[1]
 filein = sys.argv[2] #  keydocx.txt
 filein1 = sys.argv[3] # distinctfiles/xxx_norm
 fileout = sys.argv[4] # norm.txt
 recs = init_hwdoc(filein)
 normrecs = normalize_recs(recs)
 normextra = init_normextra(filein1,recs)
 write(fileout,normrecs+normextra)
