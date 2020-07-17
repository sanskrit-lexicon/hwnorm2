
To redo everything:
 sh redo.sh

Only required when some change in a metaline of some dictionary.

* sh redo_one_hw.sh xxx
 Generates file of distinct headwords, using 
 digitization csl-orig/v02/xxx/xxx.txt.
 Output file name is data/xxx_hws.txt
* sh redo_all_hws.sh
  runs sh redo_one_hw.sh xxx for all xxx in a list of dictionaries

* sh redo_one_hwextra.sh xxx
  (for all xxx except mw)
 Uses file csl-orig/v02/xxx/xxx_hwextra.txt.   
 and also uses data/xxx_hws.txt  (the distinct headwords of xxx).
 If this file present and has entries, then generates files 
  data/xxx_hwextra.txt and data/xxx_multi.txt.
 If this file absent or empty, deletes 
  data/xxx_hwextra.txt and data/xxx_multi.txt.
 The records of csl-orig/v02/xxx/xxx_hwextra.txt are parsed into two
  headwords: 
  k1P : the 'parent' headword; it should be in xxx_hws.txt.
        Program generates an ERROR if k1P is NOT in xxx_hws.txt.
  k1  : the alternate spelling of k1P.
  There are two cases:
  Case 1: 'k1' is also a headword (in xxx_hws.txt).  
    a. Write k1P,k1  (comma-separated) to xxx_multi.txt
    b. Write ;k1P k1 (space-separated, preceded by ';') to xxx_hwextra.txt
       The initial ';' is interpreted as a comment
  Case 2: 'k1' is NOT a headword.
    a. Write k1P k1 (space-separated) to xxx_hwextra.txt
  Also uses  data/xxx_hws.txt to verify that 'x' is indeed a headword of xxx.

 
* sh redo_all_hwextras.sh
  runs sh redo_one_hwextra.sh xxx for all xxx in a list of dictionaries
  which EXCLUDES mw.
* data/mw_multi.txt
 sh redo_mw_multi.sh
 Generates list of records defining multi-headword documents for mw.
 Based on csl-orig/v02/xxx/xxx.txt.  Examples are like guru,gurvI.
 As of this writing, 7831 multi-headword documents are generated.

We may discover multi-headword documents for other dictionaries, as time goes
by.


* --------------------------------------------------------------
Note on xxx_multi.txt files.
These contain comma-delimited lists of headwords which are in the same
document.  They are determined in various ways.
1. mw  : sh redo_mw_multi.sh   (see above)
2. ap90 :  The keydoc1x program does some pre-analysis of
   extra headwords. For example, 'mahar mahas' indicates that a certain
   entry for 'mahar' indicates that 'mahas' is an alternate
   spelling for mahar.   
   This, and several other examples, have the further distinction
   that there is an additional entry for one or both of these; in this
   case there is an entry for mahas with additional senses.
   In such cases, we consider 'mahas,mahar' to be one document, containing
   all the entries of the dictionary with headword either mahas or mahar.
  The keydoc1x.py program generates comments identifying such cases.
  For example:
addx warning: alternate headword already found: mahas mahar ['mahas'] []

