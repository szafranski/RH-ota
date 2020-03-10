git checkout no_pdf_included && 
git add . &&
git commit -m "new functions and fixes" -a && 
git push && 
git fetch &&
git checkout master && 
git merge no_pdf_included -m "new functions and fixes" && 
git pull &&
git fetch &&
git checkout master
