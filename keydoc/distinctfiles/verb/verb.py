"""
  
"""
from __future__ import print_function
import sys, re,codecs
class Verbmap(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  parts = re.split(r' +',line)
  self.verbs = []
  self.dictlists = []
  for part in parts:
   verb,dictliststr = part.split(':')
   dictlist = dictliststr.split(',')
   self.verbs.append(verb)
   self.dictlists.append(dictlist)

def init_verbmap(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Verbmap(x) for x in f if not x.startswith(';')]
 print(len(recs),"records read from",filein)
 return recs

def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  n = 0
  for rec in recs:
   out = ','.join(rec.verbs)
   f.write(out+'\n')
   n = n + 1
 print(n,"records written to",fileout)

if __name__=="__main__": 
 # from sanskrit-lexicon/MWS/verbs01
 filein = sys.argv[1] #  verbs1_merge2.txt 
 fileout = sys.argv[2] # keydoc1x_norm.txt
 verbs = init_verbmap(filein)
 write(fileout,verbs)

