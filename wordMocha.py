from spellchecker import SpellChecker
spell = SpellChecker()

def listener():
	userIn = input('Letters: ')
	while(userIn.lower() != 'done'):
		if (len(userIn) == 7):
			formatOutput(spell.known(twoDtoStrings(solveForSeven(userIn))))
		if (len(userIn) == 6):
			formatOutput(spell.known(twoDtoStrings(solveForSix(userIn))))
		if (len(userIn) == 5):
			formatOutput(spell.known(twoDtoStrings(solveForFive(userIn))))
		if (len(userIn) == 4):
			formatOutput(spell.known(twoDtoStrings(solveForFour(userIn))))
		if (len(userIn) == 3):
			formatOutput(spell.known(twoDtoStrings(solveForThree(userIn))))

		userIn = input('Letters: ')


def twoDtoStrings(twolist):
	final = []
	temp = ''
	for stringList in twolist:
		for character in stringList:
			temp += character.lower()
		final.append(temp)
		temp = ''
	return final

def printList(listToPrint):
	final = ''
	for word in listToPrint:
		final += word + ' '

	return final
def formatOutput(englishList):
	threeWords = []
	fourWords = []
	fiveWords = []
	sixWords = []
	allLists = []
	for word in englishList:
		if (len(word) == 3):
			threeWords.append(word)
		if (len(word) == 4):
			fourWords.append(word)
		if (len(word) == 5):
			fiveWords.append(word)
		if (len(word) == 6):
			sixWords.append(word)
	allLists.append(threeWords)
	allLists.append(fourWords)
	allLists.append(fiveWords)
	allLists.append(sixWords)
	for length in range(3,7):
		print ('Words with', length, 'letters\n')
		print(printList(allLists[length - 3]) + '\n')
	return 'Thanks for playing!'


def swap(twoElements):

	temp = twoElements[1]
	twoElements[1] = twoElements[0]
	twoElements[0] = temp
	return twoElements


def solveForOne(letter):
	return letter


def solveForTwo(letters):
	
	final = []
	
	final.append(list(letters))
	final.append(list(swap(letters)))
	
	return final



def solveForThree(letters):
	pairs = []
	final = []

	for letter in letters:
		temp = list(letters)
		temp.remove(letter)
		
		pairs.append(solveForTwo(temp))
		for pair in pairs:
			
			for two in pair:

				two.append(letter)
				final.append(two)
		temp = []
		pairs = []
		#final.append()
	
	return final

def solveForFour(letters):
	threes = []
	final = []
	for letter in letters:
		temp = list(letters)
		temp.remove(letter)
		
		threes.append(solveForThree(temp))
		for three in threes:
			
			for nums in three:
				
				tempThree = list(nums)
				final.append(tempThree)
				nums.append(letter)
				final.append(nums)
		temp = []
		threes = []
	
	return final

def solveForFive(letters):
	fours = []
	final = []
	for letter in letters:
		temp = list(letters)
		temp.remove(letter)
		fours.append(solveForFour(temp))
		for fourList in fours:
			for four in fourList:
				tempFour = list(four)
				final.append(tempFour)
				four.append(letter)
				final.append(four)
		temp = []
		fours = []
	
	return final

def solveForSix(letters):
	fives = []
	final = []
	for letter in letters:
		temp = list(letters)
		temp.remove(letter)
		fives.append(solveForFive(temp))
		for fiveList in fives:
			for five in fiveList:
				tempFive = list(five)
				final.append(tempFive)
				five.append(letter)
				final.append(five)
		temp = []
		fives = []
	
	return final

def solveForSeven(letters):
	sixes = []
	final = []
	for letter in letters:
		temp = list(letters)
		temp.remove(letter)
		sixes.append(solveForSix(temp))
		for sixList in sixes:
			for six in sixList:
				tempSix = list(six)
				final.append(tempSix)
				five.append(letter)
				final.append(six)
		temp = []
		sixes = []
	
	return final
	
def combos(letters,final):
	letters = list(letters)
	if (len(letters) < 2):
		print('given letters are too short')
		return 
	if (len(letters) == 2):
		print ('found two letters', letters)
		final.append(list((letters)))
		final.append(list(swap(letters)))
		return final

	for letter in letters:
		print ('letter:', letter)
		
		currentOthers = list(letters)

		print ('CurrentOthers before remove:', currentOthers)


		currentLetter = letter
		print ('currentLetter:', currentLetter)


		currentOthers.remove(letter)
		print('CurrentOthers after remove:',currentOthers)
		
		print ('final before recursive call:', final)


		final.append(combos(currentOthers,final))
		
		tempFinal = list(final)
		for finalCombo in tempFinal:
			
			finalCombo.append(letter)
			print ('finalCombo with current letter:', finalCombo)
			
			
			
			final.append(list(finalCombo))

		tempFinal = []
		'''for currentCombo in final:
			final.append(currentCombo.append(currentLetter))
		'''
	print ('final final')
	return final


		
'''
		else:
			combos(temp,currentLetter,final)
		for 
'''


#print (combos('abc',[]))
listener()
#recursiveTest (0,10)
#print (solveLoops('hello'))
#print ([1,2,3].remove(2))
