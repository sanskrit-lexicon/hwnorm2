dict=$1
which=$2    # xampp or cologne
cd keydoc
dir="data/$dict"
keydoc="$dir/keydoc.txt"
keydocinput="$dir/keydoc_input.txt"
if [ ! -f "$keydoc" ]
 then
  echo "redo_sqlite_one fails as $keydoc not found"
  exit 1
fi
python keydoc_input.py $keydoc $keydocinput
cp keydoc.sql $dir
cd $dir  # descend so keydoc.sql works
sqlite="keydoc.sqlite"
if [ -f $sqlite ]
 then
  rm $sqlite
 fi

sqlite3 $sqlite < keydoc.sql
echo "finished remaking $sqlite"
chmod 0755 $sqlite
cd ../../
pwd
if [ $which = "cologne" ]
 then
  dictup="${dict^^}"
  webdir="../../${dictup}Scan/2020/web/sqlite/"
  echo "we are at cologne"
  
elif [ $which = "xampp" ]
 then
  webdir="../../$dict/web/sqlite/"
else
 echo "redo_sqlite_one.sh error unknown parameter: '$which'"
 exit 1
fi

mv "$dir/$sqlite" $webdir
echo "moved $dir/$sqlite TO $webdir"
echo "finished redo_sqlite_one.sh $dict"
