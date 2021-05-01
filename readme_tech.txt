dictlist.txt  list of dictionary codes used in iterations. (05-01-2021)
  This file is in hwnorm2 (top level of repository).
  
keydoc/distincthws/redo.sh
 cd keydoc/distincthws
 sh redo_all_hws.sh
  # for each $dict in $dictlist
   sh redo_one_hw.sh $dict
    $digfile = ../../../csl-orig/v02/$dict/$dict.txt
    $hwfile = data/$dict_hws.txt
    python hws.py $dict $digfile $hwfile
    # Note first parm ($dict) is not currently used.(05-01-2021)
    # Example python hws.py mw ../../../csl-orig/v02/mw/mw.txt temp_mw_hws.txt
 # data/xxx_multi.txt
   The term 'keydoc' is intended to imply that each document for a
   dictionary may be specified by a set of headword spellings.
   In xxx.txt, distinct records have distinct L-numbers. Each record
   also has a 'k1' headword spelling.  The default documents are
   indexed by distinct values of 'k1'.
   When there is an xxx_multi.txt file for xxx, some documents are
   the union of 2 or more default documents.
   Note: the term 'xxx_multi' indicates that this file contains documents
     which are defined by multiple headwords.
   A line of xxx_multi.txt is a list of values (comma-delimited): e.g. X,Y,Z
   It should be true:
    a. values on a line are in xxx_hws.txt (e.g., that
       X is a k1 value in xxx,txt, and also Y and Z.
    b. values on a line are distinct (e.g., X and Z are different)
    c. values in two lines are distinct. (e.g., X does not appear in two lines)
 # data/mw_multi.txt
   The HxB, HxC markup of mw.txt is used to compute mw_multi.txt.
   sh redo_mw_multi.sh
   # python mw_multi.py mw ../../../csl-orig/v02/mw/mw.txt data/mw_multi.txt
 # Other dictionaries with multi files.
 # these additional multi files are generated along with hwextra files by:
 sh redo_all_hwextras.sh
  #for each dictionary in dictlist:
   sh redo_one_hwextra.sh $dict
  # digdir="../../../csl-orig/v02/${dict}"
  # infile="$digdir/${dict}_hwextra.txt"
  # outfile="data/${dict}_hwextra.txt"
  # hwfile="data/${dict}_hws.txt"
  # multifile="data/${dict}_multi.txt"
  python hw_extra.py $dict $hwfile $infile $outfile $multifile
  # recreates both $outfile and $multifile
  # Note: This is skipped for $dict==mw.
  # Example: python hw_extra.py acc data/acc_hws.txt  ../../../csl-orig/v02/acc/acc_hwextra.txt data/acc_hwextra.txt data/acc_multi.txt
  # Idea of hw_extra.py.  Suppose k1 is an alternate headword from
    csl-orig/v02/xxx/xxx_hwextra.txt; let k1P be its 'parent'
    Two possibilities:
     a. k1 is ALSO a headword in xxx_hws.txt:
      k1,k1P is written to xxx_multi.txt
      k1 k1P is written to local xxx_hwextra.txt COMMENTED OUT
     b. k1 is NOT a headword in xxx_hws.txt (This is usually true)
      k1 k1P is written to local_xxx_hwextra.txt
  
  # counts of multi files
  wc -l data/*_multi.txt
  7831 data/mw_multi.txt
  1083 data/acc_multi.txt
    30 data/ap90_multi.txt
    24 data/skd_multi.txt
   219 data/vcp_multi.txt
  9187 total
 # counts of hwextra files
 wc -l data/*_hwextra.txt
 1592 data/acc_hwextra.txt
  437 data/ap90_hwextra.txt
    1 data/bur_hwextra.txt
    1 data/cae_hwextra.txt
  335 data/skd_hwextra.txt
 1764 data/vcp_hwextra.txt
 4130 total
 # NOTE:  There is currently no provision for 'manual' additions to
  xxx_multi.txt. 
 # This ends the discussion of keydoc/distincthws/redo.sh
 
-----------------------------------------------------------------------
Scripts in hwnorm2. We assume that keydoc/distincthws/redo.sh is up to date.

redo_one_all.sh  
 for each dictionary $dict in dictlist.txt:
  redo_one.sh $dict
   $digfile = ../../csl-orig/v02/$dict/$dict.txt 
   $keydoc1 = data/$dict/keydoc1.txt
   $keyx = ../../csl-orig/v02/$dict/$dict_hwextra.txt
   # $keydoc1  distinct headwords, special logic for MW (e.g. guru,gurvI)
   # keydoc1 format: 1 or 2 tab-delimited fields
   #  field 1 = dochws = list (comma-delimited) of dictionary headwords
   #          that defines a document of the dictionary. Normally, just one
   #          headword. But e.g. guru,gurVI  in MW may be multiple headwords
   #  field 2 = docptrs = list (comma-delimited) pointers to document
   python keydoc1.py $dict $digfile $keydoc1
   # $keydoc1x adds alternate headwords from hwextra in second 'tab' field.
   python keydoc1x.py $dict $keydoc1 $keyx $keydoc1x 
   $normdistinct = "distinctfiles/${dict}_norm_extra.txt"
    # Another independent file in keydoc is $normdistinct. It may be absent.
    # If present, each line is of form 
    # normdistinct format:
    # 2 fields per line (separated by colon, space, or tab), called
    #   'key' and 'norm'
   python norm.py $dict $keydoc1x $normdistinct $norm 
    #  step1: construct list normrecs of (key,norm) pairs
    #         for each record of keydoc1x, form a list of all key spellings  
    #         present as either one of dochws or docptrs
    #         for each key, compute its normalized spelling 'norm'.
    #         if the 'norm' spelling differs from key, add (key,norm) to normrecs
    # step2:  construct normextra as list of (key,norm) pairs in normdistinct
    # step3:  Join lists normrecs and normextra.
    # step4:  Write these key,norm pairs to $norm
   $keydocnorm = data/$dict/keydoc_norm.txt
    # format:  1 field or 2 tab-delimited fields (like $keydoc1)
   python keydoc_norm.py $dict $keydoc1x $norm $keydocnorm
    # read all the (dochws, docptrs) pairs of $keydoc1x into recs/
    # read all the (key,norm) pairs of $norm into dictionary normd[key]=norm
    # For each rec in recs, add additional spellings to docptrs:
    #   for each key in rec.dochws or rec.docptrs,
    #    if normd[key] is new to docptrs or dochws, add it to docptrs.
    # Write out the modified 'recs' to $keydocnorm.
  # redo_one.sh $dict  is now done.  The result is $keydocnorm.
 
redo_merge.sh
 cd keydoc
 python keydoc_merge.py 
 # 1. construct to Python dictionaries, drecs and dd
 # For each Sanskrit dictionary dictlo in (internal) dictlist,
     1a. read all the records (recs)
     1b. construct Python dictionary d so that for each record (rec) in recs,
         and for each hw in rec.dochws or rec.docptrs,
         d[hw] is a list and rec is in d[hw]
     1c. drecs[dictlo] = recs
         dd[dictlo] = d
 # 2. Construct hw2dict, a Python dictionary, whose keys are
     all the headword spellings hw
     and whose value hw2dict[hw] is the list of dictionary codes
     such that hw in rec.dochws+rec.docptrs for some rec in drecs[dictlo].
 # 3. For each dictionary dictlo and for each rec in drecs[dictlo],
     extend rec.docptrs (Function otherptrs):
     for any hw in rec.dochws + rec.docptrs:
      for any dictionary dictlo1 other than dictlo 
        and any document rec1 in dictlo1 pointed to by hw
        and any pointer in dictlo1 to rec1:
          add hw1 to rec.docptrs.
 # 4. For each dictionary dictlo write its modified records to
      data/$dict/keydoc_merge.txt.
# redo_final_all.sh
 cd keydoc
 #1. for all $dictlo:
     sh redo_final_one.sh
     $keydoc = "$dir/keydoc.txt"
     python keydoc2.py $dict $keydocmerge $keydoc   
     # if two documents in $keydocmerge have a common word
     #   among the two dochws and docptrs,
     # then the two documents are replace by a third document,
     # Whose dochws is the union of the two dochws
     # and whose docptrs contains the union of the two docptrs MINUS
     #  the union of the new dochws.
     #  Further, this is recursive.
Example with ap90:
two inputs keydoc_merge.txt
aMhriH	aMhri
aMGri	aMhriH,aNGri,aMhri,aNGriH
new record in keydoc.txt
aMhriH,aMGri	aMhri,aNGri,aNGriH

 #2. keydocinput="$dir/keydoc_input.txt"
     keydocinput1="distinctfiles/${dict}_keydoc_input.txt"
     python keydoc_input.py $keydoc $keydocinput1 $keydocinput
