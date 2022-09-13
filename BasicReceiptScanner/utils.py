import os
import re
import ast
def getKnownShops():
    with open("shopTypes.py","tr") as file:
        p = ast.parse(file)
    return [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]

def getShopName(txt):
    knownShops = getKnownShops()
    for shop in knownShops:
        if not re.search(shop,txt) == None: return shop





