cd keydoc
dir="dataglob"
if [ ! -d "$dir" ]
 then
  mkdir $dir
 fi
cp keydoc_glob1.sql $dir/
glob1="$dir/keydoc_glob1.txt"
python keydoc_glob1.py $glob1
cd $dir  # descend so keydoc.sql works
sqlite="keydoc_glob1.sqlite"
if [ -f $sqlite ]
 then
  rm $sqlite
 fi

sqlite3 $sqlite < keydoc_glob1.sql
echo "finished remaking $sqlite"
chmod 0755 $sqlite
mv $sqlite ../

