import numpy as np
import scipy as sp
import pandas as pd
import os
import math
import sys
from sklearn import tree
import pydot
from sklearn.externals.six import StringIO 


# #LOAD DATA
posData = np.loadtxt('/dfs/scratch0/david/FengCollab/PositiveExamples.txt')

print posData.shape

neg = []

neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029718095811051522.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720709734858753.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720710154289153.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720710254952449.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720710288506881.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720710691160065.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720754379030529.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720783118401538.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720788084457473.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720809945169922.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720811471896577.csv'))
neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720812260425729.csv'))


# posData = np.random.rand(500,1008)

# neg = [np.random.rand(500,1008), np.random.rand(100,1008), np.random.rand(100,1008), np.random.rand(100,1008)
# , np.random.rand(100,1008), np.random.rand(100,1008), np.random.rand(100,1008), np.random.rand(100,1008)
# , np.random.rand(100,1008), np.random.rand(100,1008), np.random.rand(100,1008), np.random.rand(100,1008)]




negData = np.concatenate((neg[0],neg[1],neg[2],neg[3],neg[4],neg[5],neg[6],neg[7],neg[8],neg[9],neg[10],neg[11]), axis=0)
posLength = posData.shape[0]
negLength = negData.shape[0]

p = float(posLength)/float(posLength+negLength)
binEntropy = -p*math.log(p) - (1-p) * math.log(1-p)
print "Original Entropy is", binEntropy*(posLength+negLength), posLength, negLength

#For each candidate, find the information gain
entMin = 99999999999
entFeat = -1
entSplit = -1

for j in range(70208):

	#Compute IG
	posex = posData[:,j]
	negex = negData[:,j]
	posSort = np.sort(posex)
	negSort = np.sort(negex)

	posCount = 0
	negCount = 0

	val = min(posSort[0], negSort[0])

	while(True):
		a = sum(i <= val for i in posSort)
		b = sum(i <= val for i in negSort)

		# print a, b
		tot = max(a + b,0.1)
		rest = max(posLength + negLength - a - b,0.1)
		p1 = float(a)/float(tot)
		p2 = float(posLength - a) / float(rest)

		p1 = max(0.0001, min(p1, 0.9999))
		p2 = max(0.0001, min(p2, 0.9999))

		entropy = tot* (-p1*math.log(p1) - (1-p1) * math.log(1-p1)) + rest* (-p2*math.log(p2) - (1-p2) * math.log(1-p2))

		if (entropy < entMin):
			entMin = entropy
			entFeat = j
			entSplit = val
			print "New min entropy is", entMin, entFeat, entSplit, p1, a, p2, b

		if (math.isnan(val)):
			break
		elif (a < posLength and b < negLength):
			val = min(posSort[a], negSort[b])
		elif(a < posLength):
			val = posSort[a]
		elif(b < negLength):
			val = negSort[b]
		else:
			break

	print "Done with", i, "Min entropy is", entMin, entFeat, entSplit, p1, a, p2, b



	# X = np.concatenate((posex, negex), axis=0)

	# X = X.reshape(-1, 1)
	# Y = [np.zeros(posLength+negLength)]
	# Y = [1] * posLength + [0] * negLength
	# clf = tree.DecisionTreeClassifier()
	# clf = clf.fit(X, Y)

	# if (j == 100):
	# 	with open("iris.dot", 'w') as f:
	# 		f = tree.export_graphviz(clf, out_file=f)
	# 		dot_data = StringIO() 
	# 		tree.export_graphviz(clf, out_file=dot_data) 
	# 		graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
	# 		graph.write_pdf("iris.pdf") 



