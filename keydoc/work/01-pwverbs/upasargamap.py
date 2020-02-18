#-*- coding:utf-8 -*-
"""upasargamap.py
"""
from __future__ import print_function
import sys, re,codecs

def mark_entries_mwverb(entries,mwrecs):
 d = {}
 for mwverb in mwrecs:
  root = mwverb.k1
  if root not in d:
   d[root] = []
  d[root].append(mwverb)
 for entry in entries:
  metad = entry.metad
  k1 = metad['k1']  
  if k1 in d:
   entry.mwverb = d[k1]  # list of MWVerb records
  if k1 == 'car':
   print('mark_entries_mwverb found',k1)
 print(len(d.keys()),"distinct roots in mw")

def merge_entries(entries):
 d = {}
 keys = []
 for entry in entries:
  if not entry.mwverb:
   continue 
  if entry.nonverb:
   continue
  metad = entry.metad
  k1 = metad['k1']
  if k1 not in d:
   d[k1] = []
   keys.append(k1)
  d[k1].append(entry)
 recs = [d[k1] for k1 in keys]
 # check that for each k1, each entry in d[k1] has 
 for entries in recs:
  entry0 = entries[0]
  mwverb0 = entry0.mwverb  
  problem_entries = [entry for entry in entries if entry.mwverb != mwverb0]
  if problem_entries != []:
   print('merge_entries unexpected problem')
   exit(1)
 return recs

def mark_entries(entries):
 # Certain patterns indicate a verb
 for entry in entries:
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
    
  if len(marks) > 0:
   entry.marked = True
   entry.marks = marks

def write(fileout,entrylists):
 n = 0
 def yesno(flag):
  if flag:
   return 'yes'
  else:
   return 'no'
 with codecs.open(fileout,"w","utf-8") as f:
  for entrylist in entrylists:
   entry0 = entrylist[0]
   k1 = entry0.metad['k1']  # same for all entries in entrylist
   Lnums = [entry.metad['L'] for entry in entrylist]
   L = '&'.join(Lnums)
   n = n + 1
   #L = entry.metad['L']
   #k1 = entry.metad['k1']
   mwverb = entry0.mwverb  # a list of MWVerb objects. same for all in entrylist
   a = []
   for mwrec in mwverb:
    a1 = mwrec.line  
    # colon-separated fields.
    # the 'cps' field has comma-separated subfields
    # change these commas to '-'
    a1 = a1.replace(',','-')
    # now change the colon separators to comma
    a1 = a1.replace(':',',')  # use comma instead of colon
    a.append(a1)
    mwrec.used = True
   astr = ';'.join(a)
   outarr = []
   outarr.append(k1)
   outarr.append(L)
   #outarr.append(yesno(entry.marked))
   outarr.append(astr)
   out = ':'.join(outarr)
   f.write(out + '\n')
 print(n,"records written to",fileout)

def unused_mark_entries(entries,Lnums):
 for L in Lnums:
  if L not in Entry.Ldict:
   print('mark_entries ERROR 404:',L)
  else:
   entry = Entry.Ldict[L]
   entry.L_marked = True

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"returned from mwverbs")
 return recs

def write1(fileout,mwrecs):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for mwrec in mwrecs:
   if mwrec.used:
    continue
   n = n + 1
   out = mwrec.line
   f.write(out + '\n')
 print(n,"unused mw roots written to",fileout)

def write2(fileout,entrylists):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for entrylist in entrylists:
   if len(entrylist) == 1:  # only do multiple
    continue
   for entry in entrylist:
    k1 = entry.metad['k1']  # same for all entries in entrylist
    L = entry.metad['L']
    line = entry.datalines[0]
    out = '%s~%s~%s' %(k1,L,line)
    f.write(out + '\n')
   f.write(';\n')
   n = n + 1
 print(n,"records written to",fileout)

def mark_nonverb_test(line):
 if re.search(r'<lex>.*?</lex>',line):
  return True
 if re.search(r'<ab>Interj.</ab>',line):
  return True
 if re.search(r'[pP]ronom',line):
  return True
 if re.search(r'[pP]ron[.] interr[.]',line):
  return True
 if re.search(r'Indec[.]',line):
  return True
 if re.search(r'onomatop[.]',line):
  return True
 if re.search(u'¦ *<ab>Adv.</ab>',line):
  return True
 if re.search(u'¦ Suffix',line):
  return True
 if re.search(r'am Anfange einiger Comp',line):
  return True
 if re.search(u'¦ , <ab>Partic.</ab>',line):
  return True
 if re.search(r'in Verbindung mit Verben',line):
  return True
 if re.search(r'{#an°#}',line):
  return True
 return False
def nonverb_L(L):
 return L in [
  '8060', # 2 am
  '17564', # 2 Iz
  '32290', #3 kzan 
  '43153', #2 jur
  '44364', #2 tan
  '44565', #2 tap
  '46209', #3 tuj
  '48378', #1 daMs
  '48549', #2 daG
  '48982', #2 dam
  '49963', #2 dAs
  '50445', #2 dih
  '51761', #3 dU
  '55375', #4 Di
  '79165', #2 Bas
  '81416', #1 makz
  '82098', #2 mad
  '83995', #2 mas
  '85532', #2 mA
  '85538', #8 mA
  '87639', #4 mur
  '87640', #5 mur
  '87691', #2 muz
  '88057', #2 mUz
  '91858', #2 rakz
  '91859', #3 rakz
  '92679', #2 ran  participle of rA
  '93141', #4 rA
  '94176', #3 ri
  '94277', #2 rI
  '95639', #2 law
  '96737', #2 low
  '97608', #2 vaw
  '97890', #2 van
  '99301', #4 vas
  '99303', #6 vas
  '101504', #2 vAh
  '102101', #2 vij
  '111075', #2 Sas
  '115878', #2 Svit
  '119268', #3 sap
  '125609', #6 su
  '128532', #2 sU
  '128535', #5 sU
  '130532', #3 stu
  '130533', #4 stu
  '131340', #4 snu
  ]

def mark_nonverb(entries):
 for entry in entries:  
  if len(entry.marks) > 0:
   # we've already marked this as a verb.
   # not allowed to unmark it!
   continue
  if nonverb_L(entry.metad['L']):
   entry.nonverb = True
   if entry.metad['k1'] == 'car':
    print('marked car as nonverb_L')
   continue
   
  for line in entry.datalines:
   if mark_nonverb_test(line):
    entry.nonverb = True
    if entry.metad['k1'] == 'car':
     print('marked car as nonverb_test')
    break

class Preverb1(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.notes = line.split(':')
  upastr = self.notes.replace('~',',')
  upastr1 = upastr.replace('*','')
  upasargas = upastr1.split(',')
  a = [] # remove duplicates
  for u in upasargas:
   if u not in a:
    a.append(u)
  self.upasargas = a

def init_preverb1(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Preverb1(x) for x in f]
 print(len(recs),"records read from",filein)
 return recs

def k1map(recs1):
 d1 = {}
 keys1 = []
 for rec1 in recs1:
  k1 = rec1.k1
  if k1 in d1:
   print('Unexpected duplicate',k1,rec1.line)
   exit()
  d1[k1] = rec1
 return keys1,d1

class PWMW(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.k1mw = line.split(':')
  self.used = False

def init_pw_mw_map(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [PWMW(x) for x in f if not x.startswith(';')]
 print(len(recs),"records read from",filein)
 keys,d = k1map(recs)
 return recs,d

def spellmerge(recs_preverb1,mwrecs,pwmwd):
 keys1,d1 = k1map(recs_preverb1)
 keys2,d2 = k1map(mwrecs)
 # get exact matches
 matches = []
 for k1 in d1:
  r1 = d1[k1]
  k2 = None
  if k1 in d2:
   k2 = k1
  elif k1 in pwmwd:
   k = pwmwd[k1].k1mw
   if k in d2:
    k2 = k
    pwmw = pwmwd[k1]
    pwmw.used = True
   else:
    print('map not in mwrecs:',k1,k)
  if k2 == None:
   continue
  r2 = d2[k2]
  r1.used = r2
  r2.used = r1

def write_matches(fileout,recs_preverb1):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec1 in recs_preverb1:
   if not rec1.used:
    continue
   rec2 = rec1.used
   out = '%s %s' %(rec1.line,rec2.line)
   f.write(out + '\n')
   n = n + 1
 print(n,"records written to",fileout)

def write_unmatched(fileout,recs):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   if rec.used:
    continue
   out = rec.line
   f.write(out + '\n')
   n = n + 1
 print(n,"records written to",fileout)

def all_upasargas(recs):
 d = {}
 for rec in recs:
  for u in rec.upasargas:
   if u not in d:
    d[u] = 1
   else:
    d[u] = d[u] + 1
 keys=d.keys()
 keys = sorted(keys)
 print(len(keys),'total upasargas found')
 if True:
  for u in keys:
   print(u,d[u])
 return keys

if __name__=="__main__": 
 filein = sys.argv[1] #  preverb1.txt
 fileout = sys.argv[2] # upasargamap.txt
 recs_preverb1 = init_preverb1(filein)
 upasargas = all_upasargas(recs_preverb1)
 exit(1)
 write_matches(fileout,recs_preverb1)
 for r in pw_mw_recs:
  if not r.used:
   print('unused mapping:',r.line)
