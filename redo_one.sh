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
keydoc1="$dir/keydoc1.txt"
hwfile="distincthws/data/${dict}_hws.txt"
multifile="distincthws/data/${dict}_multi.txt"
python keydoc1.py $dict $hwfile $multifile $keydoc1

keydoc1x="$dir/keydoc1x.txt"
keyx="distincthws/data/${dict}_hwextra.txt"
python keydoc1x.py $dict $keydoc1 $keyx $keydoc1x

keydocnorm="$dir/keydoc1x_norm.txt"
echo "Compute $keydocnorm"
python keydoc1x_norm.py $dict $keydoc1x $keydocnorm

keydocnorm1="$dir/keydoc1x_norm1.txt"
echo "Compute $keydocnorm1"
multidir="distinctfiles/data"
# use all distinctfiles/data/multi_*.txt files
python keydoc1x_norm1.py $dict $keydocnorm $multidir $keydocnorm1

echo "END redo_one.sh for $dict"
