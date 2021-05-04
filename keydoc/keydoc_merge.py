"""hwnorm1c.py
  An emulation of hwnorm1/sanhw1/hwnorm1c
"""
from __future__ import print_function
import sys, re,codecs
import os
#from hwnorm1c import normalize_key

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
   self.docptrs = []
  else:
   self.docptrs = re.split(r'[,:]',parts[1])
  self.dup = False 

 def __repr__(self):
  x = ','.join(self.dochws)
  s = ''
  if self.docptrs == []:
   return s + x
  else:
   y = s + ','.join(self.docptrs)
   return '%s\t%s' %(x,y)

def init_hwdoc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWDoc(x) for x in f if not x.startswith(';')]
 print(len(recs),"read from",filein)
 d = {}
 for rec in recs:
  #ptrs = rec.dochws + rec.docptrs # 05-02-2021
  ptrs = rec.docptrs
  for hw in ptrs:
   if hw not in d:
    d[hw] = []
   d[hw].append(rec)
 return recs,d

def dicts_containing_hw(drecs):
 """ For any pointer, hw,  in any dictionary,
  d[hw] contains a list of ALL dictionaries having hw as a pointer.
 """
 d = {}
 dictlist = drecs.keys()
 for dictlo in dictlist:
  recs = drecs[dictlo]
  for rec in recs:
   #ptrs = rec.dochws + rec.docptrs  07/12/2020
   ptrs = rec.docptrs
   for hw in ptrs:
    if hw not in d:
     d[hw] = [dictlo]
    elif dictlo not in d[hw]: # 05-02-2021
     #else:
     d[hw].append(dictlo)
 return d

def otherptrs(dictlo,ptrs,hw2dict,dd,dbgword=None):
 ans = []
 dbg = (dbgword in ptrs) 
 dbgans = []
 for hw in ptrs:
  dicts_for_hw = hw2dict[hw]
  for dictlo1 in dicts_for_hw:
   if dictlo1 == dictlo:
    continue
   recs1 = dd[dictlo1][hw]
   for rec1 in recs1:
    #ptrs1 = rec1.dochws + rec1.docptrs 07/12
    #ptrs1 = [] + rec1.docptrs # 05-02-2021
    ptrs1 = rec1.docptrs 
    for hw1 in ptrs1:
     if hw1 not in ptrs:
      if hw1 not in ans:
       ans.append(hw1)
       dbgans.append((dictlo1,hw,hw1))
 #dbg = True
 if dbg and dbgans != []:
  for dictlo1,hw,hw1 in dbgans:
   print('otherptrs dbg:',dictlo,hw,dictlo1,hw1)
 return ans

def merge(drecs,dd):
 hw2dict = dicts_containing_hw(drecs)
 dictlist = drecs.keys()
 for dictlo in dictlist:
  recs = drecs[dictlo]
  #recs = recs[0:11]
  for rec in recs:
   #dochws = rec.dochws # 05-02-2021
   docptrs = rec.docptrs
   #ptrs = dochws + [] # new list
   ptrs = []   # 07/12
   for ptr in docptrs:
    if ptr not in ptrs:
     ptrs.append(ptr)
    else:
     print('warning: duplicate %s %s' %(dictlo,rec))
   ptrs1 = otherptrs(dictlo,ptrs,hw2dict,dd,dbgword=None) # 'mahendra')
   new_docptrs = docptrs + []  # a new list
   for ptr in ptrs1:
    if ptr not in new_docptrs:
     new_docptrs.append(ptr)
   docptrs1 = (docptrs + ptrs1)
   #if set(new_docptrs) != set(docptrs1):
   if new_docptrs != docptrs1:
    print('error 2',dictlo,new_docptrs,' != ',docptrs1)
    exit(1)
   rec.docptrs = new_docptrs

def mergerecs(recs,dbg=False):
 if dbg:
  oldarr = ['.'.join(r.docptrs) for r in recs]
  old = ' + '.join(oldarr)
 newrec = recs[0]
 for rec in recs[1:]:
  rec.dup = True
  for hw in rec.dochws:
   if hw not in newrec.dochws:
    newrec.dochws.append(hw)
  for hw in rec.docptrs:
   if hw not in newrec.docptrs:
    newrec.docptrs.append(hw)
 if dbg: # dbg
  new = '.'.join(newrec.docptrs)
  print('mergerecs old:',old)
  print('          new:',new)

def check(recs,dbg=False):
 """ check if any two docptrs have common members
 """
 #dbg=True
 d = {}
 ndup = 0
 dupnorms = []
 for rec in recs:
  if rec.dup:
   continue
  for norm in rec.docptrs:
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

def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   if rec.dup:
    continue
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

def init_dictlist(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip() for x in f]
 return recs
if __name__=="__main__":
 filein = sys.argv[1]  # dictlist.txt
 dictlist = init_dictlist(filein)
 drecs = {}
 dd = {}
 for dictlo in dictlist:
  filein = "data/%s/keydoc1x_norm1.txt"%dictlo
  if not os.path.exists(filein):
   print('keydoc_merge skipping %s: %s not found' %(dictlo,filein))
   continue
  drecs[dictlo],d = init_hwdoc(filein)
  dd[dictlo] = d
 merge(drecs,dd)
 for dictlo in dictlist:
  recs = drecs[dictlo]
  print('checking %s for merging'%dictlo)
  check(recs)
  fileout = "data/%s/keydoc_merge.txt" %dictlo
  write(fileout,recs)

