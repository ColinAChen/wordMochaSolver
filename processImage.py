import os
import numpy as np
import imutils
import cv2
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
	screenshot = cv2.imread(gameScreenshotPath + '/' + os.listdir(gameScreenshotPath)[screenshotPos], cv2.IMREAD_GRAYSCALE)
	for scale in np.linspace(0.2,1.8,40)[::-1]:
		resized = imutils.resize(screenshot, width = int(screenshot.shape[1] * scale))
		r = screenshot.shape[1] / float(resized.shape[1]) #ratio of old to new
		for letterName in os.listdir(alphabetPath):

			print('Looking for', str(letterName)[0:1])

			colorImage = cv2.imread(alphabetPath + '/' + str(letterName))
			letterImage = cv2.imread(alphabetPath + '/' + str(letterName), cv2.IMREAD_GRAYSCALE)
			rows,cols = letterImage.shape
			tempRows,tempCols = resized.shape
			if (tempRows > rows and tempCols > cols):
				res = cv2.matchTemplate(resized, letterImage, cv2.TM_CCOEFF_NORMED)
				(_,maxVal,_,maxLoc) = cv2.minMaxLoc(res)

				xRange = range(maxLoc[0] - 10, maxLoc[1] + 10)
				print (maxVal)
				threshold = 0.8
				if (maxVal >= threshold):
					if (str(letterName[0:1]) not in final):
						#final.append(str(letterName)[0:1])
						final[str(letterName[0:1])] = maxVal
					elif (final[str(letterName[0:1])] < maxVal):
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
	print (matchLetters(pathScreenshot,0,pathForm))
	'''
	for screenshot in range(0,len(os.listdir(pathScreenshot))):
   		print (matchLetters(pathScreenshot,screenshot,pathForm))
   	'''
	return 0		


if __name__ == "__main__":

    main()