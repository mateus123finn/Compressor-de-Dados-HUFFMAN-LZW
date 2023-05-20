import math as m
import os, time
from IOHandler import IOHandler

#Função que a partir do local do arquivo (path), o compacta e envia para a pasta "Compactado"
#O tamanho Máximo do Dicionário (tamDici), pode ser informado
#O dicionário é inicializado com os Bytes de 0x00 até 0xFF
#Os bytes são representados em char ('cp437') e essa representaçao é utilizada para a busca e construção do Dicionário
#O maior tamanho possível para o dicionário é 0xFFFFFFFF
def Compactar(path,tamDici = 0xFFFF):

    tempoCmc = time.time()
    try:
        f = open(path,'rb')
    except:
        return False
    nomeArquivo = os.path.basename(f.name)
    io = IOHandler(open("./Compactado/"+nomeArquivo+"LZW.lzw",'wb'))
    Dicionario = dict()
    standByte = ""
    nBytes = 1
    qntNumeros = 256
    bitsMaximo = m.floor(m.log2(tamDici)) + 1

    if(tamDici < qntNumeros or bitsMaximo > 16):
        tamDici = qntNumeros
        bitsMaximo = m.floor(m.log2(tamDici)) + 1

    for i in range(256):
        Dicionario[i.to_bytes(1,'big').decode('cp437')] = i

    buffer = -1

    io.writeByte(bitsMaximo,8)

    while(True):
        i = 0
        testeAux = ""
        maiorCasamento = ""
        for i in range(0,nBytes):
            buffer = f.read(1)
            if(buffer == b''):
                break
            testeAux += buffer.decode('cp437')

            #print(testeAux +" - "+ str(len(testeAux)))

            if testeAux in Dicionario:
                maiorCasamento = testeAux

        if(i+1 == nBytes):
            f.seek(-(nBytes-len(maiorCasamento)),1)
        else:
            f.seek(-(i-len(maiorCasamento)),1)

        if(maiorCasamento == ""):
            break
            
        io.writeByte(int(Dicionario[maiorCasamento]),bitsMaximo)
        #print(Dicionario[maiorCasamento])

        if standByte == "":
           standByte = maiorCasamento
        elif (qntNumeros < tamDici):
            standByte += maiorCasamento
            Dicionario[standByte] = qntNumeros
            qntNumeros += 1

            if(len(standByte) > nBytes):
                nBytes = len(standByte)
            
            standByte = maiorCasamento

    io.closeHandlerSave()

    print()
    print("Compressão LZW")
    print("Percentual de Redução: "+str(round(100*(1 - (os.stat(path).st_size / os.stat("./Compactado/"+nomeArquivo+"LZW.lzw").st_size))))+" %")
    print("Tempo de Execução: "+ str(round(1000 *(time.time() - tempoCmc)))+" ms")

    return True

#Função que a partir do local do arquivo (path), o descompacta e envia para a pasta "Descompactado"
#É lido os primeiros 16 bits do arquivo para definir o tamanho dos "bytes" a serem lidos
#Os "bytes" são lidos e são utilizados como o indice da lista de simbolos, que é criada de acordo com a execução do código 
def Descompactar(path):
    
    tempoCmc = time.time()
    ListaDescompactar = list()
    nLer = 0
    standByte = ""
    try:
        fileA = open(path,'rb')
    except:
        return False
    io = IOHandler(fileA)
    nomeArquivo = os.path.basename(fileA.name)
    path = nomeArquivo.split("LZW.lzw")[0]
    f = open("./Descompactado/DESC"+path,'wb')

    for i in range(256):
        ListaDescompactar.append(i.to_bytes(1,'big').decode('cp437'))

    for i in io.readBits():
        nLer <<= 1
        nLer |= i

    vetBits = io.readBits()
    bitsLidos = 0
    nLido = 0
    while(vetBits != None):

        nLido <<= 1
        nLido |= vetBits.pop(0)
        bitsLidos += 1
        
        if(bitsLidos == nLer):

            f.write(ListaDescompactar[nLido].encode('cp437'))

            if(standByte == ""):
                standByte = ListaDescompactar[nLido]
            else:
                standByte += ListaDescompactar[nLido]
                ListaDescompactar.append(standByte)
                standByte = ListaDescompactar[nLido]

            bitsLidos = 0
            nLido = 0

        if(len(vetBits) <= 0):
            vetBits = io.readBits()
    f.close()

    print()
    print("Descompressão LZW")
    print("Tempo de Execução: "+ str(round(1000 *(time.time() - tempoCmc)))+" ms")

    return True



    


        

