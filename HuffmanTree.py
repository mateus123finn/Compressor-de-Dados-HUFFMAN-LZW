from Node import Node

#classe reponsável pela criação da Árvore de HUFFMAN
class HuffmanTree:
    def __init__(self):
        self.raiz = None
        self.table = [ [ 0 for i in range(2) ] for j in range(256) ]

    #função de criação da árvore de acordo com um vetor das ocorrências dos Bytes (PosVet)
    def createTree(self, PosVet):
        auxVet = list()
        for i in range(len(PosVet)):
            if(PosVet[i] > 0):
                nAux = Node()
                nAux.setElemento(i)
                nAux.setPeso(PosVet[i])
                auxVet.append(nAux)

        #print(auxVet)

        self.raiz = self.__createTree(auxVet)
        self.__createTable(0,0,self.raiz)
        
    #função recursiva para a soma das menores ocorrências e crescimento da árvore
    def __createTree(self,vet:list):
        if(len(vet) == 1):
            #print(vet[0])
            return vet[0]

        vet.sort(key=lambda x: (x.peso, x.elemento))
        nAux = Node()        
        nAux.setPeso(vet[0].getPeso() + vet[1].getPeso())
        nAux.setLeft(vet[0])
        nAux.setRight(vet[1])
        vet.pop(0)
        vet.pop(0)
        vet.insert(0,nAux)
        return self.__createTree(vet)

    #função para recuperação de Byte a partir de um vetor de bits(vet)
    #Se for finalizada a busca, o Byte é retornado
    #Se não for finalizada a busca, o ultimo nodo é retornado para uma futura busca começando por ele (node)
    def findElemento(self, node, vet):
        if(len(vet) <= 0):
            return node
        if(node.getLeft() == None and node.getRight() == None):
            #print(node.getElemento())
            return node.getElemento()
        if(vet.pop(0) == 1):
            #print('teste')
            return self.findElemento(node.getRight(), vet)
        else:
            #print('abacate')
            return self.findElemento(node.getLeft(), vet)

    #função para criação da relação entre a representação do Byte e a quantidade de bits necessária para sua representação.
    def __createTable(self, bits, nBits, node):
        if(node.getLeft() == None and node.getRight() == None):
            #print(bin(bits))
            self.table[node.getElemento()][0] = bits
            self.table[node.getElemento()][1] = nBits
            return
        
        self.__createTable(bits << 1, nBits+1, node.getLeft())
        self.__createTable((bits << 1 )+ 1, nBits+1, node.getRight())

    #funções debug :D
    def printT(self, node):
        if(node == None):
            return

        print(node.getElemento())
        self.printT(node.getLeft())
        
        self.printT(node.getRight())
        
    
    def printLA(self):
        for i in range(len(self.table)):
            print(i)
            print(bin(self.table[i][0]) +" - "+str(self.table[i][1]))

    

