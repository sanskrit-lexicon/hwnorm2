which=$1  # cologne or xampp
if [ $which = "cologne" ]
 then
  echo "we are at cologne"
elif [ $which = "xampp" ]
 then
  echo "we are in local installation"
else
 echo "redo_sqlite_all.sh: error unknown parameter: '$which'"
 exit 1
fi
for dictlo in  acc ap90 ben ap pd  bhs bop bur cae \
 ccs gra gst ieg inm  krm mci md mw mw72 \
 pe pgn pui    pw pwg sch shs skd \
 snp stc vcp vei wil  yat
do
 sh redo_sqlite_one.sh $dictlo $which
done
