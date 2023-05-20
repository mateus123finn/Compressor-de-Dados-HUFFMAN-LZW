#Classe de nodos para a criação da árvore de HUFFMAN
class Node:
    def __init__(self):
        self.elemento = 256
        self.peso = 0
        self.left = None
        self.right = None

    def setElemento(self, elemento):
        self.elemento = elemento
    def setPeso(self, peso):
        self.peso = peso
    def setLeft(self, left):
        self.left = left
    def setRight(self, right):
        self.right = right

    def getElemento(self):
        return self.elemento
    def getPeso(self):
        return self.peso
    def getLeft(self):
        return self.left
    def getRight(self):
        return self.right