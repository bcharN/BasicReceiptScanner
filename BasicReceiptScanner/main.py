import ImagePrep
import OCR
import sys
import shopTypes 

def main():
    listOfReceiptData = []
    ocr = OCR()
    imgPrep = ImagePrep()

    for arg in range(1,len(sys.argv)):
        txt = ocr.readTextFromImg(imgPrep(arg))
        parser = shopTypes.ReceiptTypeFactory.getReceiptParser(txt)
        listOfReceiptData.append(parser(txt))
    return listOfReceiptData

    
if __name__ == "__main__":
    main()