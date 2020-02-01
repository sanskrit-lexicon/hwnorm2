# coding: utf-8
""" hwnorm1c.py  
   Feb 25, 2016. Initially, based on hwnorm1_v1c.py used by display
   //www.sanskrit-lexicon.uni-koeln.de/scans/awork/hwnorm/hwnorm1.php
   However, now considered independent.
   Jan 27, 2015
   Feb 22, 2016
   Revised hwnorm1_v1b.py so that 
   records with the same normalized spelling are put on 
   the same line of output.
   Oct 12, 2017. Remove 'fxx' -> 'fx'.  
    There is no sandhi rule for this. It's inclusion was an error.
    ref: https://github.com/sanskrit-lexicon/alternateheadwords/issues/23
   Oct 12, 2017. Add rule 'rxX' -> 'rX', where x is a non-aspirated
     consonant and X is the aspirated form of x.  For instace
     ardDa -> arDa.   Both forms are equivalent, we choose the rX form as
     the normalized form.
   Oct 18, 2017. Revised the 'cC -> C' normalization.
"""
from __future__ import print_function
import re,codecs
def unused_init(filename):
    with codecs.open(filename,'r','utf-8') as f:
        ans = {}
        for x in f:
         x = x.rstrip('\r\n')
         (normkey,key,dictstr) = re.split(r':',x)
         if normkey not in ans:
          ans[normkey]=[]
         ans[normkey].append("%s:%s" %(key,dictstr))
    return ans

slp1_cmp1_helper_data = {
 'k':'N','K':'N','g':'N','G':'N','N':'N',
 'c':'Y','C':'Y','j':'Y','J':'Y','Y':'Y',
 'w':'R','W':'R','q':'R','Q':'R','R':'R',
 't':'n','T':'n','d':'n','D':'n','n':'n',
 'p':'m','P':'m','b':'m','B':'m','m':'m'
}

def slp_cmp1_helper1(m):
 #n = m.group(1) # always M
 c = m.group(2)
 nasal = slp1_cmp1_helper_data[c]
 return (nasal+c)
rxX_helper_data = {
 'k':'K','g':'G',
 'c':'C','j':'J',
 'w':'W','q':'Q',
 't':'T','d':'D',
 'p':'P','b':'B'
}
def rxX_helper(m):
 # m.group(0) == rxX
 x = m.group(1)
 X = m.group(2)
 if (x in rxX_helper_data) and (X == rxX_helper_data[x]):
  return 'r'+X
 else:
  # no change
  return 'r'+x+X

def normalize_key_C(a):
 if 'C' not in a:
  return a
 # X + C -> XcC  (X a vowel)
 a1 = re.sub(r'([aAiIuUfFxXeEoO])C',r'\1cC',a)
 # X + cC -> XC  (X a consonant)
 a2 = re.sub(r'([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvhzSsHM])cC',r'\1C',a1)
 return a2

def homorganic_nasal(a):
 return re.sub(r'(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])',slp_cmp1_helper1,a)

def rxx_rx(a):
 return re.sub(r'([r])(.)\2',r'\1\2',a)

def rxX_rX(a):
 return re.sub(r'r(.)(.)',rxX_helper,a)

def aM(a):
 return re.sub(r'aM$','a',a)

def aH(a):
 return re.sub(r'aH$','a',a)

def uH(a):
 return re.sub(r'uH$','u',a)

def iH(a):
 return re.sub(r'iH$','i',a)

def ttr_tr(a):
 return re.sub(r'ttr','tr',a)

def ant_at(a):
 return re.sub(r'ant$','at',a)

def normalize_key(a):
 changes = []
 rules = [
  ('Mm',homorganic_nasal),
  ('rxx',rxx_rx),
  ('rxX',rxX_rX),
  ('aM',aM),
  ('aH',aH),
  ('uH',uH),
  ('iH',iH),
  ('ttr',ttr_tr),
  ('ant',ant_at),
  ('cC',normalize_key_C),  

 ]
 for rule in rules:
  code,f = rule
  b = f(a)
  change = (code,b)
  changes.append(change)
  a = b
 return a
 #return changes

def query(sanhwd_norm):
 while True:
    keyin = raw_input('Enter hw (empty to quit): ')
    if keyin == '':
        print("bye")
        break
    normkey = normalize_key(keyin)
    if normkey not in sanhwd_norm:
        print("No match for normalized key ",normkey)
    else:
        for rec in sanhwd_norm[normkey]:
            print("     ",rec)

class Normkey(object):
 def __init__(self,normkey):
  self.normkey = normkey
  self.lines = []

def main():
 import sys
 filein = sys.argv[1]
 fileout = sys.argv[2]
 f = codecs.open(filein,'r','utf-8')
 fout = codecs.open(fileout,'w','utf-8')
 n = 0
 dnorm={}
 recsout=[]
 for line in f:
  n = n + 1
  line = line.rstrip('\r\n')
  (key,dictstr) = re.split(r':',line)
  normkey = normalize_key(key)
  if normkey in dnorm:
   rec = dnorm[normkey]
  else:
   rec = Normkey(normkey)
   recsout.append(rec)
   dnorm[normkey]=rec
  rec.lines.append(line)
 # Loop through recsout, generating output
 for rec in recsout:
  outline = ';'.join(rec.lines)
  out = '%s:%s' %(rec.normkey,outline)
  fout.write("%s\n" % out)
 #
 f.close()
 fout.close()
 print(n,"lines read from",filein)
 print(len(recsout),"lines written to",fileout)
 dups = [r for r in recsout if len(r.lines)>1]
 print(len(dups),"duplicates found")

if __name__=="__main__":
 main()
