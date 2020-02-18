
PW verbs, and prefixed verbs

NOTE:  This work was originally done in a temporary directory
csl-orig/v02/pw/temp_verbs.  Some of the paths (such as ../pw.txt)
mentioned in the following notes make use of this original location.


* temporary copy of pw.txt
cp ../pw.txt temp_old_pw.txt
* temporary new version of pw.txt, initialized
cp temp_old_pw.txt temp_new_pw.txt

* correct upasarga markup, revise temp_new_pw.txt
python updateByLine.py temp_old_pw.txt manualByLine.txt temp_new_pw.txt

* preverb1.txt
python preverb1.py pw temp_new_pw.txt pwnonverb.txt preverb1.txt 
The output file shows markup improvements for upasargas.

preverb1.txt looks for patterns in PW entries that
usually indicate that the entry is a verb. 
The patterns are:
1) presence of <div n="p">— Mit {#xx#}   xx is typically a preverb, like ud, upa,
   The upasarga form is required
 We currently exclude presence of Caus., Desid., Intens.
2) presence of <ab>Caus.</ab>   entry has a causal form
3) <ab>Desid.</ab>
4) <ab>Intens.</ab>

* format of preverb1.txt records
  Three ':' separated fields per line
 1. pw headword
 2. pw Lnums corresponding to verbs. If more than 1 L, spearate using '&'
 3. pw upasargas, a comma-separated list.
     If more than 1 L, the upasarga lists for each L are separated by '~'

* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root
    
* pw_mw_map_edit.txt
 A mapping from pw spelling of roots to mw spelling.
python pw_mw_map_init.py preverb1.txt pw_mw_map_init.txt

cp pw_mw_map_init.txt pw_mw_map_edit.txt


* preverb2a
python preverb2a.py pw preverb1.txt mwverbs1.txt pw_mw_map_edit.txt preverb1_mw.txt preverb1_unmatched.txt mwverbs1_unmatched.txt

preverb1_mw.txt - matches between preverb1 records and mwverbs1 records
  Format:
  two space-separated fields
 1. preverb1 record
 2. mwverbs1 record

preverb1_unmatched.txt preverb1 records that remain unmatched (17)

mwverbs1_unmatched.txt  mwverbs1 records that are not used in matching.

pw_mw_map_edit.txt  spelling correspondences used in matching.



3859 3576  simple join of prefix and root
4024 3411  i + vowel
4043 3392  u + vowel
4101 3334  a + a
* upasargamap
Generate the prefixed forms for the preverb1 records
Read all the upasargas in preverb1, and normalize them to  U1 + U2 , etc.

python upasargamap.py preverb1.txt upasargamap.txt

* preverb3
Generate full prefixed verb forms from preverb1_mw
python preverb3.py preverb1_mw.txt mwverbs1.txt preverb3.txt

* problem with pw=dar in preverb1_mw.txt

NOTE: This change made in preverb3.txt
dar:49037&49038:anu,apa,ava,vyava,A,ud,ni,nis,pari,pra,aBipra,prati,vi,udvi,pravi~A,atyA,pratyA,samA df:95065:verb:6Ā:
Should be two records:
dar:49037:anu,apa,ava,vyava,A,ud,ni,nis,pari,pra,aBipra,prati,vi,udvi,pravi dF:95496:verb:9P,2P,2Ā:

dar:49038:A,atyA,pratyA,samA df:95065:verb:6Ā:


* pw_keydoc_input.txt
python make_keydoc_input.py preverb3.txt pw_keydoc_input.txt

The output file is used in hwnorm2/keydoc/distinctfiles/

* pw_norm_extra   NOT USED
python make_norm_extra.py preverb3.txt pw_norm_extra.txt

The output file is used in 
 hwnorm2/keydoc/distinctfiles/pw_norm_extra.txt
Note: pw_mw_map_edit.txt is also used here.

* mw_norm_extra  
python make_norm_extra_mw.py preverb3.txt mw_norm_extra.txt

The output file is used in 
 hwnorm2/keydoc/distinctfiles/mw_norm_extra.txt
