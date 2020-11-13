echo "config credentials for codecommit on cloud9"
git config --global credential.helper '!aws codecommit credential-helper $@' 
git config --global credential.UseHttpPath true


echo "install typescript"
npm i -g typescript


