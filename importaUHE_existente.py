class importaUHE_existente:
    def __init__(self):
        import sys
        import os
        
        txtUHE = open(os.path.join(sys.path[0], "Dados\\UHE_existente.csv"), "r", encoding="utf-8",).readlines()
        self.UHE = [[0]*5 for i in range(len(txtUHE) -1)]

        #importa o UHE_existente.csv e cria uma matriz[UHE][caracteristica] onde caracteristica[0] = ID, caracteristica[1] = nome, caracteristica[2] = Capacidade, caracteristica[3] = Garantia Física, e caracteristica[4] = Geração Hidrelétrica Mínima
        for linha in range(1,len(txtUHE)):
            self.UHE[linha-1][0] = int(txtUHE[linha].split(";")[0].replace(",","."))
            self.UHE[linha-1][1] = txtUHE[linha].split(";")[1].replace(",",".")
            self.UHE[linha-1][2] = float(txtUHE[linha].split(";")[2].replace(",","."))
            self.UHE[linha-1][3] = float(txtUHE[linha].split(";")[3].replace(",","."))
            self.UHE[linha-1][4] = float(txtUHE[linha].split(";")[4].replace(",","."))
            
        
        self.numUHE = len(self.UHE)