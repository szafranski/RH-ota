git checkout master &&
git pull &&
git fetch &&
git checkout no_pdf_included && 
git pull &&
git fetch &&
git merge master -m "new functions and fixes" && 
git pull &&
git add . &&
git push &&
git commit -m "new functions and fixes" -a && 
git push && 
git checkout master && 
git merge no_pdf_included -m "new functions and fixes" && 
git fetch &&
git push &&
git checkout master 