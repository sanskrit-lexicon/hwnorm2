"""keydoc_glob1.py
  
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
   self.docptrs = []
  else:
   self.docptrs = re.split(r'[,:]',parts[1])

def init_hwdoc(filein,d,dictlo):
  
 with codecs.open(filein,"r","utf-8") as f:
  for x in f:
   x = x.rstrip('\r\n')
   hw,dochws_str = x.split('\t')
   if hw not in d:
    d[hw]=[]
   ok = True
   for rec in d[hw]:
    if (dictlo == rec[0]):
     ok = False  
   if not ok:
    print("init_hwdoc error: %s %s" %(dictlo,hw))
   dochws = dochws_str.split(',') 
   def starF(hw1):
    if hw1 == hw:
     return '*'
    else:
     return hw1
   vals = map(starF,dochws)
   valstr = ','.join(vals)
   rec = '%s=%s' %(dictlo,valstr)
   #rec = '%s=%s' %(dictlo,dochws_str)
   d[hw].append(rec)



def write(fileout,d):
 with codecs.open(fileout,"w","utf-8") as f:
  keys = d.keys()
  for hw in keys:
   recs = []
   for r in d[hw]:
    # r often is like mw=*, ap90=*  (DICT=*).
    #  simplify these to simply a dict code
    # the meaning is that in the dictionary, the document is defined by
    # just one headword, i.e. hw.
    # Other cases are like mw=abc  (abc!=hw) or
    # mw=abc,xyz  where abc is either a headword or '*' meaning hw.
    r1 = re.sub(r'^([^,]+)=[*]$',r'\1',r)
    recs.append(r1)
   dict_str = ':'.join(recs)
   out = '%s\t%s' %(hw,dict_str)
   f.write(out + '\n')
 print(len(keys),"records written to",fileout)

def init_dictlist(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip() for x in f]
 return recs
 
if __name__=="__main__":
 filein = sys.argv[1]  # dictlist.txt
 fileout = sys.argv[2]
 dictlist = init_dictlist(filein)
 d = {}
 for dictlo in dictlist:
  filein = "data/%s/keydoc_input.txt"%dictlo
  if not os.path.exists(filein):
   print('keydoc_all skipping %s: %s not found' %(dictlo,filein))
   continue
  init_hwdoc(filein,d,dictlo)
 write(fileout,d)

