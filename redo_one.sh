dict=$1
echo "BEGIN redo_one.sh for $dict"
cd keydoc
if [ ! -d "data" ]
 then
  mkdir data
 fi
dir="data/$dict"
if [ ! -d "$dir" ]
 then
  mkdir $dir
 fi
digdir="../../csl-orig/v02/$dict"
digfile="$digdir/$dict.txt"
if [ ! -f "$digfile" ]
 then
 echo "redo_one.sh : $digfile not found"
 exit 1
fi
keydoc1="$dir/keydoc1.txt"
python keydoc1.py $dict $digfile  $keydoc1

keydoc1x="$dir/keydoc1x.txt"
keyx="$digdir/${dict}_hwextra.txt"
python keydoc1x.py $dict $keydoc1 $keyx $keydoc1x

norm="$dir/norm.txt"
normdistinct="distinctfiles/${dict}_norm_extra.txt"
python norm.py $dict $keydoc1x $normdistinct $norm 

keydocnorm="$dir/keydoc_norm.txt"
python keydoc_norm.py $dict $keydoc1x $norm $keydocnorm

echo "END redo_one.sh for $dict"
