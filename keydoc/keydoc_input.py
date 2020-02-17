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
 
def make_output(recs):
 """ construct list of (key,doc_str) records from list of HWDoc records
 """
 recsout = []
 for rec in recs:
  doc_str = ','.join(rec.dochws)
  allptrs = rec.dochws + rec.docptrs
  used = [] # to skip duplicates
  for key in allptrs:
   if key in used:
    continue
   used.append(key)
   recout = (key,doc_str)
   recsout.append(recout)
 return recsout

def prev_write(fileout,recs):
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

def write(fileout,recsout):
 with codecs.open(fileout,"w","utf-8") as f:
  nout = 0
  for key,doc_str in recsout:
   out = '%s\t%s' %(key,doc_str)
   f.write(out + '\n')
   nout = nout + 1
 print(nout,"records written to",fileout)

def remove_duplicates(recsout):
 ans = []
 d = {}
 for rec in recsout:
  # rec is a tuple, so we may use as a key
  if rec in d:
   print('skipping duplicate',rec)
  else:
   d[rec]= True
   ans.append(rec)
 return ans

def init_recsout_extra(filein):
 import os
 recsout = []
 if not os.path.isfile(filein):
  print('keydoc_input: file not found',filein)
 else:
  with codecs.open(filein,"r","utf-8") as f:
   recsout = []
   for line in f:
    line = line.rstrip()
    if line.startswith(';'):
     continue # comment
    key,doc_str = line.split('\t')
    recout = (key,doc_str)
    recsout.append(recout)
  print(len(recsout),"keydoc_input records from",filein)
 return recsout

if __name__=="__main__": 
 filein = sys.argv[1] #  keydocx.txt
 filein1 = sys.argv[2] # xxx_keydoc_input.txt
 fileout = sys.argv[3] # keydoc_input.txt
 recs = init_hwdoc(filein)
 recsout = make_output(recs)
 recsout1 = init_recsout_extra(filein1)
 recsout2 = remove_duplicates(recsout + recsout1)
 write(fileout,recsout2)
