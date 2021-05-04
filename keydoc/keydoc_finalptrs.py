"""keydoc_finalptrs.py
 
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
   self.docptrs = []
  else:
   self.docptrs = re.split(r'[,:]',parts[1])
  self.dup = False

def init_hwdoc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWDoc(x) for x in f if not x.startswith(';')]
 return recs
 
def init_extra(filein):
 import os
 recs = []
 if not os.path.isfile(filein):
  print('keydoc_finalptrs: file not found',filein)
  return recs
 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f if not x.startswith(';')]
 for iline,line in enumerate(lines):
  try:
   hw,ptrstr = re.split('[\t]',line)
  except:
   print('format error in line',iline+1,'of',filein)
   print(line)
   exit(1)
  ptrs = ptrstr.split(',')
  normptrs = [normalize_key(ptr) for ptr in ptrs]
  normptrstr = ','.join(normptrs)
  normhw  = normalize_key(hw)
  docline = '%s\t%s' % (normhw,normptrstr)
  rec = HWDoc(docline)
  recs.append(rec)
 print(len(recs),"extra keydoc_input records from",filein)
 return recs

def hw2recd(recs):
 # return d, a Python dictionary whose keys are
 #  all X for which there is rec in recs with X in rec.docptrs.
 # and d[X] is the list of all rec in recs for which X is in rec.docptrs.
 d = {} 
 for rec in recs:
  #doc_str = ','.join(rec.dochws)
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
 nprob = 0
 for ixrec,xrec in enumerate(recs_extra):
  assert len(xrec.dochws) == 1  # Not essential. But reasonable
  hw = xrec.dochws[0]
  xptrs = xrec.docptrs
  if hw not in d:
   # This should not happen.  But we can just WARN
   print('WARNING: extra headword not known:"%s"'%hw,xptrs[0])
   nprob = nprob + 1
   continue
  recs0 = d[hw]
  assert len(recs0) == 1
  rec = recs0[0]  # 
  # add the xptrs to rec.docptrs
  newptrs = [x for x in rec.docptrs] # a copy
  for xptr in xptrs:
   if xptr not in newptrs:
    newptrs.append(xptr)
  if False and (ixrec < 5):
   print(ixrec+1,'xrec=',','.join(xrec.dochws),','.join(xrec.docptrs))
   print(ixrec+1,' rec=',','.join(rec.dochws),','.join(rec.docptrs))
   print(ixrec+1,' new=',','.join(newptrs))
  rec.docptrs = newptrs
 print(nprob,'add_pointers headword problems')

def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  nout = 0
  for rec in recs:
   doc_str = ','.join(rec.dochws)
   ptrs_str = ','.join(rec.docptrs)
   out = '%s\t%s' %(doc_str,ptrs_str)
   f.write(out + '\n')
   nout = nout + 1
 print(nout,"records written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  keydoc_merge.txt
 filein1 = sys.argv[2] # xxx_keydoc_ptrs.txt  (may not exist)
 fileout = sys.argv[3] # keydoc_final.txt
 recs = init_hwdoc(filein)
 print(len(recs),"records read from",filein)
 recs_extra = init_extra(filein1)
 add_pointers(recs,recs_extra)
 write(fileout,recs)
