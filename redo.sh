which=$1
if [ $which = "cologne" ]
 then
  echo "we are at cologne"
elif [ $which = "xampp" ]
 then
  echo "we are in local installation"
else
 echo "redo.sh error unknown parameter: '$which'"
 exit 1
fi
 sh redo_one_all.sh    # creates documents, and normalizations
 sh redo_merge.sh      # merges all the normalizations
 sh redo_final_all.sh  # revises documents
 # 7/14/2020.  We don't need these individual keydoc.sqlite files.
 #sh redo_sqlite_all.sh $which # prepares keydoc.sqlite files, moves to web/sqlite
 # sh redo_glob.sh  This not currently needed (02-06-2020)
 sh redo_glob1.sh
