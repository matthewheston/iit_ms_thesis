import numpy as NP
import MySQLdb as SQL
from sklearn import cross_validation, grid_search
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn import preprocessing
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

cxn = SQL.connect('', '', '', '')
c = cxn.cursor()

# include other features by updating this SELECT statement
c.execute('SELECT merged, user_activity, comments_on_pr, reputation FROM feature_set')
results = c.fetchall()

# 'num_rows' needed to reshape the 1D NumPy array returend by 'fromiter'
# in other words, to restore original dimensions of the results set
num_rows = int(c.rowcount)

# recast this nested tuple to a python list and flatten it so it's a proper iterable:
x = map(list, list(results))              # change the type
x = sum(x, [])                            # flatten

X = NP.fromiter(x, dtype=int, count=-1)

X = X.reshape(num_rows, -1)

split = NP.hsplit(X, (0,1))
y = split[1].flatten()
X = split[2]
X = X.astype(float)
X_log = NP.log1p(X)
X_scaled = preprocessing.scale(X_log)



print 'LogisticRegression model'
clf = LogisticRegression(class_weight="auto")
print 'avg accuracy=%.3f' % NP.average(cross_validation.cross_val_score(clf, X_scaled, y, cv=10, scoring='accuracy'))
print 'avg precision=%.3f' % NP.average(cross_validation.cross_val_score(clf, X_scaled, y, cv=10, scoring='precision'))
print 'avg recall=%.3f' % NP.average(cross_validation.cross_val_score(clf, X_scaled, y, cv=10, scoring='recall'))


print 'DecisionTree model'
clf = DecisionTreeClassifier()
print 'avg accuracy=%.3f' % NP.average(cross_validation.cross_val_score(clf, X_scaled, y, cv=10, scoring='accuracy'))
print 'avg precision=%.3f' % NP.average(cross_validation.cross_val_score(clf, X_scaled, y, cv=10, scoring='precision'))
print 'avg recall=%.3f' % NP.average(cross_validation.cross_val_score(clf, X_scaled, y, cv=10, scoring='recall'))

print 'SVMmodel'
clf = svm.SVC(class_weight="auto")
print 'avg accuracy=%.3f' % NP.average(cross_validation.cross_val_score(clf, X_scaled, y, cv=10, scoring='accuracy'))
print 'avg precision=%.3f' % NP.average(cross_validation.cross_val_score(clf, X_scaled, y, cv=10, scoring='precision'))
print 'avg recall=%.3f' % NP.average(cross_validation.cross_val_score(clf, X_scaled, y, cv=10, scoring='recall'))
