cd keydoc
dir="dataglob"
if [ ! -d "$dir" ]
 then
  mkdir $dir
 fi
cp keydoc_glob.sql $dir/
glob="$dir/keydoc_glob.txt"
python keydoc_glob.py $glob
cd $dir  # descend so keydoc.sql works
sqlite="keydoc_glob.sqlite"
if [ -f $sqlite ]
 then
  rm $sqlite
 fi

sqlite3 $sqlite < keydoc_glob.sql
echo "finished remaking $sqlite"
chmod 0755 $sqlite
mv $sqlite ../

