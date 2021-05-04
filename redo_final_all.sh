dictlist=`cat dictlist.txt`
for dict in $dictlist
do
 echo "dictionary=$dict"
 cd keydoc
 sh redo_final_one.sh $dict
 cd ../
done
