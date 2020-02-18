#-*- coding:utf-8 -*-
"""make_norm_extra_mw.py
 
"""
from __future__ import print_function
import sys, re,codecs

def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  n = 0
  for rec in recs:
   if (rec.mw_preverb != rec.pw_preverb) and rec.mwfound:
    out = '%s\t%s'%(rec.mw_preverb,rec.pw_preverb)
    f.write(out + '\n')
    n = n + 1
 print(n,"records written to",fileout)

class Preverb3(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  (self.count,self.pfx,self.k1,self.pw_preverb,
   self.mw_preverb,self.mwfound) = re.split(r' +',line)

def init_preverb3(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Preverb3(x) for x in f if not x.startswith(';')]
 print(len(recs),"records read from",filein)
 return recs

if __name__=="__main__": 
 filein = sys.argv[1] #  preverb3.txt
 fileout = sys.argv[2] # 
 recs = init_preverb3(filein)
 write(fileout,recs)

