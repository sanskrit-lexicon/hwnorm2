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
 sh redo_sqlite_all.sh $which # prepares keydoc.sqlite files, moves to web/sqlite
