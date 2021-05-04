dictlist=`cat dictlist.txt`
for dict in $dictlist
do
 cd keydoc   
 sh redo_one.sh $dict
 cd ../
done
