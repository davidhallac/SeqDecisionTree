import numpy as np
import pandas as pd
import os
import math
import sys
from sklearn import tree

#LOAD DATA
# posData = np.loadtxt('/dfs/scratch0/david/FengCollab/PositiveExamples.txt')

# print posData.shape

# neg = []

# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029718095811051522.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720709734858753.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720710154289153.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720710254952449.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720710288506881.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720710691160065.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720754379030529.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720783118401538.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720788084457473.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720809945169922.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720811471896577.csv'))
# neg.append(np.loadtxt('/dfs/scratch0/david/FengCollab/NegativeData/NegativeExamples_2029720812260425729.csv'))


posData = np.random.rand(100,1000)

neg = [np.random.rand(100,1000)]

for item in neg:
	print item.shape


#For each candidate, find the information gain
igMax = -1
igVal = -1

for j in range(70208):

	#Compute IG



