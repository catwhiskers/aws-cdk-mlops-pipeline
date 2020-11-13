git clone codecommit://deploy-scikit_bring_your_own
cp -R repository/deploy/* deploy-scikit_bring_your_own/
cd deploy-scikit_bring_your_own/
git add .
git commit -am "trigger deploy job"
git push origin master
