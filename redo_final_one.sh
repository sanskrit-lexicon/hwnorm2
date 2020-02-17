dict=$1
cd keydoc
dir="data/$dict"

keydocmerge="$dir/keydoc_merge.txt"
if [ ! -f "$keydocmerge" ]
 then
  echo "redo_final_one.sh fails as $keydocmerge not found"
  exit 1
fi
keydoc="$dir/keydoc.txt"
python keydoc2.py $dict $keydocmerge $keydoc

keydocinput="$dir/keydoc_input.txt"
keydocinput1="distinctfiles/${dict}_keydoc_input.txt"
python keydoc_input.py $keydoc $keydocinput1 $keydocinput

cd ../
