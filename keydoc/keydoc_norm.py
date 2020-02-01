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

def init_hwdoc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWDoc(x) for x in f if not x.startswith(';')]
 return recs

def normalize_recs(recs,normd):
 for rec in recs:
  docptrs = rec.docptrs
  allptrs = rec.dochws + docptrs
  for key in allptrs:
   if key in normd:
    norm = normd[key]
    if norm not in allptrs:
     rec.docptrs.append(norm)
 
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

def init_normrecs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  d = {}
  for line in f:
   line = line.rstrip('\r\n')
   (key,norm) = line.split('\t')
   d[key] = norm
 return d
if __name__=="__main__": 
 dictlo = sys.argv[1]
 filein = sys.argv[2] #  keydocx.txt
 filein1 = sys.argv[3] # norm recs
 fileout = sys.argv[4] # keydocx_norm.txt
 recs = init_hwdoc(filein)
 normd = init_normrecs(filein1)
 normalize_recs(recs,normd)
 write(fileout,recs)
