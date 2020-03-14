cd ~/RH-ota
sudo rm -r ~/RH-ota-bup
git checkout master
git add .
git commit -m "features and fixes"
git push
sudo cp -r ~/RH-ota ~/RH-ota-bup
git checkout no_pdf_included
cd ~
sudo rm -r ~/RH-ota-bup/.git
sudo cp -r ~/RH-ota-bup/* ~/RH-ota/
sudo cp ~/RH-ota-bup/* ~/RH-ota/
cd ~/RH-ota
sudo rm -r how_to
git add .
git commit -m "features and fixes"
git push
git checkout master
