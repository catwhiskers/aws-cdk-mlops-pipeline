git clone codecommit://train-scikit_bring_your_own
cp -R repository/train/* train-scikit_bring_your_own/
cd train-scikit_bring_your_own/
git add .
git commit -am "trigger training job"
git push origin master 
