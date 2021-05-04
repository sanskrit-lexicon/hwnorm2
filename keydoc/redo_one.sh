dict=$1
echo "BEGIN redo_one.sh for $dict"
#cd keydoc
if [ ! -d "data" ]
 then
  mkdir data
 fi
dir="data/$dict"
if [ ! -d "$dir" ]
 then
  mkdir $dir
fi
# step 1
keydoc1="$dir/keydoc1.txt"
hwfile="distincthws/data/${dict}_hws.txt"
multifile="distincthws/data/${dict}_multi.txt"
python keydoc1.py $dict $hwfile $multifile $keydoc1

# step 2
keydoc1x="$dir/keydoc1x.txt"
hwextra="distincthws/data/${dict}_hwextra.txt"
python keydoc1x.py $dict $keydoc1 $hwextra $keydoc1x

# step 3
keydocnorm="$dir/keydoc1x_norm.txt"
echo "Compute $keydocnorm"
python keydoc1x_norm.py $dict $keydoc1x $keydocnorm

# step 4
keydocnorm1="$dir/keydoc1x_norm1.txt"
echo "Compute $keydocnorm1"
multidir="distinctfiles/multi"
# use all ${multidir}/multi_*.txt files
python keydoc1x_norm1.py $dict $keydocnorm $multidir $keydocnorm1

echo "END redo_one.sh for $dict"
