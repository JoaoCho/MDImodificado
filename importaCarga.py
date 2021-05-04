class importaCarga:
    def __init__(self):
        import numpy
        import sys
        import os

        txtcarga = open(os.path.join(sys.path[0], "Dados\\carga.csv"), "r", encoding="utf-8",).readlines()
        cenariolinha = [[0] for i in range(len(txtcarga) -1)]
        periodolinha = [[0] for i in range(len(txtcarga) -1)]

        for linha in range(1,len(txtcarga)):
            cenariolinha[linha-1] = txtcarga[linha].split(";")[0]
            periodolinha[linha-1] = txtcarga[linha].split(";")[1]
        
        self.numcenario = int(max(cenariolinha))
        self.numperiodo = int(max(periodolinha))

        self.carga = numpy.zeros((self.numcenario,self.numperiodo,24))
        
        #importa o carga.csv e cria uma matriz[cenario][periodo][carga] onde a carga é discriminada para cada hora do dia
        for linha in range(1,len(txtcarga)):
            for coluna in range(2, 26):
                self.carga[int(txtcarga[linha].split(";")[0])-1][int(txtcarga[linha].split(";")[1])-1][coluna-2] = float(txtcarga[linha].split(";")[coluna].replace(",","."))  

                 