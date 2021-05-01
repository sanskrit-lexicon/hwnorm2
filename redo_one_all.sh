dictlist=`cat dictlist.txt`
for dict in $dictlist
do
 sh redo_one.sh $dictlo
done
