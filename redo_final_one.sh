dict=$1
cd keydoc
dir="data/$dict"

keydocmerge="$dir/keydoc_merge.txt"
if [ ! -f "$keydocmerge" ]
 then
  echo "redo_final_one.sh fails as $keydocmerge not found"
  exit 1
fi
#keydoc="$dir/keydoc.txt"
#python keydoc2.py $dict $keydocmerge $keydoc

keydocinput="$dir/keydoc_input.txt"
keydocinput1="distinctfiles/${dict}_keydoc_input.txt"
#python keydoc_input.py $keydoc $keydocinput1 $keydocinput
# July 13, 2020.  The Search keys are always normalized.
# This means, that in usage, we require that the caller compute
# normalized spelling.
# 7/14/2020. For now, not clear that distinctfiles/xxx_keydoc_input.txt
# is what is needed (e.g. prefixed verb pointers for pw)
# So, put a non-existent file here.
keydocinput1="distinctfiles/absent_${dict}_keydoc_input.txt"
python keydoc_input.py $keydocmerge $keydocinput1 $keydocinput

cd ../
