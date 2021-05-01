
keydoc/distincthws/redo.sh
 This needs to be redone only when new headwords appear in some digitizations
 cd keydoc/distincthws
 sh redo.sh
   sh redo_all_hws.sh
     #for each dictionary $dict listed,
     #create keydoc/distincthws/data/${dict}_hws.txt 
   sh redo_mw_multi.sh
   sh redo_all_hwextras.sh


redo.sh (in top level of hwnorm2)
sh redo.sh M
  (M = Machine = cologne or xampp)
 sh redo_one_all.sh    # creates documents, and normalizations
 sh redo_merge.sh      # merges all the normalizations
 sh redo_final_all.sh  # revises documents
 #redo_sqlite_all.sh was used in prior versions. 
 #sh redo_sqlite_all.sh M # prepares keydoc.sqlite files, moves to web/sqlite
 # redo_glob1.sh used as of 
 sh redo_glob1.sh     # 

sh redo_one_all.sh
  creates data/xxx/keydoc_norm.txt for all dictionaries xxx 
  with sanskrit headwords
  (excludes ap, pd)

sh redo_merge.sh
 creates data/xxx/keydoc_merge.txt for all dictionaries xxx
 'merges' the various data/xxx/keydoc_norm.txt dictionaries

sh redo_final_one.sh xxx 
 creates data/xxx/keydoc.txt from data/xxx/keydoc_merge.txt

sh redo_final_all.sh
 runs redo_final_one.sh for all xxx

sh redo_sqlite_one.sh xxx M
  (M = cologne or xampp)
 cd keydoc
 creates data/xxx/keydoc_input.txt from data/xxx/keydoc.txt
 creates keydoc.sqlite from data/xxx/keydoc_input.txt 
 moves keydoc.sqlite to ../../$dict/web/sqlite/

sh redo_sqlite_all.sh M
  (M = cologne or xampp)
