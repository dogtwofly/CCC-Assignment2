git clone -v https://github.com/dogtwofly/xanthic.git
cd ~/xanthic/service
curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
sudo apt install nodejs
npm install
sudo npm install -g forever
forever start app.js
