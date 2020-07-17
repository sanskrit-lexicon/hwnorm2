"""keydoc1.py
 Specify documents from headword list,
 Using precomputed :
  a) list of distinct headwords
  b) list of multi-headword documents 
"""
from __future__ import print_function
import sys, re,codecs

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
  self.used = True

def extract_hws(filein,dictlo):
 # distinct headwords are one per line
 # Allow ; comments in filein
 with codecs.open(filein,"r","utf-8") as f:
  hws = [HWDoc(x) for x in f if not x.startswith(';')]
 n = len(hws)
 print('extract_hws:',n,"records in",filein)
 return hws

def extract_multihws(filein,dictlo):
 # each line contains more than one headword, separated by comma
 # if filein doesn't exist, return empty list
 import os
 if not os.path.exists(filein):
  print('no multihws: no such file',filein)
  return []
 with codecs.open(filein,"r","utf-8") as f:
  multihws = [x.rstrip('\r\n').split(',') for x in f if not x.startswith(';')]
 n = len(multihws)
 print('extract_multihws:',n,"records in",filein)
 return multihws

def write(fileout,docs):
 with codecs.open(fileout,"w","utf-8") as f:
  nmulti = 0
  for doc in docs:
   doclist = doc.dochws
   doclist = sorted(doclist)  # temporary
   out = ','.join(doclist)
   f.write(out + '\n')
   if len(doclist) > 1:
    nmulti = nmulti + 1
 print('keydoc1:',len(docs),"records written to",fileout)
 print('keydoc1:',nmulti,"documents have multiple headwords")

def insert_multihws(hwrecs,multihws):
 d = {}
 for ihwrec,hwrec in enumerate(hwrecs):
  hw = hwrec.dochws[0]  # at this point, hwrec has just one headword
  d[hw] = ihwrec #[hw]

 for multihw in multihws:
  # multihw is a list of headwords
  if len(multihw) == 1:  # error
   print('insert_multihws ERROR. Expect hw list',multihw)
   exit(1)
  #### This logic assumes:
  ## the FIRST word of multihw is unique among the various multihws
  ## If A,B and A,C are two or more multihw with same first word, 
  ## then replace them with A,B,C.  This has been done in multisimplify
  for ihw,hw in enumerate(multihw):
   ihwrec = d[hw]
   hwrec = hwrecs[ihwrec]
   if ihw == 0:
    hwrec.dochws = multihw
    hwrec.used = True
   elif len(hwrec.dochws) == 1:
    hwrec.used = False
 docs = [hwrec for hwrec in hwrecs if hwrec.used]
 return docs

def check_disjoint(docs):
 d = {}
 for doc in docs:
  # doc is a list of hws
  for hw in doc:
   if hw in d:
    print('non-disjoint:',d[hw],doc)
  for hw in doc:
   d[hw] = doc

def unused_mergerecs_helper(recs,dbg=False):
 oldarr = [(','.join(r.dochws) + '%s'%r.used) for r in recs]
 old = ' + '.join(oldarr)
 newrec = recs[0]
 for rec in recs[1:]:
  if not rec.used:
   # example in acc
   # advEtAnanda,advayAnanda   and advayAnanda,advEtAnanda
   continue
  rec.used = False
  if hwchk in rec.dochws:
   print('mergerecs_helper: dropped rec',rec.dochws)
  for hw in rec.dochws:
   if hw not in newrec.dochws:
    newrec.dochws.append(hw)
  #for hw in rec.normptrs:
  # if hw not in newrec.normptrs:
  #  newrec.normptrs.append(hw)
 if dbg: # dbg
  new = ','.join(newrec.dochws)
  print('mergerecs old:',old)
  print('          new:',new)

def unused_mergerecs(recs,dbg=False):
 """ check if any two dochws have common members
 """
 d = {}
 ndup = 0
 duphws = []
 duprecs = []
 for rec in recs:
  for hw in rec.dochws:
   if hw in d:
    if dbg: print('check:',hw,'in two documents')
    d[hw].append(rec)
    ndup = ndup + 1
    duphws.append(hw)
   else:
    d[hw] = [rec]
 print('check: %s records have common headwords'%ndup)
 duprecs = []
 for hw in duphws:
  for rec in d[hw]:
   if rec not in duprecs:
    duprecs.append(rec)
 print(len(duprecs),"count of duprecs")
 mrecs = []
 for irec,rec in enumerate(duprecs):
  if not rec.used:
   continue
  hws = [hw for hw in rec.dochws]
  while True:
   nhws = len(hws)
   duprecs1= duprecs[irec+1:]
   for rec1 in duprecs1:
    common = [] # hws in rec1.dochws and in hws
    new = []    # hws in rec1.dowhws but not in hws
    if not rec.used:
     continue
    for hw in rec1.dochws:
     if hw in hws:  # rec1 intersects
      common.append(hw)
     else:
      new.append(hw)
    if common == rec1.dochws:
     # mark rec1 as not used -- it adds nothing to hws
     rec1.used = False
     if hwchk in rec1.dochws:print('mergerecs dropped 1',rec1.dochws)
     continue
    if common == []:
     # no commonality between rec1.dochws and hws
     continue
    # new must be non-empty, as well as common
    # Update hws
    hws = hws + new
    # We have used up rec1
    rec1.used = False
    if hwchk in rec1.dochws:print('mergerecs dropped 1',rec1.dochws)
   if len(hws) == nhws:
    # nothing found in this iteration of duprecs1 loop.
    break  # break while True 
   # update rec.dochws
   rec.dochws = hws

class MultiWrapper(object):
 def __init__(self,obj):
  self.obj = obj
  self.empty = False
  self.eqclass = set([s for s in obj])

def multisimplify(arrs):
 """ arrs is a list of lists.
   For arr in arrs, any two elements of arr are 'equivalent', by assumption.
   Let S denote the set of all elements.  Let there be an equivalence 
   relation on S; for two elements 'a' and 'b' of S, write a ~ b if the two
   elements are equivalent.
   This routine then returns the the partition of S into equivalence classes.
 """
 emptyset = set()
 barrs = [MultiWrapper(arr) for arr in arrs]
 for i1,barr in enumerate(barrs):
  if barr.empty:
   continue
  # Make a copy of the elements of barr
  #eqclass = barr.eqclass
  while True:
   extendedFlag = False
   for barr1 in barrs[i1+1:]:
    if (not barr1.empty) and (barr.eqclass.intersection(barr1.eqclass) != emptyset):
     barr.eqclass = barr.eqclass.union(barr1.eqclass)
     barr1.empty = True
     extendedFlag = True
   if not extendedFlag:
    break  # leave the while True loop
 ans = [list(barr.eqclass) for barr in barrs if not barr.empty]
 return ans
 if False:  # dbg
  for i,barr in enumerate(barrs):
   barstr = ','.join(barr.obj)
   print(i,barstr,barr.empty,barr.eqclass)
  exit(1)
def test():
 text = """
nAmaliNgAnuSAsana,amarakoSa
trikARqa,amarakoSa
nAmaliNgAnuSAsana,aBiDAnatantra
advEtAnanda,advayAnanda
advayAnanda,advEtAnanda
"""
 lines = text.splitlines()
 multihws = []
 for line in lines:
  line = line.strip()
  if ',' in line:
   multihw = line.split(',')
   multihws.append(multihw)
 multihws1 = multisimplify(multihws)
 for multihw in multihws1:
  print(','.join(multihw))
 exit()
if __name__=="__main__": 
 #test()
 dictlo = sys.argv[1] # xxx
 filein = sys.argv[2] #  list of distinct headwords
 filein1 = sys.argv[3] # list of multi-hw documents; file may not exist
 fileout = sys.argv[4] # 
 hwrecs = extract_hws(filein,dictlo)
 multihws0 = extract_multihws(filein1,dictlo)
 multihws = multisimplify(multihws0)
 docs = insert_multihws(hwrecs,multihws)
 write(fileout,docs)
