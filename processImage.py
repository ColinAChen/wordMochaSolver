import os
import cv2

'''
Colin Chen October 2018

Take a screenshot from wordMocha (eventually run in app?)

Template match each letter
Find all possible words with those letters

'''
#display an image
'''
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
def getLettersFromGame(imagePath,alphabetPath):
	#image[startRow:endRow, startCol:endCol]
	image = cv2.imread(imagePath + '/' + os.listdir(imagePath)[0], cv2.IMREAD_GRAYSCALE)
	#display('cropTest', image[0:200, 0:100])
	rows,cols = image.shape
	
	bottomHalf = image[int(rows/2):rows,0:cols]
	return formatLetter(bottomHalf)



def main():
    #formatAll('alphabet', pathForm)
    display('bottomHalf', getLettersFromGame(pathScreenshot,pathForm))


if __name__ == "__main__":

    main()