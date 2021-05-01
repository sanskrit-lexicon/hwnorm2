dict=$1
echo "BEGIN distincthws/redo_one_hw.sh for $dict"
digdir="../../../csl-orig/v02/${dict}"
digfile="$digdir/${dict}.txt"
hwfile="data/${dict}_hws.txt"
python hws.py $dict $digfile $hwfile
