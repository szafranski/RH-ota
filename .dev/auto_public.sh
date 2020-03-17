git pull
cd ~/RH-ota
git status
git add .
git commit -a
git push
git checkout no_pdf
git pull
git status
git merge master -m "up-to-date with master"
git push
git checkout master
git status