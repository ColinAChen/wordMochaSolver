import os
import cv2
import numpy as np
'''
Colin Chen October 2018

Take a screenshot from wordMocha (eventually run in app?)

Template match each letter
Find all possible words with those letters

'''
#display an image

pathUnForm = 'C:/Users/colin/wordMochaRepo/wordMochaSolver/alphabet/'
pathForm = 'C:/Users/colin/wordMochaRepo/wordMochaSolver/alphabetFormat/'
pathScreeshot = 'C:/Users/colin/wordMochaRepo/wordMochaSolver/screenshots/'

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
	ret, letter = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
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
def formatScreenshot(imagePath):
	#image[startRow:endRow, startCol:endCol]
	image = cv2.imread(imagePath + '/' + os.listdir(imagePath)[0], cv2.IMREAD_GRAYSCALE)
	#display('cropTest', image[0:200, 0:100])
	rows,cols = image.shape
	
	bottomHalf = image[int(rows/2):rows,0:cols]
	return formatLetter(bottomHalf)

def matchLetters(gameScreenshotPath, alphabetPath):
	final = []
	screenshot = cv2.imread(gameScreenshotPath + '/' + os.listdir(gameScreenshotPath)[2], cv2.IMREAD_GRAYSCALE)
	for letterName in os.listdir(alphabetPath):

		print('Looking for', str(letterName)[0:1])

		colorImage = cv2.imread(alphabetPath + '/' + str(letterName))
		letterImage = cv2.imread(alphabetPath + '/' + str(letterName), cv2.IMREAD_GRAYSCALE)
		rows,cols = letterImage.shape

		res = cv2.matchTemplate(screenshot, letterImage, cv2.TM_CCOEFF_NORMED)
		(_,maxVal,_,_) = cv2.minMaxLoc(res)
		print (maxVal)
		threshold = 0.65
		if (maxVal >= threshold):
			final.append(str(letterName)[0:1])
	print ('expected', str(os.listdir(gameScreenshotPath)[2]))
	print ('found', len(final), 'letters')
	return final

		




def main():
    #formatAll('alphabet', pathForm)
    #display('bottomHalf', formatScreenshot(pathScreeshot))
    print (matchLetters(pathScreeshot,pathForm))


if __name__ == "__main__":

    main()