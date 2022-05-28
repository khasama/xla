# import pytesseract as tess
# tess.pytesseract.tesseract_cmd = r'E:\python\tess\tesseract.exe'

import cv2
from utlis import *
import os
import calendar
import time



def getListImg(imgPath):
    
    current_GMT = time.gmtime()
    ts = calendar.timegm(current_GMT)
    uploadPath = "static/img/"+str(ts)
    os.mkdir(uploadPath)
    path = imgPath
    hsv = [0, 65, 59, 255, 0, 255]
    hsv_green = [55, 65, 100, 255, 0, 255]

    img = cv2.imread(path)

    imgRs = detectColor(img, hsv_green)

    imgContour, contours = getContours(imgRs, img, showCanny=False, 
                                    minArea=500, filter=0,
                                    cThr=[100, 150], draw=True)
    
    roiList = getRoi(img, contours)
    for x, roi in enumerate(roiList):
        roi = cv2.resize(roi, (0, 0), None, 2, 2)
        #cv2.imshow(str(x), roi)
        cv2.imwrite(uploadPath+"/"+str(x)+'.jpg', roi)

    
    return uploadPath

# hlText = []
# for x, roi in enumerate(roiList):
    # print(tess.image_to_string(roi))
    # hlText.append(tess.image_to_string(roi))
#getListImg('d.jpg')
