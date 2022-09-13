import pytesseract


class OCR:
    def __init__(self):
        pass

    def readTextFromImg(self, img):
        return pytesseract.image_to_string(img)






