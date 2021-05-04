class importaDadosGerais:
    def __init__(self):
        import sys
        import os
       
        txtdados = open(os.path.join(sys.path[0], "Dados\\dados_cenario.csv"), "r", encoding="utf-8",).readlines()
                
        colunastotal = len(txtdados[1].split(";"))

        numcenarios = 0
        #conta o número de cenários considerados (valores não vazios na planilha)
        for coluna in range(1, colunastotal):
            if (txtdados[1].split(";")[coluna].replace("\n", ""). replace(" ", "") != ""):
                numcenarios = numcenarios + 1

        self.GSF = [[0] for i in range(numcenarios)]
        self.CVU = [[0] for i in range(numcenarios)]
        self.ProbCenario = [[0] for i in range(numcenarios)]

        #cria a matriz GSF[cenario] que estabelece cada GSF para cada cenário e matriz CVU[cenario] que estabelece cada multiplicador do CVU para cada cenário
        for cenario in range(numcenarios):
            self.GSF[cenario] = float(txtdados[1].split(";")[cenario+1].replace(",","."))
            self.CVU[cenario] = float(txtdados[2].split(";")[cenario+1].replace(",","."))
            self.ProbCenario[cenario] = float(txtdados[3].split(";")[cenario+1].replace(",","."))


        txtperiodos = open(os.path.join(sys.path[0], "Dados\\dados_periodo.csv"), "r", encoding="utf-8",).readlines()

        colunastotalperiodos = len(txtperiodos[1].split(";"))

        numperiodos = 0

        #conta o número de cenários considerados (valores não vazios na planilha)
        for coluna in range(1, colunastotalperiodos):
            if (txtperiodos[1].split(";")[coluna].replace("\n", ""). replace(" ", "") != ""):
                numperiodos = numperiodos + 1

        self.ProbPeriodo = [[0] for i in range(numperiodos)]

        for periodo in range(numperiodos):
            self.ProbPeriodo[periodo] = float(txtperiodos[1].split(";")[periodo+1].replace(",","."))