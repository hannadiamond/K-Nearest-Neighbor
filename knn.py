import random
import sys
import math
import instance

def Distance(testItem, trainingList, k, distanceFunction):
	tupleList = []
	predictedLabel = []
	predictedLabelCount = []
	testLabel = testItem.Getlabel()

	#for Hamming Distance
	if distanceFunction == "H":
		testListString = testItem.GetlistString()
		for instance in trainingList:
			#get distance
			distance = 0
			trainListString = instance.GetlistString()
			for i in range(0, len(trainListString)):
				if trainListString[i] != testListString[i]:
					distance += 1
			#find and keep only the smallest k distances
			if len(tupleList) < k:
				tup = (instance, distance)
				tupleList.append(tup)
			else :
				tup = (instance, distance)
				tupleList.append(tup)
				tupleList.sort(key=lambda tup: tup[1])
				tup2 = tupleList.pop()
	#for euclidian distance
	if distanceFunction == "E":
		testListNum = testItem.GetlistNum()
		for instance in trainingList:
			#get distance
			x = 0
			trainListNum = instance.GetlistNum()
			for i in range(0, len(testListNum)):
				x += (trainListNum[i]-testListNum[i])*(trainListNum[i]-testListNum[i])
			distance = math.sqrt(x)
			#find and keep only the smallest k distances
			if len(tupleList) < k:
				tup = (instance, distance)
				tupleList.append(tup)
			else :
				tup = (instance, distance)
				tupleList.append(tup)
				tupleList.sort(key=lambda tup: tup[1])
				tup2 = tupleList.pop()

	#Get labels and number of times it was seen
	for t in tupleList:
		if len(predictedLabel) == 0:
			predictedLabel.append(t[0].label)
			predictedLabelCount.append(1)
			continue
		for i in range(0, len(predictedLabel)):
			if predictedLabel[i] == t[0].label:
				predictedLabelCount[i] = predictedLabelCount[i] + 1
				continue
			if i == len(predictedLabel)-1 and predictedLabel[i] != t[0].label:
				predictedLabel.append(t[0].label)
				predictedLabelCount.append(1)
	#Get label that was predicted the most
	index = 0
	maxNum = 0
	for i in range(0, len(predictedLabelCount)):
		if predictedLabelCount[i] > maxNum:
			maxNum = predictedLabelCount[i]
			index = i

	tup = (predictedLabel[index], testLabel)
	return tup

def preprocessInstance(inputList):
	inst = instance.Instance(inputList)
	inst.process()
	return inst

def main():
	completeList = []
	shuffledCompleteList = []
	trainingList = []
	testList = []
	tupleList = []
	matrixLabel = []
	matrixCount = []
	label = []
	dic = {}
	accuracyNum = 0

	userInput = sys.argv
	fileLocation = sys.argv[1]
	distanceFunction = sys.argv[2]
	k = int(sys.argv[3])
	percent = float(sys.argv[4])
	seed = int(sys.argv[5])

	#open file and process data
	dataFile = open(fileLocation, "r")
	next(dataFile)
	for line in dataFile:
		arr = line.split(",")
		completeList.append(preprocessInstance(arr))
	dataFile.close()

	#shuffle list
	random.seed(seed)
	shuffledCompleteList = list(completeList)
	random.shuffle(shuffledCompleteList)

	#create training and test sets
	trainingSetNum = math.ceil(len(shuffledCompleteList) * percent)
	cur = 0;
	for i in range(0, len(shuffledCompleteList)):
		if cur < trainingSetNum:
			trainingList.append(shuffledCompleteList[i])
			cur+=1
		else:
			testList.append(shuffledCompleteList[i])

	#run distance function on test list
	for item in testList:
		tup = Distance(item, trainingList, k, distanceFunction)
		if tup[0] == tup[1]:
			accuracyNum +=1
		#count the number of time predicted/actual label pairs occured
		if len(matrixLabel)==0:
			matrixLabel.append(tup)
			matrixCount.append(1)
		else:
			for i in range(0, len(matrixLabel)):
				matrixTup = matrixLabel[i]
				if matrixTup[0] == tup[0] and matrixTup[1] == tup[1]:
					matrixCount[i] = matrixCount[i] + 1
					break
				if i == len(matrixLabel)-1:
					matrixLabel.append(tup)
					matrixCount.append(1)

	#add all possible labels to figure out matrix
	for i in range(0, len(matrixLabel)):
		matrixTup = matrixLabel[i]
		matrixTupLabelZero = matrixTup[0]
		matrixTupLabelOne = matrixTup[1]
		zero = False
		one = False
		for i in range(0, len(label)):
			if label[i] == matrixTupLabelZero:
				zero = True
			if label[i] == matrixTupLabelOne:
				one = True
		if 	matrixTupLabelZero == matrixTupLabelOne and zero == False:
			label.append(matrixTupLabelZero)
		else:
			if zero == False:
				label.append(matrixTupLabelZero)
			if one == False:
				label.append(matrixTupLabelOne)

    #make it easy to get label index using dictionary
	for i in range(0, len(label)):
		dic[label[i]] = i

	#build confusion matrix
	row, col = len(label), len(label);
	matrix = [[0 for x in range(row)] for y in range(col)]
	for i in range(0, len(matrixLabel)):
		tup = matrixLabel[i]
		predicted = tup[0]
		actual = tup[1]
		count = int(matrixCount[i])
		predictedIndex = dic[predicted]
		actualIndex = dic[actual]
		matrix[actualIndex][predictedIndex] = count

	#print out confusion matrix
	s = ""
	for lab in label:
		s += lab + ","
	print(s+ "\n")
	for row in range(0, len(label)):
		s = ""
		for col in range(0, len(label)):
			s += str(matrix[row][col]) + ","
			if col == len(label)-1:
				s+= label[row]
		print(s + "\n")

	accuracy = float(accuracyNum)/len(testList)
	print(accuracy)


if (__name__ == "__main__"):
    main();
