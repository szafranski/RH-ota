git checkout master && 
git add . &&
git commit -m "new functions and fixes" -a && 
git push && 
git checkout no_pdf_included && 
git merge origin -m "new functions and fixes" && 
git checkout master