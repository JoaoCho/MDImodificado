class importaPCHexp:
    def __init__(self):
        import sys
        import os

        txtPCH = open(os.path.join(sys.path[0], "Dados\\PCH_exp.csv"), "r", encoding="utf-8",).readlines()
        self.PCH_exp = [[0]*8 for i in range(len(txtPCH) -1)]

        #importa o PCH_exp.csv e cria uma matriz[PCH][caracteristica] onde caracteristica[0] = ID, caracteristica[1] = nome, caracteristica[2] = Número máximo de PCHs para expansão, , caracteristica[3] = Capacidade, caracteristica[4] = Garantia Física, caracteristica[5] = CAPEX e caracteristica[6] = Degrau de CAPEX por nova usina
        for linha in range(1,len(txtPCH)):
            self.PCH_exp[linha-1][0] = int(txtPCH[linha].split(";")[0].replace(",","."))
            self.PCH_exp[linha-1][1] = txtPCH[linha].split(";")[1].replace(",",".")
            self.PCH_exp[linha-1][2] = float(txtPCH[linha].split(";")[2].replace(",","."))
            self.PCH_exp[linha-1][3] = float(txtPCH[linha].split(";")[3].replace(",","."))
            self.PCH_exp[linha-1][4] = float(txtPCH[linha].split(";")[4].replace(",","."))
            self.PCH_exp[linha-1][5] = float(txtPCH[linha].split(";")[5].replace(",","."))
            self.PCH_exp[linha-1][6] = float(txtPCH[linha].split(";")[6].replace(",","."))
            self.PCH_exp[linha-1][7] = float(txtPCH[linha].split(";")[7].replace(",","."))
        
        self.numPCH = len(self.PCH_exp)