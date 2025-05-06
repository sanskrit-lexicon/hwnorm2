dict=$1
#cd keydoc
dir="data/$dict"

merge="$dir/keydoc_merge.txt"
if [ ! -f "$merge" ]
 then
  echo "redo_final_one.sh fails as $merge not found"
  exit 1
fi

ptrs="distinctfiles/${dict}_keydoc_ptrs.txt"
final="$dir/keydoc_final.txt"
python3 keydoc_finalptrs.py $merge $ptrs $final
# keydoc_input.py constructs an inverted index from $final
keydocinput="$dir/keydoc_input.txt"
python3 keydoc_input.py $final $keydocinput
