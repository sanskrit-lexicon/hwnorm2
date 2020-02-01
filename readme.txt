
sh redo.sh M
  (M = cologne or xampp)
 sh redo_one_all.sh    # creates documents, and normalizations
 sh redo_merge.sh      # merges all the normalizations
 sh redo_final_all.sh  # revises documents
 sh redo_sqlite_all.sh M # prepares keydoc.sqlite files, moves to web/sqlite


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
