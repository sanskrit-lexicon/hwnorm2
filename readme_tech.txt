dictlist.txt  list of dictionary codes used in iterations. (05-01-2021)
  This file is in hwnorm2 (top level of repository).

--------------------------------------------------------------------------
keydoc/distincthws/redo.sh
 cd keydoc/distincthws
 sh redo.sh
  # this runs 2 scripts:
  1. sh redo_all_hws.sh
   # For each $dict, construct data/$dict_hws.txt from digitization $dict.txt
  2. sh redo_all_hwextras.sh
   # For each $dict, construct data/$dict_multi.txt and $dict_hwextra.txt,
     where possible.
  # Now discuss each of these steps
  step 1: sh redo_all_hws.sh
   # for each $dict in $dictlist
   sh redo_one_hw.sh $dict
    input: $digfile = ../../../csl-orig/v02/$dict/$dict.txt
    output:  $hwfile = data/$dict_hws.txt
    python hws.py $dict $digfile $hwfile
    # Note first parm ($dict) is not currently used.(05-01-2021)
    # Example python hws.py mw ../../../csl-orig/v02/mw/mw.txt data/mw_hws.txt
    # Note: program assures that the headwords in $hwfile are distinct.
  step 2: sh redo_all_hwextras.sh
   # for each $dict in dictlist:
   sh redo_one_hwextra.sh $dict
   # digdir="../../../csl-orig/v02/${dict}"
   # infile="$digdir/${dict}_hwextra.txt"
   # outfile="data/${dict}_hwextra.txt"
   # hwfile="data/${dict}_hws.txt"
   # multifile="data/${dict}_multi.txt"
   if $dict == mw:
    # digfile="$digdir/${dict}.txt"
    python mw_multi.py $dict $digfile $multifile
    # recreates  $multifile (for mw, assume no hwextra)
    # example: H1 guru, H1B gurvI, H2 gurvI -> guru,gurvI
   else:
    python hw_extra.py $dict $hwfile $infile $outfile $multifile
    # recreates both $outfile and $multifile
    # Example: python hw_extra.py acc data/acc_hws.txt  ../../../csl-orig/v02/acc/acc_hwextra.txt data/acc_hwextra.txt data/acc_multi.txt

  step 2: sh redo_all_hwextras.sh
   DISCUSS the constructed multi and hwextra files for dict != mw
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
   At this stage of construction, it is NOT known that xxx_multi.txt records
   satisfy these properties!
  # Idea of hw_extra.py.  Suppose k1 is an alternate headword from
    csl-orig/v02/xxx/xxx_hwextra.txt; let k1P be its 'parent'.
    (Thus, k1 is an alternate spelling of k1P).
    Two possibilities:
     a. k1 is ALSO a headword in xxx_hws.txt:
      k1P,k1 is written to xxx_multi.txt;
       We will consider records k1 and k1P in xxx.txt to be
         in the same 'document'
      k1P k1 is written to local xxx_hwextra.txt COMMENTED OUT
     b. k1 is NOT a headword in xxx_hws.txt (This is usually true)
      k1P k1 is written to local xxx_hwextra.txt
      We consider k1 to be an additional pointer to document containing
      record k1P.
      NOTE 05-03-2021: In distincthws/data/acc_hwextra.txt,
       we have 'akzapAda akzacaraRa', so aczacaraRa is pointer to akzapAda
       in acc. However, keydoc_merge.py (See below) uses this to merge
       documents in other dictionaries; notably, mw dictionary has
       records for both headwords, and the pairing in acc_hwextra.txt
       causes the two mw records to be merged.  Subtle!
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
Scripts in hwnorm2. We assume that keydoc/distincthws/redo.sh is up to date,
as discussed above.

redo_one_all.sh  
 for each dictionary $dict in dictlist.txt:
  cd keydoc
  redo_one.sh $dict
   Step 1 of redo_one.sh: construct keydoc/data/$dict/keydoc1.txt
   # $keydoc1  distinct headwords (e.g. guru,gurvI)
   # keydoc1 format: 1 or 2 tab-delimited fields
   #  field 1 = dochws = list (comma-delimited) of dictionary headwords
   #          that defines a document of the dictionary. Normally, just one
   #          headword. But e.g. guru,gurVI  based on $multifile..
   #  field 2 = docptrs = list (comma-delimited) pointers to document
   $hwfile = keydoc/distincthws/data/$dict_hws.txt
   $multifile = keydoc/distincthws/data/$dict_multi.txt
   $keydoc1 = keydoc/data/$dict/keydoc1.txt
   python keydoc1.py $dict $hwfile $multifile $keydoc1
   
   Step 2 of redo_one.sh: construct keydoc/data/$dict/keydoc1x.txt
   # $keydoc1x adds alternate headwords from hwextra in second 'tab' field.
   # These alternates are added to field 2; i.e.,
   #  if k1 is an alternate to k1P (from hwextra) and
   #  k1P is in dochws of document D, then k1 is added to docptrs of D.
   $hwextra =  distincthws/data/$dict_hwextra.txt
   $keydoc1x = keydoc/data/$dict/keydoc1x.txt
   python keydoc1x.py $dict $keydoc1 $hwextra $keydoc1x
   
   step 3 of redo_one.sh: construct keydoc/data/$dict/keydoc1x_norm.txt
   python keydoc1x_norm.py $dict $keydoc1x $keydocnorm
   $keydocnorm = keydoc/data/$dict/keydoc1x_norm.txt
   # for each record R in $keydoc1x, normalize each key in R.dochws and
   # in R.docptrs; the result is a list R.normptrs.
   # Now, it may be that for some other record S, there are common elements
   # in R.normptrs and S.normptrs.  In this case we replace R with
   # a merged record, and discard S.
   # This process is repeated until there is no commonality between
   #  the normptrs of any two records.
   # Finally, we write the new records;  for a record R, write
   # R.dochws and R.normptrs.
   Example:  (from ap90)
     R = aMga:aMga:aNga  (dochws:docptrs:normptrs)
     S = aMgaM:aMgaM:aNga
     Merge: aMga,aMgaM:aNga   (dochws:normptrs)

   step 4 of redo_one.sh: construct keydoc/data/$dict/keydoc1x_norm1.txt
    $keydocnorm1="$dir/keydoc1x_norm1.txt"
    $multidir="distinctfiles/multi"
    python keydoc1x_norm1.py $dict $keydocnorm $multidir $keydocnorm1
    
    # Example: python keydoc1x_norm1.py mw data/mw/keydoc1x_norm.txt distinctfiles/data data/mw/keydoc1x_norm1.txt
    
    # Revise the document records of $dict/keydoc1x_norm.txt, based on
    # ALL the extra multi files for $dict; these files are
    # distinctfiles/data/multi_X.txt for some X.
    # These are headword equivalences (not necessarily normalized).
    # They are obtained by various means.
    # 05-02-2021: Currently only 2 files:
    #  multi_verb.txt  equivalent spellings of verbs in various dictionaries
    #  multi_test.txt  Sample records. First is 'Bizaj,Bizak,Bizag'
    #  Using just multi_test.txt with $dict=mw,  data/mw/keydoc1x_norm1.txt
    #  merges 3 records of data/mw/keydoc1x_norm.txt into 1 record:
    #   Bizaj\t'Bizaj, Bizak\t'Bizak, Bizag\t'Bizag,   ->
    #    Bizaj,Bizak,Bizag\tBizaj,Bizak,Bizag
    #  With dictionary BUR, we get
    #   Bizaj\t'Bizaj -> Bizaj,Bizak,Bizag\tBizaj,Bizak,Bizag

------------------------------------------------------------------------------
redo_merge.sh
 cd keydoc
 python keydoc_merge.py ../dictlist.txt
 # Use hwnorm2/dictlist.txt for list of dictionaries.
 # 1. Read each data/$dict/keydoc1x_norm1.txt;
 # 2. merge the results (see below for further description)
 # 3. Write data/$dict/keydoc_merge.txt file for each $dict.
 In more detail ...
 # 1. Construct two data structures, drecs and dd, which are
   such that
   drecs[$dict] = list of all records in data/$dict/keydoc1x_norm1.txt
    Each record consists of two lists:
    a. dochws :  the headwords (k1) comprising a document for $dict
    b. docptrs:  various normalized spellings associated with the document
   dd[$dict] is a dictionary whose keys comprise all dochws and docptrs.
      It is the 'inverted index' of the records; i.e.,
      dd[$dict][X] is a list of all records R in drecs[$dict] such that
         X is in R.dochws or in R.docptrs.
 # 2. Construct hw2dict, a Python dictionary, whose keys are
     all the headword spellings hw
     and whose value hw2dict[hw] is the list of dictionary codes $dict
     such that hw in R.docptrs for some R in drecs[$dict].
 # 3. For each dictionary $dict and for each R in drecs[$dict],
     extend R.docptrs (Function otherptrs):
     for any hw in R.docptrs:
      for any dictionary $dict1 in hw2dict[hw] other than $dict 
        and any document R1 in dd[$dict1][hw]
        and any hw1 in R1.docptrs:
          add hw1 to R.docptrs.
 # 4. For each dictionary $dict, look for pairs of records R1 and R2
      in drecs[$dict] such that R1.docptrs and R2.docptrs have common
      elements; mark R2 as a duplicate, and merge R2.dochws into R1.dochws,
      and merge R2.docptrs into R1.docptrs2.
      Do this recursively until the remaining non-duplicates have no overlap.
 # 5. For each dictionary $dict write its modified records non-duplicate
      records to data/$dict/keydoc_merge.txt.
      
# redo_final_all.sh
 for all $dict in dictlist,
  cd keydoc
  sh redo_final_one.sh $dict
  step 1:
   # $merge=data/$dict/keydoc_merge.txt
   # $ptrs=distinctfiles/$dict_keydoc_ptrs.txt
     Note: format is hw<tab>p1,p2,   p1, p2, etc are
     pointers  to hw for dictionary. e.g.,
     - Example from pw_keydoc_ptrs.txt
       akz<TAB>nirakz,samaka are prefixed verbs of verb akz
       Note: Program normalizes 'hw' and p1,p2 
     
   # $final=data/$dict/keydoc_final.txt
   python keydoc_finalptrs.py $merge $ptrs $final
   # add additional ptrs for dictionary (think sub-headwords)
  step 2:
   # $keydocinput=data/$dict/keydoc_input.txt  (inverted index of $final)
   python keydoc_input.py $final $keydocinput
   # Discussion
   The output file $keydocinput is an inverted index; i.e.,
   It contains two tab-delimited fields:
    field1 = normalized headword
    field2 = a comma-delimited list of (non-normalized) headwords which
             comprise a document.


-----------------------------------------------------------------------
------- 05-02-2021: DELETE MATERIAL BELOW ??? ----------------------------------
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
 
