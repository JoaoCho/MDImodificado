class importaEXP:
    def __init__(self):
        import numpy 
        import collections
        import sys
        import os

        txtOUTRASexp = open(os.path.join(sys.path[0], "Dados\\OUTRAS_exp.csv"), "r", encoding="utf-8",).readlines()
        TecnologiaOutraslinha = [[0] for i in range(len(txtOUTRASexp) -1)]
        periodolinha = [[0] for i in range(len(txtOUTRASexp) -1)]

        for linha in range(1,len(txtOUTRASexp)):
            TecnologiaOutraslinha[linha-1] = int(txtOUTRASexp[linha].split(";")[0])
            periodolinha[linha-1] = int(txtOUTRASexp[linha].split(";")[2])

        numtecnologiaoutras = int(max(TecnologiaOutraslinha))
        numperiodo = int(max(periodolinha))
        self.numOUTRAS = numtecnologiaoutras

        #importa o OUTRAS_exp.csv e cria uma matriz[tecnologia][periodo][fator capacidade] onde o fator capacidade é discriminado para cada hora do dia
        self.OUTRAS_exp = numpy.zeros((numtecnologiaoutras,numperiodo,27))
        self.nomeOUTRAS_exp = [[""] for i in range (numtecnologiaoutras)]
        
        for linha in range(1,len(txtOUTRASexp)):
            for coluna in range(3, 30):
                self.OUTRAS_exp[int(txtOUTRASexp[linha].split(";")[0])-1][int(txtOUTRASexp[linha].split(";")[2])-1][coluna-3] = float(txtOUTRASexp[linha].split(";")[coluna].replace(",","."))

            for notec in range (0, numtecnologiaoutras):
                if int(txtOUTRASexp[linha].split(";")[0].replace(",",".")) == notec+1:
                    self.nomeOUTRAS_exp[notec] = txtOUTRASexp[linha].split(";")[1].replace(",",".")

        txtUTEexp = open(os.path.join(sys.path[0], "Dados\\UTE_exp.csv"), "r", encoding="utf-8",).readlines()

        TecnologiaUTElinha = [[0] for i in range(len(txtUTEexp) -1)]
        cenariolinha = [[0] for i in range(len(txtUTEexp) -1)]

        for linha in range(1,len(txtUTEexp)):
            TecnologiaUTElinha[linha-1] = int(txtUTEexp[linha].split(";")[0])
            cenariolinha[linha-1] = int(txtUTEexp[linha].split(";")[2])
        
        numUTEexp = int(max(TecnologiaUTElinha))
        numcenario = int(max(cenariolinha))

        self.numUTE = numUTEexp        
        self.UTE_exp = numpy.zeros((numUTEexp, numcenario, 5))
        self.nomeUTE_exp = [[""] for i in range (numUTEexp)]

        #importa o UTE_exp.csv e cria uma matriz[IDUTE][cenario][propriedade] onde o propriedade[0] é GTMin (em %), propriedade[1] é o CVU e propriedade[2] é o CAPEX
        for linha in range(1,len(txtUTEexp)):
            IDUTE = int(txtUTEexp[linha].split(";")[0].replace(",","."))
            cenario = int(txtUTEexp[linha].split(";")[2].replace(",","."))

            self.UTE_exp[IDUTE-1][cenario-1][0] = float(txtUTEexp[linha].split(";")[3].replace(",","."))  
            self.UTE_exp[IDUTE-1][cenario-1][1] = float(txtUTEexp[linha].split(";")[4].replace(",","."))
            self.UTE_exp[IDUTE-1][cenario-1][2] = float(txtUTEexp[linha].split(";")[5].replace(",","."))
            self.UTE_exp[IDUTE-1][cenario-1][3] = float(txtUTEexp[linha].split(";")[6].replace(",",".")) 
            self.UTE_exp[IDUTE-1][cenario-1][4] = float(txtUTEexp[linha].split(";")[7].replace(",","."))   

            for notec in range (0, numUTEexp):
                if int(txtUTEexp[linha].split(";")[0].replace(",",".")) == notec+1:
                    self.nomeUTE_exp[notec] = txtUTEexp[linha].split(";")[1].replace(",",".")


        txtUHE = open(os.path.join(sys.path[0], "Dados\\UHE_exp.csv"), "r", encoding="utf-8",).readlines()

        TecnologiaUHElinha = [[0] for i in range(len(txtUHE) -1)]

        for linha in range(1,len(txtUHE)):
            if txtUHE[linha].split(";")[0] != None:
                TecnologiaUHElinha[linha-1] = int(txtUHE[linha].split(";")[0])

        numUHEexp = int(len(TecnologiaUHElinha)) 

        self.UHE_exp = [[0]*6 for i in range(len(txtUHE) -1)]
        self.nomeUHE_exp = [[""] for i in range (numUHEexp)]

        self.numUHE = numUHEexp

        #importa o UHE_exp.csv e cria uma matriz[UHE][caracteristica] onde caracteristica[0] = ID, caracteristica[1] = nome, caracteristica[2] = Capacidade, caracteristica[3] = Garantia Física, caracteristica[4] = CAPEX e caracteristica[5] = GHMin
        for linha in range(1,len(txtUHE)):
            self.UHE_exp[linha-1][0] = int(txtUHE[linha].split(";")[0].replace(",","."))
            self.UHE_exp[linha-1][1] = txtUHE[linha].split(";")[1].replace(",",".")
            self.UHE_exp[linha-1][2] = float(txtUHE[linha].split(";")[2].replace(",","."))
            self.UHE_exp[linha-1][3] = float(txtUHE[linha].split(";")[3].replace(",","."))
            self.UHE_exp[linha-1][4] = float(txtUHE[linha].split(";")[4].replace(",","."))
            self.UHE_exp[linha-1][5] = float(txtUHE[linha].split(";")[5].replace(",","."))

            self.nomeUHE_exp[notec] = txtUHE[linha].split(";")[1].replace(",",".")
        
        Repetidas = [item for item, count in collections.Counter(TecnologiaUHElinha).items() if count > 1]

        self.numConfsUHEexp = len(Repetidas)
        self.MatrizConfUHE = numpy.zeros((len(Repetidas), self.numUHE,))

        for uhe in range(self.numUHE):
            for repetida in range(len(Repetidas)):
                if self.UHE_exp[uhe][0] == Repetidas[repetida]:
                    self.MatrizConfUHE[repetida][uhe] = 1

        txtUTEexpRet = open(os.path.join(sys.path[0], "Dados\\UTE_Retrofit.csv"), "r", encoding="utf-8",).readlines()

        TecnologiaUTElinhaRet = [[0] for i in range(len(txtUTEexpRet) -1)]

        for linha in range(1,len(txtUTEexpRet)):
            TecnologiaUTElinhaRet[linha-1] = int(txtUTEexpRet[linha].split(";")[0])
        
        numUTERet = int(max(TecnologiaUTElinhaRet))

        self.numUTERet = numUTERet        
        self.UTE_Ret = numpy.zeros((numUTERet, numcenario, 4))
        self.nomeUTERet = [[""] for i in range (numUTERet)]

        #importa o UTE_Retrofit.csv e cria uma matriz[IDUTE][cenario][propriedade] onde o propriedade[0] é GTMin (em %), propriedade[1] é o CVU e propriedade[2] é o CAPEX
        for linha in range(1,len(txtUTEexpRet)):
            IDUTERet = int(txtUTEexpRet[linha].split(";")[0].replace(",","."))
            cenario = int(txtUTEexpRet[linha].split(";")[2].replace(",","."))

            self.UTE_Ret[IDUTERet-1][cenario-1][0] = float(txtUTEexpRet[linha].split(";")[3].replace(",","."))  
            self.UTE_Ret[IDUTERet-1][cenario-1][1] = float(txtUTEexpRet[linha].split(";")[4].replace(",","."))
            self.UTE_Ret[IDUTERet-1][cenario-1][2] = float(txtUTEexpRet[linha].split(";")[5].replace(",","."))
            self.UTE_Ret[IDUTERet-1][cenario-1][3] = float(txtUTEexpRet[linha].split(";")[6].replace(",","."))  

            for notec in range (0, numUTERet):
                if int(txtUTEexpRet[linha].split(";")[0].replace(",",".")) == notec+1:
                    self.nomeUTERet[notec] = txtUTEexpRet[linha].split(";")[1].replace(",",".")                    