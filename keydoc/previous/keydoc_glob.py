"""keydoc_glob.py
  
"""
from __future__ import print_function
import sys, re,codecs
import os

def init_hwdoc(filein,d,dictlo):
 with codecs.open(filein,"r","utf-8") as f:
  for x in f:
   hw,_ = x.split('\t')
   if hw not in d:
    d[hw]=[]
   d[hw].append(dictlo)
   #if dictlo not in d[hw]:
   # d[hw].append(dictlo)

dictlist = re.split(r' +','acc ap90 ben   bhs bop bur cae ' \
 + 'ccs gra gst ieg inm  krm mci md mw mw72 ' \
 + 'pe pgn pui    pw pwg sch shs skd ' \
 + 'snp stc vcp vei wil  yat ap pd')
# dictlist = re.split(r' +','ap90 mw')

def write(fileout,d):
 with codecs.open(fileout,"w","utf-8") as f:
  keys = d.keys()
  for hw in keys:
   dict_str = ','.join(d[hw])
   out = '%s\t%s' %(hw,dict_str)
   f.write(out + '\n')
 print(len(keys),"records written to",fileout)

if __name__=="__main__": 
 fileout = sys.argv[1]
 d = {}
 for dictlo in dictlist:
  filein = "data/%s/keydoc_input.txt"%dictlo
  if not os.path.exists(filein):
   print('keydoc_all skipping %s: %s not found' %(dictlo,filein))
   continue
  init_hwdoc(filein,d,dictlo)
 write(fileout,d)

