dictlist=`cat ../../dictlist.txt`
for dict in $dictlist
do
 sh redo_one_hw.sh $dict
done
