import cv2
import numpy as np

def detectColor(img, hsv):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgRs = cv2.bitwise_and(img, img, mask=mask)
    return imgRs

def getContours(img, imgDraw, showCanny=False, minArea=1000, filter=0, cThr=[100, 100], draw=False):
    imgDraw = imgDraw.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) #làm mịn
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1]) # Tô Viền
    kernel = np.array((10, 10))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=1)
    imgClose = cv2.morphologyEx(imgDial, cv2.MORPH_CLOSE, kernel)

    if showCanny: cv2.imshow('Canny', imgClose)
    contours, hiearchy = cv2.findContours(imgClose, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    finalContours = []
    for i in contours:
        area = cv2.contourArea(i)
        #print(area)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])
    #finalContours = sorted(finalContours, key=lambda x:x[1], reverse=True)
    if draw:
        for con in finalContours:
            x, y, w, h = con[3]
            cv2.rectangle(imgDraw, (x, y), (x + w, y + h), (255, 0, 255), 3)
            #cv2.drawContours(imgDraw, con[4], -1, (0, 0, 255), 2)
    
    return imgDraw, finalContours

def getRoi(img, contours):
    roiList = []
    for con in contours:
        x, y, w, h = con[3]
        roiList.append(img[y:y+h, x:x+w])
    return roiList

def roiDisplay(roiList):
    for x, roi in enumerate(roiList):
        roi = cv2.resize(roi, (0, 0), None, 2, 2)
        cv2.imshow(str(x), roi)

