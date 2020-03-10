git checkout master && 
git add . &&
git commit -m "new functions and fixes" -a && 
git push && 
git checkout no_pdf_included && 
git merge master/no_pdf_included -m "new functions and fixes" && 
git checkout master