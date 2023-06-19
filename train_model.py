from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from pickle import dump

df = pd.read_csv('training_data.csv')
print(df)
print(df.iloc[:, :-1].values, df['mode'].values)
X = df.iloc[:, :-1].values
y = df['mode'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = MLPClassifier(solver='lbfgs')

clf.fit(X, y)
score = int(clf.score(X_test, y_test)*100)
print(score)

print(clf.predict([
    [0.5, 2, 1, 1]
]))
with open('model.pkl', 'wb') as f:
    dump(clf, f)
