#Name:		Will Hicks
#CLID:		wsh7290
#Course:	CMPS 420-Artificial Intelligence
#Professor:	Dr. Mark G. Radle
#Assignment:	Genetic Algorithm
#DueDate:	March 18, 2015
#DueTime:	10:00 AM

#I certify that this is completely an entirely my own work



###IMPORTING LIBRARIES


import random 
import re  #  Regular Expression Library
import math



### CLASSES ####
class Chromosome:
	def _init_(self):
		self.name = ''
		self.bitPattern = ''
		self.fitnessValue = 0
		self.fitnessRatio = 0
		self.rangeMin = 0
		self.rangeMax = 0


### FUNCTIONS  ####

# Find Population size
def calcPopSize(numDVars, prop):
     if(numDVars == 1):
         return 2;
     else:
         popSize = numDVars // prop
         if(popSize % 2 == 1):
             popSize = popSize + 1
         return popSize;

#Select random chromosome for reproduction
def selectMate(liChromObj):
	problemDetected = False
	rangeNum = round(random.uniform(0.0, 99.9), 1)
	#print("Random Range = ",rangeNum, '\n')



	for chromObj in liChromObj:
		#print("This is the chromosomes range ",chromObj.rangeMin, '-',chromObj.rangeMax)
		if(chromObj.rangeMin <= rangeNum < chromObj.rangeMax):
			return chromObj;

	#if it doesn't find any chromosomes in the range, then we got a problem, so handle it
	problem = Chromosome()
	problem.name = "I'm not supposed to exist"
	problemDetected = True
	if(problemDetected):
		print("#########WE GOT A PROBLEM OVER HERE in SELECTMATE FUNCTION")
		print("This is the range num it picked", rangeNum)
		for chromObj in liChromObj:
			print("This is the chromosomes range ",chromObj.rangeMin, '-',chromObj.rangeMax)
			
	return problem;	


#Open File
def openCNFFile(fileName):
	inFile = open(fileName, "r")
	CNF = inFile.readline()
	inFile.close()

	CNF = CNF.rstrip('\n')

	return CNF;

 
def GeneticAlgorithm():
	random.seed()

	#open the file that contains example CNF inputs for the Genetic Algorithm

	###FOR LANCE, in case you have a different file

	#fileName = input("Please enter the file name that contains the CNF: ")
	#CNF = openCNFFile(fileName)

	CNF = openCNFFile("GA.input")
	
	# Reformat the CNF so it's easy to parse

	#remove any newline characters, parentheses, and white space
	originalCNF = CNF
	CNF = CNF.replace('(', '').replace(')', '').replace(' ', '')

	#print("This is the CNF without parentheses or whitespace: ",CNF)
	#print()

	


	###FIND DISTINCT VARIABLES(NUMBER OF GENES)

	#using the imported regular expression libray, whittle down the CNF to only the single letter variables
	liDistinctVars = re.split('\W+', CNF)

	#Set returns an unordered list of unique subsets, so let's reorder it alphabetically
	liDistinctVars = sorted(list(set(liDistinctVars)))

	#print("This is the list of distinct variables: ", liDistinctVars, "\n")



	# The fitness value is the number of disjuncts in the given CNF.  Our Goal is to
	# find a member of the population in which all of their disjuncts evaluate to true,
	# and thus are equal to the total amount of disjuncts in the original CNF
	disjCNF = CNF.split('*')
	FV = len(disjCNF)

	print("Goal Fitness Value = ",FV,"\n")

	# Number of Genes/Bits(size of chromosome)
	numDistinctVars = len(liDistinctVars)
	numOfGenes = numDistinctVars

	print("The number of bits/genes in each chromosome = ", numOfGenes, "\n")

	# Population size is usually number of bits, but play with the size to
	# see what converges faster.  As per Dr. Radle's suggestion, the size of the population should be half or a quarter
	# the number of distinct variables
	# Note: You always want an even population number for reproduction's sake

	if(numDistinctVars > 0 or numDistinctVars < 16):
	    popSize = calcPopSize(numDistinctVars, 2)
	elif(numDistinctVars >=16 or numDistinctVars <= 26):
	    popSize = calcPopSize(numDistinctVars, 4)

	print("This is the population size: ", popSize, "\n")



	# Alright let's make an initial random population that is the first generation
	# Let's make an array to hold the size of the population
	# and put in each element the random chromosome

	#Initialize an array of empty Chromosome objects
	arrChromObj= []

	for i in range(popSize):
	    x = Chromosome()
	    arrChromObj.append(x)

	# For each member of the population, create a random bit pattern
	for i in range(popSize):
	    chromosomeBP = ""
    
	    for gene in range(numOfGenes):
        	chromosomeBP += str(random.randrange(0, 2))

	    #place the chromsome in the array
	    arrChromObj[i].bitPattern = chromosomeBP


	#Iterate through each member of the population until you find one that has a fitness value
	#that matches our goal fitness value.  When this happens.  The function will return.

	#Translate the CNF so it can be evaluated by python's function eval
	CNF = CNF.replace('!',' not ').replace('+', ' or ')

	#Initialize some variables
	fVMatches = 0
	oldPopTotalFV = 0
	generationNum = 0

	#Infinite Loop until solution is found
	while(True):
		#output what generation we're currently on
		print("\nGeneration Number =", generationNum,"\n")
		
		#Start the total FV out at zero
		popTotalFV = 0

		chromNum = 1

		for chromosome in arrChromObj:
			chromosome.name = "C" + str(chromNum) # Start off with C1, not C0
			tempCNF = CNF
			outputIfSuccess = ""
    
			#print("This is the chromosome that breaks",chromosome.name)
			for i in range(0, numOfGenes):
				varLetter = liDistinctVars[i]
				#print("This is i = ", i)
				#print("This is the letter variable", varLetter)
				bitValue = chromosome.bitPattern[i]
				#print("this is the bitvalue: ", bitValue)
				# Let's remember the truth values in case it's a solution
				outputIfSuccess += varLetter + '=' + bitValue + '\n'
				tempCNF= tempCNF.replace(varLetter, bitValue)

			tempCNF = tempCNF.split('*')

			#print("This is the tempCNF that will have each element in it evaluated:\n ", tempCNF, '\n')

			# Evaluate the fitness value of each member of the population.  Fitness value is how many disjuncts evaluate to 			true.  The fittest member is the one closest to the total number of disjuncts
			
			chromFV = 0

			for disjunctValue in tempCNF:
				chromFV += eval(disjunctValue)
			chromosome.fitnessValue = chromFV
    
			#print("This is how many truth values chromosome", chromosome.name + "(" + chromosome.bitPattern + ")", "yielded: ", chromFV)

			#If the chromosome's fitness value is equal to our GOAL fitness Value, we might as well stop what we're
			#doing because we've found a solution! No use in doing extra work
			if(FV == chromFV):
				#output the truth values
				if(generationNum == 0):
					print("We found a solution in a randomly populated member of our first generation ")

				print("We found a solution.  Here's the bit pattern of the solution followed by the truth values\n")
				print("Chromosome Bit Pattern = \n", chromosome.bitPattern)
				print(outputIfSuccess)

				#Exit the program
				return;

		        
        		
			#If we haven't found a success yet, we'll have to determine it's fitness ratio for reproduction selection
			popTotalFV += chromFV
		
			chromNum += 1


		###CHECK FOR PLATEAU EFFECT ####
		if(popTotalFV == oldPopTotalFV):
			fVMatches += 1
			if(fVMatches > 5):
				print("Plateua effect detected\n")
				#Mutate one member of the population
				memberMutatorNum = random.randrange(0, popSize)
				geneMutatorNum = random.randrange(0, numOfGenes)
				bPList = list(arrChromObj[memberMutatorNum].bitPattern)

				bPList[geneMutatorNum] = '0' if (bPList[geneMutatorNum] == 1) else '1'
				
				arrChromObj[memberMutatorNum].bitPattern = ''.join(bPList)

				###REPEAT(FIX For cleaner code)

				#Subtract the old FV from the total
				popTotalFV -= arrChromObj[memberMutatorNum].fitnessValue
				tempCNF = CNF
				outputIfSuccess = ""
    
				for i in range(0, numOfGenes):
					varLetter = liDistinctVars[i]
					#print("This is the letter variable", varLetter)
					bitValue = arrChromObj[memberMutatorNum].bitPattern[i]
					#print("this is the bitvalue: ", bitValue)
					outputIfSuccess += varLetter + '=' + bitValue + '\n'
					tempCNF= tempCNF.replace(varLetter, bitValue)

				tempCNF = tempCNF.split('*')

				#print("This is the tempCNF that will have each element in it evaluated:\n ", tempCNF, '\n')

				# Evaluate the fitness value of each member of the population.  Fitness value is how many disjuncts evaluate to 			true.  The fittest member is the one closest to the total number of disjuncts
			
				chromFV = 0

				for disjunctValue in tempCNF:
					chromFV += eval(disjunctValue)
				arrChromObj[memberMutatorNum].fitnessValue = chromFV

				popTotalFV += chromFV
    
				#print("This is how many truth values chromosome", chromosome.name + "(" + chromosome.bitPattern + ")", "yielded: ", chromFV)

				#If the chromosome's fitness value is equal to our GOAL fitness Value, we might as well stop what we're
				#doing because we've found a solution!
				if(FV == chromFV):
					#output the truth values
					print(outputIfSuccess)
					#Exit the program
					return;

				#Reset the number of matches
				fVMatches = 0
				
		oldPopTotalFV = popTotalFV




	   ###CALCULATE FITNESS RATIO of each chromosome for reproduction selection###
		rangeStart = 0

		for i in range(len(arrChromObj)):
			FR = float((arrChromObj[i].fitnessValue / popTotalFV) * 100)
			arrChromObj[i].fitnessRatio = FR
			#print("This is the fitness ratio", arrChromObj[i].fitnessRatio)
			arrChromObj[i].rangeMin = rangeStart
			arrChromObj[i].rangeMax = rangeStart + FR
			#print("This is the chromosomes range ",arrChromObj[i].rangeMin, '-',arrChromObj[i].rangeMax)
			rangeStart += FR

		# Print Header
		print("{0:24} {1:16}{2:20}{3:20}{4:10}".format("Chromosome Name", " Genes", "Fitness Value", "Fitness Ratio", "Range"))
		print()

		for chromObj in arrChromObj:

			stringRange = str(round(chromObj.rangeMin, 2)) + "-" + str(round(chromObj.rangeMax, 2))
        
			print("{0:20}{1:16}{2:8}{3:16.2f}{4:10}".format(chromObj.name,chromObj.bitPattern,chromObj.fitnessValue,chromObj.fitnessRatio,"               " + stringRange))






           ###REPRODUCE###
		totalNumReproductions = popSize / 2

		reprodCount = 0
		chromosomeCount = 1
		newGen = []

		while(reprodCount <= totalNumReproductions):
			#pick a pair of chromosomes for crossover reproduction

			maleChrom = selectMate(arrChromObj)
			femaleChrom = selectMate(arrChromObj)

			#you don't want it mating with itself
			while(maleChrom.name == femaleChrom.name):
				femaleChrom = selectMate(arrChromObj)
	
			#print("The male member of the population selected for reproduction is\n", maleChrom.name)
			#print("The female member of the population selected for reproduction is\n", femaleChrom.name)


			##Select crossover point
			randXoverPnt = random.randrange(1, numOfGenes)  
			#print("This is the index of crossover ", randXoverPnt)
	
			lHSMale = maleChrom.bitPattern[0:randXoverPnt]
			rHSMale = maleChrom.bitPattern[randXoverPnt: numOfGenes]

			lHSFemale = femaleChrom.bitPattern[0:randXoverPnt]
			rHSFemale = femaleChrom.bitPattern[randXoverPnt: numOfGenes]
			

			offspring1 = Chromosome()
			offspring1.name = "C" + str(chromosomeCount)
			offspring1.bitPattern = lHSMale + rHSFemale

			newGen.append(offspring1)
	
			offspring2 = Chromosome()
			offspring2.name = "C" + str(chromosomeCount)
			offspring2.bitPattern = rHSMale + lHSFemale

			#print("This is the bit pattern for offspring 1",offspring1.bitPattern)
			#print("This is the bit pattern for offspring 2",offspring2.bitPattern)
			chromosomeCount += 2

			newGen.append(offspring2)

			reprodCount +=1
	
		#Replace old generation with new generation and repeat for next generation until solution is found
		arrChromObj = newGen
		generationNum += 1

		if(generationNum > 150):
			print("\nThe CNF: \n\n", "'" +  originalCNF + "'","\n\n has no solution\n")
			return;
		

###MAIN########
GeneticAlgorithm()

    	
