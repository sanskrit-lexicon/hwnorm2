"""keydoc1.py
 Specify documents from headword list.
 For mw, take into account the 'ABCE' record types
 
"""
from __future__ import print_function
import sys, re,codecs

class HWDoc(object):
 count=0
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
  # for extract_keys_a
  self.status = 'orig'
  HWDoc.count = HWDoc.count + 1
  self.count = HWDoc.count

 def __repr__(self):
  x = ','.join(self.dochws)
  #s = self.status + '\t'
  s = ''
  #s = '(Record #%06d) '%self.count
  if self.docptrs == []:
   return s + x
  else:
   y = s + ','.join(self.docptrs)
   return '%s\t%s' %(x,y)

def init_hwdoc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWDoc(x) for x in f if not x.startswith(';')]
 return recs

def list_union_unique(a):
 """ a is a list of lists
  return a list of the unique items in all the lists of a
 """
 ans = []
 for x in a:
  for y in x:
   if y not in ans:
    ans.append(y)
 return ans

itest = 0
def maximal_doc(recs):
 global itest # ref https://python-textbok.readthedocs.io/en/1.0/Variables_and_Scope.html
 
 recs1 = sorted(recs,key = lambda rec: len(rec.dochws), reverse=True)
 rec_max = recs1[0]
 # verify that rec_max is maximal in that set(rec_max.dochws)
 # is a subset of set(rec.dochws) for all rec in recs
 rec_max_set = set(rec_max.dochws)
 nonsubsets = [rec for rec in recs if not rec_max_set.issubset(set(rec.dochws))]
 if nonsubsets != 0:
  itest = itest + 1
  if itest <= 5:
   for rec in nonsubsets:
    print('%s is not a subset of %s'%(rec_max.dochws,rec.dochws))
  
 return rec_max
itest_c1 = 0
itext_c1_max = -1  # skip tests
def extract_keys_c3(recsin):
 """  This gives same result as extract_keys_c1, _c2  but is many
  times faster.  (1 sect vs. 2 min vs 20+min)
  consider two records A and B
  A1 = sequence of distinct key1 values that define the document for A
  A2 = additional normalized spellings of any key1 values, if any
  B1 = defining key1 values for document for B
  B2 = additional normalized spellings, if any
  We can assume that A1 and B1 have no key1 in common.
  However, if might be that A1 and B2 have some value in common;
  Example for SKD:
  A = 'a:None'  b = 'aH:a'
  In this case, we want to:
   - delete both records A and B
   - include a record 'C'  so that C = 'a,aH:None'
  Here is another hypothetical example:
  A = 'a1,a2:a3,a4',  B = 'b1,b2:a3,b4'
  Then
   C = 'a1,a2,b1,b2:a3,a4,b4
 """
 e = {}
 ehws = []
 for rec in recsin:
  ptrs = rec.dochws + rec.docptrs
  for hw in ptrs:
   if hw not in e:
    e[hw] = []
    ehws.append(hw)
   e[hw].append(rec)

 recsout = []
 for hw in ehws:
  recs = [r for r in e[hw] if e[hw] != []]
  if hw in ['narahari','narendra']:
   print('chk2a',hw,recs)
  if recs == []:
   continue
  dochws = list_union_unique([r.dochws for r in recs])
  docptrs = list_union_unique([r.docptrs for r in recs])
  docall = list_union_unique([dochws,docptrs])
  for hw1 in docall:
   recs1 = [r for r in e[hw1] if e[hw1] != []]
   #if hw1 in ['narahari','narendra']:
   # print('chk3:',hw,hw1,recs1)
   dochws1 = list_union_unique([r.dochws for r in recs1])
   docptrs1 = list_union_unique([r.docptrs for r in recs1])
   docall1 = dochws1 + docptrs1
   if ('narahari' in docall1) or ('narendra' in docall1):
    print('chk4:',hw,hw1)
    print('   dochws1=',dochws1)
    print('   docptrs1=',docptrs1)
   dochws = list_union_unique([dochws,dochws1])
   docptrs = list_union_unique([docptrs,docptrs1])
  rec = e[hw][0]
  rec.dochws = dochws
  rec.docptrs = docptrs
  recsout.append(rec)
  docall = dochws + docptrs
  for hw1 in docall:
   e[hw1] = []
 return recsout

def related_recs(hw,e):
 recs = e[hw]
 while True:
  dochws = list_union_unique([r.dochws for r in recs])
  docptrs = list_union_unique([r.docptrs for r in recs])
  docall = list_union_unique([dochws,docptrs])
  newrecs=[]
  for hw1 in docall:
   for r in e[hw1]:
    if r not in recs:
     if r not in newrecs:
      newrecs.append(r)
  if newrecs == []:
   return recs
  recs = recs + newrecs  # continue with while loop
 
def extract_keys_c4(recsin):
 """  This gives same result as extract_keys_c1, _c2  but is many
  times faster.  (1 sect vs. 2 min vs 20+min)
  consider two records A and B
  A1 = sequence of distinct key1 values that define the document for A
  A2 = additional normalized spellings of any key1 values, if any
  B1 = defining key1 values for document for B
  B2 = additional normalized spellings, if any
  We can assume that A1 and B1 have no key1 in common.
  However, if might be that A1 and B2 have some value in common;
  Example for SKD:
  A = 'a:None'  b = 'aH:a'
  In this case, we want to:
   - delete both records A and B
   - include a record 'C'  so that C = 'a,aH:None'
  Here is another hypothetical example:
  A = 'a1,a2:a3,a4',  B = 'b1,b2:a3,b4'
  Then
   C = 'a1,a2,b1,b2:a3,a4,b4
 """
 e = {}
 ehws = []
 for rec in recsin:
  ptrs = rec.dochws + rec.docptrs
  for hw in ptrs:
   if hw not in e:
    e[hw] = []
    ehws.append(hw)
   e[hw].append(rec)
 if False:
  for hw in ['narendra','narahari']:
   print('debug: records related to',hw)
   recs = related_recs(hw,e)
   for irec,rec in enumerate(recs):
    print('  ',irec+1,rec)

 recsout = []
 for hw in ehws:
  recs = related_recs(hw,e)
  if len(recs) == 0:
   continue
  dochws = list_union_unique([r.dochws for r in recs])
  docptrs = list_union_unique([r.docptrs for r in recs])
  docall = list_union_unique([dochws,docptrs])
  rec = recs[0]
  rec.dochws = dochws
  # get ptrs that are not in dochws
  ptrs = [hw for hw in docptrs if hw not in dochws]
  rec.docptrs = ptrs
  recsout.append(rec)
  for hw1 in docall:
   e[hw1] = []
 
 return recsout

def extract_keys_c1(recsin):
 """ This method is sure, but quite slow 
  Is there a way to make it faster?
 """
 n = len(recsin)
 for rec in recsin:
  rec.ptrs_set = set(rec.dochws + rec.docptrs)
 recsout = []
 i1 = 0
 while i1 < n:
  rec1 = recsin[i1]
  #if (i1% 100) == 0: print(i1)
  if rec1 == None:
   i1 = i1 + 1
   continue
  dochws1 = rec1.dochws
  docptrs1 = rec1.docptrs
  #ptrs1 = dochws1 + docptrs1
  ptrs1_set = rec1.ptrs_set
  i2 = i1+1
  while i2 < n:
   rec2 = recsin[i2] 
   if rec2 == None:
    i2 = i2 + 1
    continue
   ptrs2_set = rec2.ptrs_set
   if ptrs1_set.intersection(ptrs2_set) == set():
    i2 = i2 + 1
    continue
   dochws2 = rec2.dochws
   docptrs2 = rec2.docptrs
   dochws1 = list_union_unique([dochws1,dochws2])
   docptrs1 = list_union_unique([docptrs1,docptrs2]) 
   recsin[i2] = None
   i2 = i2 + 1
  rec1.dochws = dochws1
  rec1.docptrs = docptrs1
  recsout.append(rec1)
  i1 = i1 + 1
 return recsout

def extract_keys_c2(recsin):
 """ This method is also sure, but much slower than extract_keys_c1
 """
 n = len(recsin)
 for rec in recsin:
  rec.ptrs_set = set(rec.dochws + rec.docptrs)
  rec.empty = False
 recsout = []
 i1 = 0
 while i1 < n:
  rec1 = recsin[i1]
  #if (i1% 100) == 0: print(i1)
  if rec1.empty:
   i1 = i1 + 1
   continue
  dochws1 = rec1.dochws
  docptrs1 = rec1.docptrs
  #ptrs1 = dochws1 + docptrs1
  ptrs1_set = rec1.ptrs_set
  i2 = i1+1
  recs2 = [rec2 for rec2 in recsin[i2:] if 
    (not rec2.empty) and
    (ptrs1_set.intersection(rec2.ptrs_set) != 0)]
  for rec2 in recs2:
   dochws2 = rec2.dochws
   docptrs2 = rec2.docptrs
   dochws1 = list_union_unique([dochws1,dochws2])
   docptrs1 = list_union_unique([docptrs1,docptrs2]) 
   rec2.empty = True
  rec1.dochws = dochws1
  rec1.docptrs = docptrs1
  recsout.append(rec1)
  i1 = i1 + 1
 return recsout

def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   #out = "%s\t%s" %(rec.status,rec)
   out = "%s" % rec
   f.write(out + '\n')
 print(len(recs),"records written to",fileout)

if __name__=="__main__": 
 dictlo = sys.argv[1]
 filein = sys.argv[2] #  extract_keys.txt
 fileout = sys.argv[3] # 
 recs = init_hwdoc(filein)
 recsout = extract_keys_c4(recs)
 write(fileout,recsout)
