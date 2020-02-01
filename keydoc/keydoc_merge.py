"""keydoc_merge.py
  
"""
from __future__ import print_function
import sys, re,codecs
import os
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
 print(len(recs),"read from",filein)
 d = {}
 for rec in recs:
  ptrs = rec.dochws + rec.docptrs
  for hw in ptrs:
   if hw not in d:
    d[hw] = []
   d[hw].append(rec)
 return recs,d



dictlist = re.split(r' +','acc ap90 ben   bhs bop bur cae ' \
 + 'ccs gra gst ieg inm  krm mci md mw mw72 ' \
 + 'pe pgn pui    pw pwg sch shs skd ' \
 + 'snp stc vcp vei wil  yat ap pd')
# dictlist = re.split(r' +','ap90 mw')

def dicts_containing_hw(drecs):
 d = {}
 for dictlo in dictlist:
  recs = drecs[dictlo]
  for rec in recs:
   ptrs = rec.dochws + rec.docptrs
   for hw in ptrs:
    if hw not in d:
     d[hw] = [dictlo]
    else:
     d[hw].append(dictlo)
 return d

def otherptrs(dictlo,ptrs,hw2dict,dd):
 ans = []
 for hw in ptrs:
  dicts_for_hw = hw2dict[hw]
  for dictlo1 in dicts_for_hw:
   if dictlo1 == dictlo:
    continue
   recs1 = dd[dictlo1][hw]
   for rec1 in recs1:
    ptrs1 = rec1.dochws + rec1.docptrs
    for hw1 in ptrs1:
     if hw1 not in ptrs:
      if hw1 not in ans:
       ans.append(hw1)
 return ans

def merge(drecs,dd):
 hw2dict = dicts_containing_hw(drecs)
 for dictlo in dictlist:
  recs = drecs[dictlo]
  #recs = recs[0:11]
  for rec in recs:
   dochws = rec.dochws
   docptrs = rec.docptrs
   ptrs = dochws + docptrs
   ptrs1 = otherptrs(dictlo,ptrs,hw2dict,dd)
   docptrs1 = docptrs + ptrs1
   rec.docptrs = docptrs1

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
 #filein = sys.argv[1] #  keydocx.txt
 #fileout = sys.argv[2] # keydocx_norm.txt
 drecs = {}
 dd = {}
 for dictlo in dictlist:
  filein = "data/%s/keydoc_norm.txt"%dictlo
  if not os.path.exists(filein):
   print('keydoc_merge skipping %s: %s not found' %(dictlo,filein))
   continue
  drecs[dictlo],d = init_hwdoc(filein)
  dd[dictlo] = d
 merge(drecs,dd)
 for dictlo in dictlist:
  recs = drecs[dictlo]
  fileout = "data/%s/keydoc_merge.txt" %dictlo
  write(fileout,recs)

