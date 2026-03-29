
readme.txt for hwnorm2 repo. Revised 03-28-2026.
This documents the steps to recreate keydoc/keydoc_glob1.sqlite
which is used by csl-apidev/sample/dalglob1.php.
For further documentation, see
readme_20250505.txt, readme_previous.txt, readme_tech.txt

-------------------------------------------------
* local (xampp) update
cd /c/xampp/htdocs/cologne/hwnorm2/
# Add new dictionary codes, if any, to dictlist.txt.
cd keydoc/distincthws
sh redo.sh
# remake keydoc/keydoc_glob1.sqlite for local installation
cd /c/xampp/htdocs/cologne/hwnorm2/
sh redo.sh xampp
# --------------------
push revised hwnorm2 repo to github.

-------------------------------------------------
* Cologne (xampp) update
# connect to cologne server
# cd to hwnorm2 repo
git pull
# remake keydoc/keydoc_glob1.sqlite for cologne installation
sh redo.sh cologne



