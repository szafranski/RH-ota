cd ~/RH-ota
git status
git add .
git commit -m "new functions and fixes" -a
git push
git checkout no_pdf_included
git status
git merge master -m "updated with master"
git push
git checkout master

