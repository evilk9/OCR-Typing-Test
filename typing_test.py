#Automatic OCR typing built to be used at http://typing-speed-test.aoeu.eu/?lang=en
#Average 200WPM
#Created by Lachlan Page 
from PIL import ImageGrab
from PIL import Image
import numpy as np
import cv2
import time 
import pytesseract
import os
import SendKeys

#Path to Pytesseract executable {if added to PATH then not needed}
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

#Colour Range for masking ([R, G, B])
upper = np.array([184,227,105])
lower = np.array([0,0,0])

#Initial Setup Timer {Countdown from 4}
for i in xrange(0,5):
	time.sleep(1)
	print i

isRunning = True
start_time = time.time()
while (isRunning):
	#BBOX { TOPLEFT X, TOPLEFT Y, BOTTOMRIGHT X , BOTTOMRIGHT Y}
	#Coordinates are correct for full screen 1080p monitor firefox
	img = ImageGrab.grab(bbox=(660,350, 1250,500))

	#Masking {black untyped text becomes white}
	img = np.array(img)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
	mask = cv2.inRange(img, lower, upper)

	#temp file storage
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, mask)

	text_on_screen = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)

	#OCR joins two words with "\n" when near end of screen - fix to seperate 
	text_on_screen = text_on_screen.replace('\n', ' ')
	text_on_screen = text_on_screen.split(" ")

	for word in text_on_screen:
		SendKeys.SendKeys(str(word))
		SendKeys.SendKeys("{SPACE}")

	#Constrain running time to 60 seconds
   	if(time.time() - start_time >= 60):
   		isRunning = False