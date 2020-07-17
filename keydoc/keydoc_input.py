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
  if len(parts) == 1:
   #a = []
   #for x in self.dochws:
   # a.append(x)
   #self.docptrs = a
   self.docptrs = []
  else:
   self.docptrs = re.split(r'[,:]',parts[1])
  self.dup = False

def init_hwdoc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWDoc(x) for x in f if not x.startswith(';')]
 return recs
 
def make_output(recs):
 """ construct list of (key,doc_str) records from list of HWDoc records
  July 13, 2020.  Use only the docptrs (which are normalized).
 """
 recsout = []
 # d is used to check that rec1.docptrs is disjoint from rec2.docptrs.
 d = {} 
 for rec in recs:
  doc_str = ','.join(rec.dochws)
  #allptrs = rec.dochws + rec.docptrs
  allptrs = rec.docptrs
  used = [] # to skip duplicates
  for key in allptrs:
   if key not in d:
    d[key] = [rec]
   else:
    print('keydoc_input: duplicate key',key)
    d[key].append(rec)
   if key in used:
    continue
   used.append(key)
   recout = (key,doc_str)
   recsout.append(recout)
 return recsout,d

def unused_write(fileout,recsout):
 with codecs.open(fileout,"w","utf-8") as f:
  nout = 0
  for key,doc_str in recsout:
   out = '%s\t%s' %(key,doc_str)
   f.write(out + '\n')
   nout = nout + 1
 print(nout,"records written to",fileout)

def unused_remove_duplicates(recsout):
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

def unused_init_recsout_extra(filein):
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

def init_extra(filein):
 import os
 recs = []
 if not os.path.isfile(filein):
  print('keydoc_input: file not found',filein)
  return recs
 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f if not x.startswith(';')]
 for line in lines:
  ptr,hw = re.split('[\t ]',line)
  normptr = normalize_key(ptr)
  normhw  = normalize_key(hw)
  docline = '%s\t%s' % (normhw,normptr)
  rec = HWDoc(docline)
  recs.append(rec)
 print(len(recs),"extra keydoc_input records from",filein)
 return recs

def hw2recd(recs):
 # d[hw] = rec for all hw in rec.docptrs.
 # also check that rec1.docptrs is disjoint from rec2.docptrs for rec1 != rec2
 d = {} 
 for rec in recs:
  doc_str = ','.join(rec.dochws)
  allptrs = rec.docptrs
  for key in allptrs:
   if key not in d:
    d[key] = [rec]
   else:
    print('keydoc_input WARNING (hw2recd): duplicate key',key)
    d[key].append(rec)
 return d

def add_pointers(recs,recs_extra):
 d = hw2recd(recs)
 for ixrec,xrec in enumerate(recs_extra):
  assert len(xrec.dochws) == 1  # Not essential. But reasonable
  hw = xrec.dochws[0]
  xptrs = xrec.docptrs
  if hw not in d:
   # This should not happen.  But we can just WARN
   print('WARNING: extra headword not known:',hw,xptrs)
   continue
  recs0 = d[hw]
  assert len(recs0) == 1
  rec = recs0[0]  # 
  # add the xptrs to rec.docptrs
  newptrs = [x for x in rec.docptrs] # a copy
  for xptr in xptrs:
   if xptr not in newptrs:
    newptrs.append(xptr)
  if True and (ixrec < 5):
   print(ixrec+1,'xrec=',','.join(xrec.dochws),','.join(xrec.docptrs))
   print(ixrec+1,' rec=',','.join(rec.dochws),','.join(rec.docptrs))
   print(ixrec+1,' new=',','.join(newptrs))
  rec.docptrs = newptrs

def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  nout = 0
  for rec in recs:
   doc_str = ','.join(rec.dochws)
   #print('%s\t%s' %(doc_str,','.join(rec.docptrs)))
   for key in rec.docptrs:
    out = '%s\t%s' %(key,doc_str)
    f.write(out + '\n')
    nout = nout + 1
 print(nout,"records written to",fileout)

def writedbg(fileout,recs):
 filedbg = fileout.replace('.txt','_dbg.txt')
 with codecs.open(filedbg,"w","utf-8") as f:
  nout = 0
  for rec in recs:
   doc_str = ','.join(rec.dochws)
   out = '%s\t%s' %(doc_str, ','.join(rec.docptrs))
   f.write(out + '\n')
   nout = nout + 1
 print(nout,"records written to",filedbg)

if __name__=="__main__": 
 filein = sys.argv[1] #  keydocx.txt
 filein1 = sys.argv[2] # xxx_keydoc_input.txt  (may not exist)
 fileout = sys.argv[3] # keydoc_input.txt
 recs = init_hwdoc(filein)

 recs_extra = init_extra(filein1)
 add_pointers(recs,recs_extra)
 #keydoc_merge.check(recs)
 write(fileout,recs)

 exit(1)
