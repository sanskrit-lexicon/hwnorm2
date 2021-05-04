"""keydoc_input.py
 
"""
from __future__ import print_function
import sys, re,codecs
from hwnorm1c import normalize_key
class HWDoc(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  parts = line.split('\t')
  # dochws is list of dictionary headwords defining a document
  # docptrs is list of pointers (including dochws) that 'point to' the
  # document specified by dochws.
  self.dochws = re.split(r'[,:]',parts[0])
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
   for key in rec.docptrs:
    out = '%s\t%s' %(key,doc_str)
    f.write(out + '\n')
    nout = nout + 1
 print(nout,"records written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  keydoc_final.txt
 fileout = sys.argv[2] # keydoc_input.txt
 recs = init_hwdoc(filein)
 write(fileout,recs)
