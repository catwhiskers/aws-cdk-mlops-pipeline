git clone codecommit://build-scikit_bring_your_own
cp -R repository/build/* build-scikit_bring_your_own/
cd build-scikit_bring_your_own/
git add .
git commit -am "trigger training job"
git push origin master 

