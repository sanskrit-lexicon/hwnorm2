cd keydoc
dir="dataglob"
if [ ! -d "$dir" ]
 then
  mkdir $dir
fi
glob1="$dir/keydoc_glob1.txt"
echo "redo_glob1: Construct $glob1"
python keydoc_glob1.py $glob1
# 05-01-2021.  Create sqlite file with Python
sqlite="keydoc_glob1.sqlite"
echo "redo_glob1: construct $sqlite"
python make_glob1_sqlite.py $glob1 $sqlite
# uncertain about this 'permission' step
chmod 0755 $sqlite
# done!
#cp keydoc_glob1.sql $dir/
#cd $dir  # descend so keydoc.sql works
#if [ -f $sqlite ]
# then
#  rm $sqlite
# fi

#sqlite3 $sqlite < keydoc_glob1.sql
#echo "finished remaking $sqlite"
#chmod 0755 $sqlite
#mv $sqlite ../

