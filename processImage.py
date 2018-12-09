import os
import numpy as np
import imutils
import cv2
import sys
import math

import wordMocha
#ML TO DETERMINE LIKLINESS THAT WORD IS ENGLISH
'''
Colin Chen October 2018

Take a screenshot from wordMocha (eventually run in app?)

Template match each letter
Find all possible words with those letters

'''
#display an image
'''import cv2

pathUnForm = 'C:/Users/colin/coding/wordMochaSolver/alphabet/'
pathForm = 'C:/Users/colin/coding/wordMochaSolver/alphabetFormat/'
pathScreenshot = 'C:/Users/colin/coding/wordMochaSolver/screenshots/'
'''
pathUnForm = str(os.getcwd()) + '/alphabet/'
pathForm = str(os.getcwd()) + '/alphabetFormat/'
pathScreenshot = str(os.getcwd()) + '/screenshots/'
def display (title, img):
	cv2.imshow(title, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
#testImage = cv2.imread('C:/Users/colin/wordMochaRepo/wordMochaSolver/alphabet/A.png',cv2.IMREAD_GRAYSCALE)
#display ('pathTest',testImage )
#letters from black to white
#format a single image (go to black and white)
def distance(point1, point2):
	return math.sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2) )
def findInList(searchList,value):
	index = -1
	indicies = []
	while(True):
		try:
			index = searchList.index(value, index+1)
		except ValueError:
			return indicies
		indicies.append(index)

def formatLetter(img): 
	
	
	blur = cv2.GaussianBlur(img,(5,5),0)
	ret, letter = cv2.threshold(blur, 145, 255, cv2.THRESH_BINARY)
	reblur = cv2.GaussianBlur(letter,(5,5),0)
	template = cv2.Canny(reblur,50,200)
	(tHeight,tWidth) = template.shape[:2]
	return reblur

def formatSeveral(img):
	threshToTry = [100,110,120,130,140,150,160,170,180,190,200]

	processedImages = {}
	blur = cv2.GaussianBlur(img, (5,5), 0)
	for threshold in threshToTry:
		ret, letter = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
		display(str(threshold), letter)
		#print (letter)

		processedImages[threshold] = letter
	return processedImages

def formatScreen(img):

	blur = cv2.GaussianBlur(img,(5,5),0)
	ret, letter = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
	return letter
#save a single image
def saveImages(imageName,image,pathDest):
	try:
		cv2.imwrite(os.path.join(pathDest,imageName), image)
		print('Save successful')
	except:
		print ('Save failed')

#format and save all images from alphabet to alphabetFormat
def formatAll(path,pathDest):
	for im in os.listdir(path):
		fullPath = path + '/' + str(im)#full image path
		image = cv2.imread(fullPath,cv2.IMREAD_GRAYSCALE)#get image from full image path
		
		
		#display (str(im), formatLetter(image)) #display image
		saveImages(str(im), formatLetter(image),pathDest) #save image #name = str(im), 

#get the letters from a screenshot
def formatScreenshot(imagePath,screenshotPos):
	#image[startRow:endRow, startCol:endCol]
	image = cv2.imread(imagePath + '/' + os.listdir(imagePath)[screenshotPos], cv2.IMREAD_GRAYSCALE)
	#display('cropTest', image[0:200, 0:100])
	rows,cols = image.shape
	
	bottomHalf = image[int(rows/2):rows,0:cols]
	return formatScreenshot(bottomHalf)

def matchLetters(gameScreenshotPath,screenshotPos, alphabetPath):
	final = {}

	locations = []
	totalRatio=0
	count=0
	letterToScren = 0
	iteration = 0
	screenshot = cv2.imread(gameScreenshotPath + '/' + os.listdir(gameScreenshotPath)[screenshotPos], cv2.IMREAD_GRAYSCALE)
	for scale in np.linspace(0.2,2,100)[::-1]:
		print ('SCALE:',scale)
		resized = imutils.resize(screenshot, width = int(screenshot.shape[1] * scale))
		r = screenshot.shape[1] / float(resized.shape[1]) #ratio of old to new

		for letterName in os.listdir(alphabetPath):

			#print('Looking for', str(letterName)[0:1])

			colorImage = cv2.imread(alphabetPath + '/' + str(letterName))
			letterImage = cv2.imread(alphabetPath + '/' + str(letterName), cv2.IMREAD_GRAYSCALE)
			rows,cols = letterImage.shape
			tempRows,tempCols = resized.shape

			if (tempRows > rows and tempCols > cols):
				res = cv2.matchTemplate(resized, letterImage, cv2.TM_CCOEFF_NORMED)
				(_,maxVal,_,maxLoc) = cv2.minMaxLoc(res)

				xRange = range(maxLoc[0] - 10, maxLoc[1] + 10)
				#print (maxVal)
				threshold = 0.9
				if (maxVal >= threshold): #only if decent match
					letterToScreen = cols/(resized.shape[1])
					totalRatio += letterToScreen
					count += 1
					print (str(letterName[0:1]), maxVal)
					print ('RATIO', letterToScreen)
					print ('MAXLOC', maxLoc)
					if (str(letterName[0:1]) not in final): #add if letter is not already in
						#final.append(str(letterName)[0:1])
						final.setdefault(str(letterName[0:1]),[maxVal,maxLoc])
						#final[str(letterName[0:1])] = maxVal
					elif (distance(final[str(letterName[0:1])][1],maxLoc) > 10):
						print (distance(final[str(letterName[0:1])][1],maxLoc))
						final.setdefault(str(letterName[0:1]),[maxVal,maxLoc])
					elif (final[str(letterName[0:1])][0] < maxVal): #add if current score is better than existing one
						final[str(letterName[0:1])] = [maxVal,maxLoc]
			iteration += 1
	print ('expected', str(os.listdir(gameScreenshotPath)[screenshotPos]))
	#print ('expecting', len(locations), 'letters')
	print ('found', len(final), 'letters')
	print ('Average ratio', (totalRatio / count))
	return final





def newMatchLetters(gameScreenshotPath,screenshotPos, alphabetPath):
	final = []
	locs = []
	temp = []
	temporaryApp = []
	iteration = 0
	screenshot = cv2.imread(gameScreenshotPath + '/' + os.listdir(gameScreenshotPath)[screenshotPos], cv2.IMREAD_GRAYSCALE)
	for scale in np.linspace(0.2,2,100)[::-1]:
		print ('SCALE:',scale)
		resized = imutils.resize(screenshot, width = int(screenshot.shape[1] * scale))
		r = screenshot.shape[1] / float(resized.shape[1]) #ratio of old to new

		for letterName in os.listdir(alphabetPath): #for each letter
			letter = str(letterName[0:1])
			#print('Looking for', str(letterName)[0:1])

			colorImage = cv2.imread(alphabetPath + '/' + str(letterName))
			letterImage = cv2.imread(alphabetPath + '/' + str(letterName), cv2.IMREAD_GRAYSCALE)
			rows,cols = letterImage.shape
			tempRows,tempCols = resized.shape

			if (tempRows > rows and tempCols > cols):
				res = cv2.matchTemplate(resized, letterImage, cv2.TM_CCOEFF_NORMED)
				
				#(_,maxVal,_,maxLoc) = cv2.minMaxLoc(res)
				threshold = 0.9
				locations = np.where(res >= threshold)
				for point in list(zip(*locations[::-1])): #for each matching point of a single letter, can be matches at diff locs
					temp = [letter,point]	#temp holds the letter and the point

					if (letter not in final):	#add letter if it is new 
						final.append(letter)
						locs.append(point)
						print ('adding new letter', letter)
					else:
						print ('looking for old letter', letter)
						letterIndex = findInList(final, letter)
						print (letterIndex)
						for index in letterIndex:
							if (distance(point,locs[index]) > 75):
								print (distance(point,locs[index]))
								final.append(letter)
								locs.append(point)					
				'''
						for letterPoint in final:
							print (letterPoint)
							if (str(letterName[0:1]) not in letterPoint[0]): #add if new letter		
								final.append(temp)
							elif (distance(letterPoint[1],point) > 50):
								#print ('DISTANCE',distance(letterPoint[1],point))

								final.append(temp)
				'''	
					
				'''	
				if (maxVal >= threshold): #only if decent match
					letterToScreen = cols/(resized.shape[1])
					totalRatio += letterToScreen
					count += 1
					print (str(letterName[0:1]), maxVal)
					print ('RATIO', letterToScreen)
					print ('MAXLOC', maxLoc)
					temp = [str(letterName[0:1]), maxVal, maxLoc]
					for letter in final:

						if (str(letterName[0:1]) not in letter[0]): #add if new letter
							
							final.append(temp)
							
						elif (distance(letter[2],maxLoc) > 10):
							print ('DISTANCE',distance(final[str(letterName[0:1])][1],maxLoc))
							final.append(temp)
						#elif (final[str(letterName[0:1])][0] < maxVal): #add if current score is better than existing one
							#final[str(letterName[0:1])] = [maxVal,maxLoc]
				'''
	print ('expected', str(os.listdir(gameScreenshotPath)[screenshotPos]))
	#print ('expecting', len(locations), 'letters')
	print ('found', len(final), 'letters')
	
	return final

def smartMatchLetters(gameScreenshotPath,screenshotPos, alphabetPath):
	final = {}
	locations = []
	screenshot = cv2.imread(gameScreenshotPath + '/' + os.listdir(gameScreenshotPath)[screenshotPos], cv2.IMREAD_GRAYSCALE)
	screenshotWidth = int(screenshot.shape[1]) #width of screenshot
	print('ORIGINAL WIDTH', screenshotWidth)
	'''
	for scale in np.linspace(0.2,2,100)[::-1]:
		print ('SCALE:',scale)
		resized = imutils.resize(screenshot, width = int(screenshot.shape[1] * scale))
		r = screenshot.shape[1] / float(resized.shape[1]) #ratio of old to new
	'''
	for letterName in os.listdir(alphabetPath):

		#print('Looking for', str(letterName)[0:1])

		colorImage = cv2.imread(alphabetPath + '/' + str(letterName))
		letterImage = cv2.imread(alphabetPath + '/' + str(letterName), cv2.IMREAD_GRAYSCALE)
		rows,cols = letterImage.shape
		ratio = (cols/screenshotWidth)
		print ('RATIO of LETTER to SCREENSHOT', ratio)

		resized = imutils.resize(screenshot,width = 10 * cols)
		tempRows,tempCols = resized.shape
		print ('RESIZED WIDTH', tempCols)
		print ('RATIO OF LETTER to RESIZED:', (tempCols/cols))
		if (tempRows > rows and tempCols > cols):
			
			res = cv2.matchTemplate(resized, letterImage, cv2.TM_CCOEFF_NORMED)
			(_,maxVal,_,maxLoc) = cv2.minMaxLoc(res)

			xRange = range(maxLoc[0] - 10, maxLoc[1] + 10)
			#print (maxVal)
			threshold = 0.9
			if (maxVal >= threshold): #only if decent match
				print (str(letterName[0:1]), maxVal)
				if (str(letterName[0:1]) not in final): #add if letter is not already in
					#final.append(str(letterName)[0:1])
					final[str(letterName[0:1])] = maxVal
				elif (final[str(letterName[0:1])] < maxVal): #add if current score is better than existing one
					final[str(letterName[0:1])] = maxVal

	print ('expected', str(os.listdir(gameScreenshotPath)[screenshotPos]))
	#print ('expecting', len(locations), 'letters')
	print ('found', len(final), 'letters')
	return final
def topMatches(scoreList,expectedNum): #list of scores, expected number of letters
	final = [expectedNum]
	for score in scoreList:
		if (len(final) < expectedNum):
			final.append(score)
		else:
			for temp in range(0,len(final)):
				if (score > temp):
					final[temp] = score
	return final

	

def main():
	#display('bottomHalf', 0,formatScreenshot(pathScreenshot))
	#print (matchLetters(pathScreeshot,pathForm))

	formatAll(pathUnForm, pathForm)
	letters = newMatchLetters(pathScreenshot,int(sys.argv[1]),pathForm)
	print (letters)
	print (wordMocha.solve(letters))
	'''
	for screenshot in range(0,len(os.listdir(pathScreenshot))):
   		print (matchLetters(pathScreenshot,screenshot,pathForm))
   	'''
	return 0		


if __name__ == "__main__":

    main()