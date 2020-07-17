dict="mw"
echo "BEGIN distincthws/redo_mw_multi.sh"
digdir="../../../csl-orig/v02/${dict}"
digfile="$digdir/${dict}.txt"
hwfile="data/${dict}_multi.txt"
python mw_multi.py $dict $digfile $hwfile
