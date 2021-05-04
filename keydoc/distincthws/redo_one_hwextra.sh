dict=$1
echo "BEGIN distincthws/redo_one_hw.sh for $dict"
digdir="../../../csl-orig/v02/${dict}"
infile="$digdir/${dict}_hwextra.txt"
outfile="data/${dict}_hwextra.txt"
hwfile="data/${dict}_hws.txt"
multifile="data/${dict}_multi.txt"
if [ $dict = "mw" ]
then
 echo "construct $multifile"
 digfile="$digdir/${dict}.txt"
 python mw_multi.py $dict $digfile $multifile
else
 echo "Try to construct $outfile $multifile"
 python hw_extra.py $dict $hwfile $infile $outfile $multifile
fi

