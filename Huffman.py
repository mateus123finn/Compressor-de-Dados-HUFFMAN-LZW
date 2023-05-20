from HuffmanTree import HuffmanTree
from IOHandler import IOHandler
import os, time

#Função que a partir do local do arquivo (path), o compacta e envia para a pasta "Compactado"
#O arquivo é lido por byte, e esses são contados e armazenados em "qnt_ocasioes"
#Com esta lista de ocasiões a arvore de HUFFMAN é criada e suas representações são colocadas em uma matriz ([Representação, Quantidade de Bits])
#Essa matriz é utilizada para compactar o arquivo
#A lista de ocasiões é salva no arquivo compactado para a futura criação da árvore de HUFFMAN para sua descompactação.
def Compactar(path):

    tempoCmc = time.time()
    try:
        fopen = open(path,'rb')
    except:
        return False
    nomeArquivo = os.path.basename(fopen.name)
    qnt_ocasioes = [0]*256
    i = IOHandler(open("./Compactado/"+nomeArquivo+"HUFFMAN.hf",'wb'))
    ht = HuffmanTree()
    with fopen as f:
        stream = f.read(1)
        while stream:
            for b in stream:
                qnt_ocasioes[b] += 1
            stream = f.read(1)
    ht.createTree(qnt_ocasioes)
        #ht.printLA()
    i.salvarlista(qnt_ocasioes)
    with open(path,'rb') as f:
        stream = f.read(1)
        while stream:
            for b in stream:
                i.writeByte(ht.table[b][0],ht.table[b][1])
            stream = f.read(1)
        
    i.closeHandlerSave()
    print()
    print("Compressão HUFFMAN")
    print("Percentual de Redução: "+str(round(100*(1 - (os.stat(path).st_size / os.stat("./Compactado/"+nomeArquivo+"HUFFMAN.hf").st_size))))+" %")
    print("Tempo de Execução: "+ str(round(1000 *(time.time() - tempoCmc)))+" ms")
    #print()
    return True

#Função que a partir do local do arquivo (path), o descompacta e envia para a pasta "Descompactado"
#A lista de ocasiões é recuperada do arquivo e utilizada para a construção da árvore de HUFFMAN
#O vetor de Bits de um byte é passado para a função de encontrar um elemento (Ver explicação em HuffmanTree)
#Os Bytes recuperados são escritos em um arquivo
def Descompactar(path):

    tempoCmc = time.time()
    try:
        fopen = open(path,'rb')
    except:
        return False
    i = IOHandler(fopen)
    nomeArquivo = os.path.basename(fopen.name)
    path = nomeArquivo.split("HUFFMAN.hf")[0]
    f = open("./Descompactado/DESC"+path,'wb')
    qnt_ocasioes = list()
    ht = HuffmanTree()

    qnt_ocasioes = i.readlista()
    ht.createTree(qnt_ocasioes)
        #ht.printLA()

    vet = i.readBits()
    nodeParado = ht.raiz
    while(vet != None):
        item = ht.findElemento(nodeParado,vet)
            #print(item)
        if(isinstance(item,int)):
            f.write(item.to_bytes(1,'big'))
            nodeParado = ht.raiz

        else:
            vet = i.readBits()
            nodeParado = item
    f.close()

    print()
    print("Descompressão HUFFMAN")
    print("Tempo de Execução: "+ str(round(1000 *(time.time() - tempoCmc)))+" ms")

    return True

        

    
