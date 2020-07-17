_one_all.sh  
 for each dictionary $in the list of dictionaries,
  redo_one.sh $dict
   cd keydoc
 
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
