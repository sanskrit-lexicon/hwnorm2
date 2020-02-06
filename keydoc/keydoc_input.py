"""keydoc_input.py
 
"""
from __future__ import print_function
import sys, re,codecs
class HWDoc(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  parts = line.split('\t')
  # dochws is list of dictionary headwords defining a document
  # docptrs is list of pointers (including dochws) that 'point to' the
  # document specified by dochws.
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
 
def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  nout = 0
  for rec in recs:
   doc_str = ','.join(rec.dochws)
   allptrs = rec.dochws + rec.docptrs
   used = [] # to skip duplicates
   for key in allptrs:
    if key in used:
     continue
    used.append(key)
    out = '%s\t%s' %(key,doc_str)
    f.write(out + '\n')
    nout = nout + 1
 print(nout,"records written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  keydocx.txt
 fileout = sys.argv[2] # keydoc_input.txt
 recs = init_hwdoc(filein)
 write(fileout,recs)
