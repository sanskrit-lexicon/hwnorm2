#-*- coding:utf-8 -*-
"""preverb1.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.marks = []  # verb markup markers, in order found, if any

def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

def  make_correction(entry,iline,oldline,newline,upasarga,upasarga1):
 outarr = []
 d = entry.metad
 outarr.append('; key = %s, L = %s,  %s -> %s'%(d['k1'],d['L'],upasarga,upasarga1))
 lnum = entry.linenum1 + iline +1
 outarr.append('%s old %s' %(lnum,oldline))
 outarr.append('%s new %s' %(lnum,newline))
 outarr.append(';')
 return outarr

def mark_entries_verb(entries,pwnonverbsd):
 for entry in entries:
  # first exclude known non-verbs
  k1 = entry.metad['k1']
  if k1 in pwnonverbsd:
   continue
  # might be a verb. look for upasarga pattern
  marks = []
  for iline,line in enumerate(entry.datalines):
   m = re.search(r'<ab>(Desid.|Intens.|Caus.)</ab>',line)
   if m:
    form = m.group(1)
    marks.append(form)
   m = re.search(r'<div n="p">— Mit {#(.*?)#}',line)
   if m:
    upasarga = m.group(1)
    # look for cases with {#xxx#} contains more than upasarga
    if not re.search(r'^[*]?[a-zA-Z]*$',upasarga):    
     upasarga = '{#%s#}' % upasarga
     upasarga1 = re.sub(r'^{#([*]?.*?)([^a-zA-Z].*)#}$',r'{#\1#}{#\2#}',upasarga)
     upasarga2 = re.sub(r'#}{# *, *',r'#}, {#',upasarga1)
     newline = line.replace(upasarga,upasarga2)
     correction_lines = make_correction(entry,iline,line,newline,upasarga,upasarga2)
     for c in correction_lines:
      print(c)
     # correct upasarga for marks
     m = re.search(r'<div n="p">— Mit {#(.*?)#}',newline)
     upasarga = m.group(1)
    # add upasarga to the list of marks
    marks.append(upasarga)
    
  if len(marks) == 0:
   continue
  # remove cases where ONLY Desid.|Intens.|Caus. is present in marks
  marks = [x for x in marks if x not in ['Desid.','Intens.','Caus.']]
  if len(marks) > 0:
   """ Consider cases like 
     {#*marImfja#}¦ <lex>Adj.</lex> vom <ab>Intens.</ab> von {#marj#}.
    which should NOT be marked as verb
   """
   isverb = True  # tentatively
   line = entry.datalines[0]
   if re.search(r'¦ *<lex>',line):
    print(entry.metad['k1'],entry.metad['L'],' NOT A VERB')
    isverb = False #  No, mistaken identity!
   if isverb:
    entry.marked = True
    entry.marks = marks

def merge_marked_entries(entries):
 d = {}
 keys = []
 for entry in entries:
  if not entry.marked:
   continue
  k1 = entry.metad['k1']
  if k1 not in d:
   d[k1] = []
   keys.append(k1)
  d[k1].append(entry)
 entrylists = []
 for k1 in keys:
  entrylists.append(d[k1])
 return entrylists

def write(fileout,entrylists):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for entrylist in entrylists:
   k1 = entrylist[0].metad['k1']  
   n = n + 1
   L = '&'.join([entry.metad['L'] for entry in entrylist])
   entrylistmarks = [','.join(entry.marks) for entry in entrylist]
   allmarks = '~'.join(entrylistmarks)
   outarr = []
   outarr.append(k1)
   outarr.append(L)
   outarr.append(allmarks)
   out = ':'.join(outarr)
   f.write(out + '\n')
 print(n,"records written to",fileout)

def init_pwnonverbs(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f if not line.startswith(';')]
 d = {}
 for line in lines:
  m = re.search(r'^([^ ]*)',line)
  key = m.group(1)
  d[key] = True
 return d

if __name__=="__main__": 
 dictlo = sys.argv[1] # xxx
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[3] # pw non verb file.
 fileout = sys.argv[4] # 
 entries = init_entries(filein)
 pwnonverbsd = init_pwnonverbs(filein1)

 mark_entries_verb(entries,pwnonverbsd)
 entrylists = merge_marked_entries(entries)
 write(fileout,entrylists)
