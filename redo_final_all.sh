for dictlo in  acc ap90 ben   bhs bop bur cae \
 ccs gra gst ieg inm  krm mci md mw mw72 \
 pe pgn pui    pw pwg sch shs skd \
 snp stc vcp vei wil  yat ap pd
do
 #dictup="${dictlo^^}"
 echo "dictionary=$dictlo"
 sh redo_final_one.sh $dictlo
done
