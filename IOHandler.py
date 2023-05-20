import math
class IOHandler:

    #Inicialização do buffer e a quantidade de bits guardados
    def __init__(self, fileO):
        self.nBits = 0
        self.buffer = 0x0000
        self.file = fileO

    #função que recebe os bits a serem guardados e a quantidade de bits para sua representação e trata os dados para mandar para a função __writeBits
    def writeByte(self, bits, tbits):
        aBytes = 0x0000
        if(tbits > 8):
            aux = 8 - (tbits - 8)
            aBytes = bits & 0xFFFF
            aBytes <<= aux
            n1 = aBytes & 0xFF00
            n1 >>= 8
            n2 = aBytes & 0x00FF
            n2 >>= aux
            self.__writeBits(n1,8)
            self.__writeBits(n2,tbits-8)
        else:
            self.__writeBits(bits,tbits)

    #função que salva a lista no arquivo de acordo com a quantidade de bits do maior valor da lista
    def salvarlista(self, vet):
        maiorVal = max(vet)
        Nbits = math.floor(math.log2(maiorVal)) + 1
        self.file.write(Nbits.to_bytes(4,'big'))
        for i in vet:
            self.writeByte(i,Nbits)

    #função que le do arquivo uma lista de acordo com a quantidade de bits presentes no começo do arquivo e retorna esta lista
    def readlista(self):
        vet = list()
        Nbits = int.from_bytes(self.file.read(4),'big')
        stream = self.readBits()
        for i in range(256):
            aux = 0
            numberRead = 0
            while(aux < Nbits):
                if(len(stream) <= 0):
                    stream = self.readBits()
                else:
                    numberRead <<= 1
                    numberRead |= stream.pop(0)
                    aux+=1
            vet.append(numberRead)
        return vet

    #função que transforma um byte do arquivo em um vetor com os 8 bits
    def readBits(self):
        bitList = list()
        rawbytes = self.file.read(1)
        buffer = int.from_bytes(rawbytes,'big')

        if(rawbytes == b''):
            return None
        for i in range(8):
            n = buffer & 0x80
            n >>= 7
            buffer <<= 1
            bitList.append(n)
        
        #print(bitList)
        return bitList
        
    #função que adciona os bits passados (bits) no buffer de acordo com a quantidade de bits para a representação (tbits)
    #Se o buffer ficar cheio (16 bits), os primieros 8 bits são escritos no arquivo e limpos do buffer
    def __writeBits(self, bits, tBits):
        if(self.nBits + tBits >= 16):
            #print(str(tBits)+" - "+str(self.nBits))
            aux = 16 - self.nBits
            self.buffer <<= aux
            aux = tBits - aux
            rBits = self.buffer & 0xFF00
            rBits >>= 8
            self.buffer &= 0x00FF
            self.buffer <<= aux
            self.buffer |= bits
            self.nBits = (self.nBits + tBits) - 8
            self.file.write(rBits.to_bytes(1,'big'))

        else:
            self.buffer <<= tBits
            self.buffer |= bits
            self.nBits += tBits

    #função que escreve no arquivo os bits que sobraram no buffer, depois o fecha
    def closeHandlerSave(self):
        #print(self.nBits)
        if(self.nBits > 0):
            aux = 16 - self.nBits
            self.buffer <<= aux
            rBits = self.buffer & 0xFF00
            rBits >>= 8
            self.file.write(rBits.to_bytes(1,'big'))
            if(aux < 8):
                self.buffer &= 0x00FF
                self.file.write(self.buffer.to_bytes(1,'big'))

        self.file.close()
