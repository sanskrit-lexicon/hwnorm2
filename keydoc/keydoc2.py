"""keydoc1.py
 Specify documents from headword list.
 For mw, take into account the 'ABCE' record types
 
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
   self.docptrs = []
  else:
   self.docptrs = re.split(r'[,:]',parts[1])
  # for extract_keys_a
  self.status = 'orig'

 def __repr__(self):
  x = ','.join(self.dochws)
  #s = self.status + '\t'
  s = ''
  if self.docptrs == []:
   return s + x
  else:
   y = s + ','.join(self.docptrs)
   return '%s\t%s' %(x,y)

def init_hwdoc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWDoc(x) for x in f if not x.startswith(';')]
 return recs

def extract_keys_c(recsin):
 """  consider two records A and B
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
 # d is a dictionary, that maps any native key1  (e.g., a1,a2) into
 #  the record that contains it
 # We also cbeck that documents are disjoint, in the sense that
 # dochws attributes are disjoint
 d = {} 
 for rec in recsin:
  for hw in rec.dochws:
   # check for non-disjoint documents
   if hw in d:
    rec_dup = d[hw]
    print('non-disjoint documents:')
    print('A = %s' % rec_dup)
    print('B = %s' % rec)
   d[hw] = rec
 # 
 irecsdbg=[337,338,339]
 irecsdbg=[0,1,2]
 irecsdbg=[]
 def checkaNga(s,irec):
  print('checkaNga',s,irec)
  for i in irecsdbg:
   print('   ',i,recsin[i].status,recsin[i])
  for hw in ['a','aH']:
   print('d[%s]='%hw,d[hw])

 for irec,rec in enumerate(recsin):
  if irec in irecsdbg: checkaNga('BEFORE',irec)
  if rec.status == 'del':
   continue
  hws0 = [hw for hw in rec.docptrs if (hw in d) and (d[hw]!= rec)]
  if len(hws0) == 0:
   continue
  recs0 = [d[hw] for hw in hws0]    
  newptrs = []
  newhws =  []
  # copy dochws into newhws
  for hw in rec.dochws:
   newhws.append(hw)
  # reclassify rec.docptrs
  newhws1 = []  # the ones not in rec.dochws
  for hw in rec.docptrs:
   if hw not in hws0:
    newptrs.append(hw)
    continue
   assert hw not in newhws,"error xxx"
   newhws.append(hw)
   newhws1.append(hw)
  # Similarly merge dochws and docptrs for all rec0 in recs0
  # Not sure this logic is complete.
  for rec0 in recs0:
   for hw in rec0.dochws:
    if hw not in newhws:
     newhws.append(hw)
   for hw in rec0.docptrs:
    if hw not in newptrs:
     newptrs.append(hw)
  # relabel recs0 as deleted
  for rec0 in recs0:
   rec0.status = 'del'
  # reset d[hw] for the added headwords
  if irec in irecsdbg:print(irec,'newhws1=',newhws1)
  for hw in newhws1:
   d[hw].dochws = newhws
   d[hw].newptrs = newptrs
  if irec in irecsdbg: checkaNga('AFTER',irec)
  # reset rec
  rec.dochws = newhws
  rec.docptrs = newptrs
  rec.status = 'new'
 return

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
def extract_keys_c1(recsin):
 """  consider two records A and B
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
 global itest_c1,itext_c1_max
 # d is a dictionary, that maps any native key1  (e.g., a1,a2) into
 #  the record that contains it
 # We also cbeck that documents are disjoint, in the sense that
 # dochws attributes are disjoint
 d = {} 
 e = {}
 ehws = []
 for rec in recsin:
  """
  for hw in rec.dochws:
   # check for non-disjoint documents
   if hw in d:
    rec_dup = d[hw]
    print('non-disjoint documents:')
    print('A = %s' % rec_dup)
    print('B = %s' % rec)
   d[hw] = rec
  """
  ptrs = rec.dochws + rec.docptrs
  for hw in ptrs:
   if hw not in e:
    e[hw] = []
    ehws.append(hw)
   e[hw].append(rec)

  dochws = list_union_unique([r.dochws for r in e[hw]])
  docptrs = list_union_unique([r.docptrs for r in e[hw]])
  docall = list_union_unique([dochws,docptrs])
  for hw in docall:
   for r in e[hw]:
    r.dochws = dochws
    r.docptrs = docptrs
  for hw in ptrs:
   for r in e[hw]:
    if itest_c1 <= itext_c1_max:
     print('At 1) %s -> %s'%(hw,r))
  itest_c1 = itest_c1 + 1
 recsout = []
 f = {}
 itest_c1 = 0
 for hw in ehws:
  recs = e[hw]
  itest_c1 = itest_c1 + 1
  if itest_c1 <= itext_c1_max:
   s = ['%s'%rec for rec in recs]
   s1 = ':'.join(s)
   print(hw,'->',s1)
   print(len(recs),'records for headword',hw)
  #rec_maximal = maximal_doc(recs)
  dochws = list_union_unique([rec.dochws for rec in recs])
  docptrs = list_union_unique([rec.docptrs for rec in recs])
  docall = list_union_unique([dochws,docptrs])
  #rec = recs[0]
  #rec.max_dochws = dochws
  #rec.max_docptrs = docptrs
  # generate an 'empty' HWDoc
  docall_str = '.'.join(docall)
  if docall_str in f:
   if itest_c1 <= itext_c1_max:
    print('skipping',hw,'in ehws')
   continue
  f[docall_str] = True
  rec = HWDoc('')
  rec.dochws = dochws  
  rec.docptrs = docptrs
  recsout.append(rec)
 return recsout
 # first attempt
 for hw in ehws:
  recs = e[hw]
  dochws = list_union_unique([rec.dochws for rec in e[hw]])
  docptrs = list_union_unique([rec.docptrs for rec in e[hw]])
  # generate an 'empty' HWDoc
  rec = HWDoc('')
  rec.dochws = dochws
  rec.docptrs = docptrs
  recsout.append(rec)
 return recsout

def unused_extract_keys_b(d0,keyarr0):
 emptyset = set()
 multikey = [k for k in keyarr0 if len(d0[k])>1]
 d = {}
 for i1,k1 in enumerate(multikey):
  if d0[k1] == []:
   continue
  keys = set(d0[k1])
  found = False
  for i2,k2 in enumerate(multikey):
   if i2<=i1:
    continue
   keys2 = set(d0[k2])
   isect = keys.intersection(keys2)
   if isect != emptyset:
    keys = keys.union(keys2)
    #print('merging',k2,d0[k2],'into',k1,d0[k1],'yields',keys)
    d0[k2] = []
    d0[k1] = []
    found = True
  for k in keys:
   if (k != k1) and (k in d0) and (len(d0[k]) == 1):
    d0[k] = []
  if found:
   d[k1] = list(keys)
   #print('changing',k1,d0[k1],'to',d[k1]) 
 keyarr = []
 for k in keyarr0:
  if d0[k] != []:
   d[k] = d0[k]
   keyarr.append(k)
  elif k in d:
   #print('dropping key',k)
   keyarr.append(k)   
  else:
   #print('Dropping singleton key',k)
   pass
 return d,keyarr

def unused_extract_keys_b(d0,keyarr0):
 emptyset = set()
 multikey = [k for k in keyarr0 if len(d0[k])>1]
 d = {}
 for i1,k1 in enumerate(multikey):
  if d0[k1] == []:
   continue
  keys = set(d0[k1])
  found = False
  for i2,k2 in enumerate(multikey):
   if i2<=i1:
    continue
   keys2 = set(d0[k2])
   isect = keys.intersection(keys2)
   if isect != emptyset:
    keys = keys.union(keys2)
    #print('merging',k2,d0[k2],'into',k1,d0[k1],'yields',keys)
    d0[k2] = []
    d0[k1] = []
    found = True
  for k in keys:
   if (k != k1) and (k in d0) and (len(d0[k]) == 1):
    d0[k] = []
  if found:
   d[k1] = list(keys)
   #print('changing',k1,d0[k1],'to',d[k1]) 
 keyarr = []
 for k in keyarr0:
  if d0[k] != []:
   d[k] = d0[k]
   keyarr.append(k)
  elif k in d:
   #print('dropping key',k)
   keyarr.append(k)   
  else:
   #print('Dropping singleton key',k)
   pass
 return d,keyarr

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
 recsout = extract_keys_c1(recs)
 #extract_keys_c(recs) ## do it again
 #d0,keyarr0 = extract_keys_a(recs)
 #d,keyarr = extract_keys_b(d0,keyarr0)
 write(fileout,recsout)
