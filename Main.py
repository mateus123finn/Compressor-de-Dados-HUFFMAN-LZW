#Autor: Mateus Leal Sobreira

import os
import Huffman as hf
import LZW as l

if(not os.path.exists("./Compactado")):
    os.mkdir("./Compactado")
if(not os.path.exists("./Descompactado")):
    os.mkdir("./Descompactado")

opc = ""

print("Compactador/Descompactador de HUFFMAN e LZW ver 1.0 @Mateus Leal")

while(opc != "0"):
    print()
    print("1- Compactar um Arquivo")
    print("2- Descompactar um Arquivo")
    print("0- Sair")
    opc = input("Escolha uma opção: ")
    print()

    if(opc == "1"):
        print("1- Compactar com Huffman")
        print("2- Compactar com LZW")
        print("3- Compactar com os Dois")
        opc = input("Escolha uma opção: ")
        path = input("Digite o nome do arquivo a ser Comprimido: ")

        if(opc == "1"):
            if (not hf.Compactar(path)):
                print("Arquivo não encontrado !!!!!!")
        elif(opc == "2"):
            if (not l.Compactar(path)):
                print("Arquivo não encontrado !!!!!!")
        else:
            if (not hf.Compactar(path) or not l.Compactar(path)):
                print("Arquivo não encontrado !!!!!!")

    elif(opc == "2"):
        print("1- Descompactar com Huffman")
        print("2- Descompactar com LZW")
        opc = input("Escolha uma opção: ")
        path = input("Digite o nome do arquivo a ser Descomprimido: ")

        if(opc == "1"):
            if (not hf.Descompactar(path)):
                print("Arquivo não encontrado !!!!!!")
        elif(opc == "2"):
            if (not l.Descompactar(path)):
                print("Arquivo não encontrado !!!!!!")
