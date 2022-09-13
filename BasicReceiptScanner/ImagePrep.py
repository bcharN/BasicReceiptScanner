import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.filters import threshold_local 
from PIL import Image
import os.path

class ImagePrep:

    def __init__(self):
        pass

    def openCvResize(self, image, scale):
        width = int(image.shape[1] * scale)
        height = int(image.shape[0] * scale)
        return cv2.resize(image,(width,height),interpolation = cv2.INTER_AREA)

    def approximateContour(self, contour):
        peri = cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, 0.032 * peri, True)

    def getReceiptContour(self, contours):    
        for c in contours:
            approx = self.approximateContour(c)
            if len(approx) == 4:
                return approx
    
    def contourToRec(self, contour, scale):
        pts = contour.reshape(4, 2)
        rect = np.zeros((4, 2), dtype = "float32")

        s = pts.sum(axis = 1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect / scale

    def wrapPerspective(img, rect):
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        return cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    
    def bwScanner(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        T = threshold_local(gray, 21, offset = 5, method = "gaussian")
        return (gray > T).astype("uint8") * 255

    def prepImage(self, pathToImage):
        if not os.path.isfile(pathToImage) : raise ValueError("pathToImage must be a string representing a valid path to an image file ")
        with cv2.imread(pathToImage) as img:
            scale = 500 / img.shape[0]
            originalImage = img.copy()
            image = self.openCvResize(image, scale)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
            dilated = cv2.dilate(blurred, rectKernel)
            edged = cv2.Canny(dilated, 100, 200, apertureSize=3)
            contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            largest_contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
            receipt_contour = self.getReceiptContour(largest_contours)
            scanned = self.wrapPerspective(originalImage.copy(), self.contourToRec(receipt_contour))
            result = self.bwScanner(scanned)
        return Image.fromarray(result)
            
    def prepImages(self, pathsToImages):
        for path in pathsToImages:
            yield self.prepImage(path)
    


