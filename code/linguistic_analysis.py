import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation, grid_search
from sklearn.linear_model import LogisticRegression

csv_file = csv.DictReader(open("merged_and_comments.tsv", "r"), delimiter="\t", quotechar='"')
x = []
y = []
for line in csv_file:
    x.append(line["comments"])
    y.append(line["new_merged"])

vec = CountVectorizer(ngram_range=(1,2), binary=True)
x = vec.fit_transform(x)
y = np.array(y, dtype=float)

clf = LogisticRegression()
print 'avg accuracy=%.3f' % np.average(cross_validation.cross_val_score(clf, x, y, cv=10, scoring='accuracy'))
print 'avg precision=%.3f' % np.average(cross_validation.cross_val_score(clf, x, y, cv=10, scoring='precision'))
print 'avg recall=%.3f' % np.average(cross_validation.cross_val_score(clf, x, y, cv=10, scoring='recall'))

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
print 'avg accuracy=%.3f' % np.average(cross_validation.cross_val_score(clf, x, y, cv=10, scoring='accuracy'))
print 'avg precision=%.3f' % np.average(cross_validation.cross_val_score(clf, x, y, cv=10, scoring='precision'))
print 'avg recall=%.3f' % np.average(cross_validation.cross_val_score(clf, x, y, cv=10, scoring='recall'))

clf = LogisticRegression()
clf.fit(x,y)
top_indices = clf.coef_[0].argsort()[::-1]
vocab_r = dict((idx, word) for word, idx in vec.vocabulary_.iteritems())
print 'merged words:\n', '\n'.join(['%s=%.3f' % (vocab_r[idx], clf.coef_[0][idx]) for idx in top_indices[:20]])
top_indices = clf.coef_[0].argsort() # sort in increasing order
print '\n\nnotmerged words:\n', '\n'.join(['%s=%.3f' % (vocab_r[idx], clf.coef_[0][idx]) for idx in top_indices[:20]])
