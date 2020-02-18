#-*- coding:utf-8 -*-
"""preverb3.py
 
"""
from __future__ import print_function
import sys, re,codecs

def write(fileout,recs_preverb_mw):
 n = 0
 def yesno(flag):
  if flag:
   return 'yes'
  else:
   return 'no'
 nyes = 0
 nno = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs_preverb_mw):
   preverb1 = rec.preverb1
   upasargas = preverb1.upasargas
   pwpreverbs = preverb1.pwpreverbs
   mwpreverbs = preverb1.mwpreverbs
   mwpreverbs_found = preverb1.mwpreverbs_found
   outarr = []
   k1 = preverb1.k1
   iyes = len([mwfound for mwfound in mwpreverbs_found if mwfound])
   ino  = len([mwfound for mwfound in mwpreverbs_found if not mwfound])
   outarr.append('; Case %03d  %s  %s (%s/%s)' %
    (irec+1,k1,len(upasargas),iyes,ino))
   for iupa,upa in enumerate(upasargas):
    icase = iupa + 1
    pwpreverb = pwpreverbs[iupa]
    mwpreverb = mwpreverbs[iupa]
    mwfound = mwpreverbs_found[iupa]
    if mwfound:
     nyes = nyes + 1
    else:
     nno = nno + 1
    outarr.append('%02d %10s %10s %20s %20s %s'%(icase,upa,k1,pwpreverb,mwpreverb,yesno(mwfound)))
   for out in outarr:
    f.write(out + '\n')
 n = len(recs_preverb_mw)
 print(n,"records written to",fileout)
 print(nyes,"mwpreverb spellings found")
 print(nno,"mwpreverb spellings NOT found")

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
 recs = [r for r in recs if r.cat == 'preverb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"preverbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d

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


class Preverb1(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.Lstr,self.notes = line.split(':')
  upastr = self.notes.replace('~',',')
  upastr1 = upastr.replace('*','')
  upasargas = upastr1.split(',')
  a = [] # remove duplicates
  for u in upasargas:
   if u not in a:
    a.append(u)
  self.upasargas = a
  self.pwpreverbs = []
  self.mwpreverbs = []
  self.mwpreverbs_found = []

class Preverb1_mw(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.preverb1_line,self.mw_line = line.split(' ')
  self.preverb1 = Preverb1(self.preverb1_line)
  self.mwrec = MWVerb(self.mw_line)

def preverb_mw_edit(line):
 changes = [
  ['dar:49037&49038:anu,apa,ava,vyava,A,ud,ni,nis,pari,pra,aBipra,prati,vi,udvi,pravi~A,atyA,pratyA,samA df:95065:verb:6Ā:',
   ['dar:49037:anu,apa,ava,vyava,A,ud,ni,nis,pari,pra,aBipra,prati,vi,udvi,pravi dF:95496:verb:9P,2P,2Ā:',
    'dar:49038:A,atyA,pratyA,samA df:95065:verb:6Ā:'
   ]
  ],
  ['sarj:121554&121556:ud,aByud~ati,aByati,samati,anu,aByanu,apa,vyapa,api,pratyapi,aBi,ava,atyava,anvava,aByava,upAva,nyava,pratyava,vyava,samava,A,aDyA,upA,samA,ud,anUd,aByud,paryud,vyud,samud,upa,nirupa,samupa,ni,pratini,saMni,nis,aBinis,pratinis,parA,pari,pra,anupra,paripra,pratipra,vi,anuvi,aBivi,udvi,prativi,saMvi,sam,anusam,upasam,parisam,pratisam sarj:237906&237907:verb:1P,1P:',
   ['sarj:121554:ud,aByud sarj:237906&237907:verb:1P,1P:',
   'sarj:121556:ati,aByati,samati,anu,aByanu,apa,vyapa,api,pratyapi,aBi,ava,atyava,anvava,aByava,upAva,nyava,pratyava,vyava,samava,A,aDyA,upA,samA,ud,anUd,aByud,paryud,vyud,samud,upa,nirupa,samupa,ni,pratini,saMni,nis,aBinis,pratinis,parA,pari,pra,anupra,paripra,pratipra,vi,anuvi,aBivi,udvi,prativi,saMvi,sam,anusam,upasam,parisam,pratisam sfj:251924:verb:6P,6Ā:'
   ]
  ],

 ]
 for oldline,newlines in changes:
  if line == oldline:
   pwpart,_ = line.split(' ')
   k1,Ls,_ = pwpart.split(':')
   print('preverb_mw_edit: editing',k1,Ls)
   return newlines
 # otherwise just return line as a list
 return [line]

def init_preverb1_mw(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = []
  for line in f:
   line = line.rstrip()
   edit_lines = preverb_mw_edit(line)
   for edit_line in edit_lines:
    recs.append(Preverb1_mw(edit_line))
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

sandhimap = {
 ('i','a'):'ya',
 ('i','A'):'yA',
 ('i','i'):'I',
 ('i','I'):'I',
 ('i','u'):'yu',
 ('i','U'):'yU',
 ('i','f'):'yf',
 ('i','F'):'yF',
 ('i','e'):'ye',
 ('i','E'):'yE',
 ('i','o'):'yo',
 ('i','O'):'yO',

 ('u','a'):'va',
 ('u','A'):'vA',
 ('u','i'):'vi',
 ('u','I'):'vI',
 ('u','u'):'U',
 ('u','U'):'U',
 ('u','f'):'vf',
 ('u','F'):'vF',
 ('u','e'):'ve',
 ('u','E'):'vE',
 ('u','o'):'vo',
 ('u','O'):'vO',

 ('a','a'):'A',
 ('a','A'):'A',
 ('A','a'):'A',
 ('A','A'):'A',
 
 ('a','i'):'e',
 ('A','i'):'e',
 ('a','I'):'e',
 ('A','I'):'e',
 
 ('a','u'):'o',
 ('A','u'):'o',
 ('a','U'):'o',
 ('A','U'):'o',
 
 ('a','f'):'Ar',
 ('A','f'):'Ar',
 ('a','e'):'e',
 ('d','s'):'ts',
 ('a','C'):'acC', # pra+Cad = pracCad
 ('i','C'):'icC',
 ('d','q'):'qq',  # ud + qI
 ('d','k'):'tk',
 ('d','K'):'tK',
 ('d','c'):'tc',
 ('d','C'):'tC',
 ('d','w'):'tw',
 ('d','W'):'tW',
 ('d','t'):'tt',
 ('d','T'):'tT',
 ('d','p'):'tp',
 ('d','P'):'tP',
 ('d','s'):'ts',
 ('d','n'):'nn',

 ('i','st'):'izw',
 ('s','h'):'rh', # nis + han -> nirhan
 ('m','s'):'Ms', # sam + saYj -> saMsaYj
 ('m','S'):'MS',
 ('m','k'):'Mk',
 ('m','K'):'MK',
 ('m','c'):'Mc',
 ('m','C'):'MC',
 ('m','w'):'Mw',
 ('m','W'):'MW',
 ('m','t'):'Mt',
 ('m','T'):'MT',
 ('m','p'):'Mp',
 ('m','P'):'MP',

 ('m','v'):'Mv',
 ('m','l'):'Ml',
 ('m','r'):'Mr',
 ('m','n'):'Mn',
 
 ('s','k'):'zk', # nis + kf -> nizkf
 ('s','g'):'rg',
 ('s','G'):'rG',
 ('s','j'):'rj',
 ('s','q'):'rq',
 ('s','d'):'rd',
 ('s','D'):'rD',
 ('s','b'):'rd',
 ('s','B'):'rD',
 ('s','m'):'rm',
 ('s','n'):'rn',

}
def join_prefix_verb(pfx,root):
 if pfx.endswith('ud') and (root == 'sTA'):
  return pfx[0:-2] + 'ut' + 'TA'  # ud + sTA = utTA
 if (pfx == 'saMpra') and (root in ['nad','nam','naS']):
  pfx = 'sampra'
  root = 'R' + root[1:]
  return pfx + root
 if (pfx == 'pra') and (root == 'nakz'):
  return 'pranakz' # odd, since mw has aBipraRakz
 pfx1,pfx2 = (pfx[0:-1],pfx[-1])
 root1,root2 = (root[0],root[1:])
 if (pfx2,root1) in sandhimap:
  return pfx1 + sandhimap[(pfx2,root1)] + root2
 if len(root) > 1:
  root1,root2 = (root[0:2],root[2:])
  if (pfx2,root1) in sandhimap:
   return pfx1 + sandhimap[(pfx2,root1)] + root2
 if root == 'i':
  if pfx == 'dus':
   return 'duri'
  if pfx == 'nis':
   return 'niri'
 if 'saMpra' in pfx:
  pfx = pfx.replace('saMpra','sampra')
  return pfx + root
 if  pfx.endswith(('pari','pra')) and root.startswith('n'):
  return pfx + 'R' + root[1:]  # pra + nad -> praRad
 if pfx.endswith('nis') and root.startswith(('a','I','u','U')):
  pfx = pfx.replace('nis','nir')
  return pfx + root
 ans = pfx + root
 d = {'duscar':'duScar'}
  
 if ans in d:
  ans = d[ans]
 return ans

def join_upasargas(recs_preverb1_mw,mwpreverbs_dict):
 
 for rec in recs_preverb1_mw:
  preverb1 = rec.preverb1
  mwrec = rec.mwrec
  k1 = preverb1.k1
  kmw = mwrec.k1
  for u in preverb1.upasargas:
   pw_preverb = join_prefix_verb(u,k1)
   preverb1.pwpreverbs.append(pw_preverb)
   mw_preverb = join_prefix_verb(u,kmw)
   preverb1.mwpreverbs.append(mw_preverb)
   if mw_preverb in mwpreverbs_dict:
    mwprerec = mwpreverbs_dict[mw_preverb]
    mwprerec.used = True
    preverb1.mwpreverbs_found.append(True)
   else:
     preverb1.mwpreverbs_found.append(False)

if __name__=="__main__": 
 filein = sys.argv[1] #  preverb1_mw_edit.txt
 filein1 = sys.argv[2] # mwverbs1.txt
 
 fileout = sys.argv[3] # preverb2.txt  matches of filein, filein1
 #fileout1 = sys.argv[6] # mwverbs not found in preverb1
 #fileout2 = sys.argv[7] # preverb1 lines not matched
 recs_preverb1_mw = init_preverb1_mw(filein)
 mwrecs,mwpreverbs_dict = init_mwverbs(filein1)
 join_upasargas(recs_preverb1_mw,mwpreverbs_dict)
 write(fileout,recs_preverb1_mw)

 exit(1)
 write_unmatched(fileout1,recs_preverb1)
 write_unmatched(fileout2,mwrecs)
 write_matches(fileout,recs_preverb1)
 for r in pw_mw_recs:
  if not r.used:
   print('unused mapping:',r.line)
