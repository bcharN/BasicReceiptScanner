import utils
class ReceiptTypeFactory:
    def __init__(self) -> None:
        self._shops = {}
    def registerShop(self, name, shopParser):
        self._shops[name] = shopParser

    def getReceiptParser(self,txt,shopName = None):
        if shopName == None: self.shopname = utils.getShopName(txt)
        if not shopName: raise ValueError(shopName)
        return self._shops.get(shopName)










