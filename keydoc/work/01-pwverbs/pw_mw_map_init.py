#-*- coding:utf-8 -*-
"""preverb2a.py
"""
from __future__ import print_function
import sys, re,codecs

class Preverb1(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.notes = line.split(':')
  self.mwspell = None
 
def init_preverb1(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Preverb1(x) for x in f]
 print(len(recs),"records read from",filein)
 return recs

def ar_f(k):
 if 'ar' in k:
  return re.sub(r'ar','f',k)
 return None

def A_E(k):
 if k.endswith('A'):
  return re.sub(r'A$','E',k)
 return None

def manual(k):
 dManual = { # pw:mw
  'graB':'grah',
  'iD':'inD',
  'arTay':'arT',  # there IS an 'arT' in PW, pointing to 'arTay'
  'hvA':'hve',
  'skad':'skand',
  'Sar':'SF',
  'Sad':'Sat',  
  'vyA':'vye',
  'vAsay':'vAs',
  'lakzay':'lakz',
  'kalp':'kxp',
 }
 if k in dManual:
  return dManual[k]
 return None

def mwspell_helper(k):
 """ k is pw spelling.
   change to an MW spelling
 """
 k2 = manual(k)
 if k2 != None:
  return k2

 k2 = A_E(k)
 if k2 != None:
  return k2

 k2 = ar_f(k)
 if k2 != None:
  return k2
 return None

def mwspell(recs):
 for rec in recs:
  k = mwspell_helper(rec.k1)
  if k != None:
   rec.mwspell = k

def write(fileout,recs):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   if not rec.mwspell:
    continue
   n = n + 1
   out = "%s:%s" %(rec.k1,rec.mwspell)
   f.write(out + '\n')
 print(n,"records written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  preverb1.txt
 fileout = sys.argv[2] # pw_mw_map_init.txt

 recs = init_preverb1(filein)
 mwspell(recs)
 write(fileout,recs)
