import re
import shopTypes

class Rossman:
    def __init__(self,txt):
        return self.getDataFromTxt(txt)
    def getDataFromTxt(self,txt):
        pass
shopTypes.ReceiptTypeFactory.registerShop("Rossman",Rossman)

class Biedronka:
    def __init__(self,txt):
        return self.getDataFromTxt(txt)
    def getDataFromTxt(self,txt):
        pass
shopTypes.ReceiptTypeFactory.registerShop("Biedronka",Biedronka)



