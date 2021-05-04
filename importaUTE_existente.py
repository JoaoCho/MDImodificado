class importaUTE_existente:
    def __init__(self):
        import sys
        import os
        
        txtUTE = open(os.path.join(sys.path[0], "Dados\\UTE_existente.csv"), "r", encoding="utf-8",).readlines()
        self.UTE = [[0]*5 for i in range(len(txtUTE) -1)]
        
        #importa o UTE_existente.csv e cria uma matriz[UTE][caracteristica] onde caracteristica[0] = ID, caracteristica[1] = nome, caracteristica[2] = Capacidade, caracteristica[3] = GTMin, e   caracteristica[4] = CVU
        for linha in range(1,len(txtUTE)):
            self.UTE[linha-1][0] = int(txtUTE[linha].split(";")[0].replace(",","."))
            self.UTE[linha-1][1] = txtUTE[linha].split(";")[1].replace(",",".")
            self.UTE[linha-1][2] = float(txtUTE[linha].split(";")[2].replace(",","."))
            self.UTE[linha-1][3] = float(txtUTE[linha].split(";")[3].replace(",","."))
            self.UTE[linha-1][4] = float(txtUTE[linha].split(";")[4].replace(",","."))

        self.numUTE = len(self.UTE)