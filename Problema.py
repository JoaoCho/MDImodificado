from pyomo.opt import SolverFactory
import pyomo.environ as pyo
import math 
import numpy
import sys
import os
       
class Problema():
    def __init__(self, carga, UHE_existente, UTE_existente, G_exp, PCH_exp, dados):
        numcenario = carga.numcenario
        numperiodo = carga.numperiodo
        
        #cria concrete model no pyomo
        self.model = pyo.ConcreteModel()

        #cria variáveis de decisão para geração[usina][cenario][periodo]

        self.model.GHExist = pyo.Var(range(UHE_existente.numUHE), range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.GTExist = pyo.Var(range(UTE_existente.numUTE), range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)

        self.model.CustoGTExist = pyo.Var(initialize = 0, domain = pyo.NonNegativeReals)
        self.model.CustoexpOutras = pyo.Var(initialize = 0, domain = pyo.NonNegativeReals)
        self.model.CustoexpUTEs = pyo.Var(initialize = 0, domain = pyo.NonNegativeReals)
        self.model.CustoexpUTERet = pyo.Var(initialize = 0, domain = pyo.NonNegativeReals)
        self.model.CustoexpUHEs = pyo.Var(initialize = 0, domain = pyo.NonNegativeReals)
        self.model.CustoexpPCHs = pyo.Var(initialize = 0, domain = pyo.NonNegativeReals)

        self.model.CustoTotal = pyo.Var(initialize = 0, domain = pyo.NonNegativeReals)

        self.model.CapacidadeOUTRAS_exp = pyo.Var(range(G_exp.numOUTRAS), domain = pyo.NonNegativeReals)

        self.model.CapacidadeUTE_exp = pyo.Var(range(G_exp.numUTE), domain = pyo.NonNegativeReals)


        self.model.GOUTRAS_exp = pyo.Var(range(G_exp.numOUTRAS), range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.GUTE_exp = pyo.Var(range(G_exp.numUTE), range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.GUHE_exp = pyo.Var(range(G_exp.numUHE), range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.binaryUHE_exp = pyo.Var(range(G_exp.numUHE), domain=pyo.Binary)

        self.model.GPCH_exp = pyo.Var(range(PCH_exp.numPCH), range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.IntegerPCH_exp = pyo.Var(range(PCH_exp.numPCH), domain=pyo.Integers)

        self.model.GUTE_Ret = pyo.Var(range(G_exp.numUTERet), range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.IntegerUTE_Ret = pyo.Var(range(G_exp.numUTERet), domain=pyo.Integers)

        self.model.Total_GHExist = pyo.Var(range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.Total_GTExist = pyo.Var(range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.Total_GOUTRAS_exp = pyo.Var(range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.Total_GUTE_exp = pyo.Var(range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.Total_GUTE_Ret = pyo.Var(range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.Total_GUHE_exp = pyo.Var(range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)
        self.model.Total_GPCH_exp = pyo.Var(range(numcenario), range(24*numperiodo), domain = pyo.NonNegativeReals)

        self.model.restricoes = pyo.ConstraintList()

        #!restrição de atendimento de carga
        for periodo in range(24*numperiodo):
            for cenario in range(numcenario):
                periodocarga = math.trunc(periodo/24)
                horacarga = periodo - periodocarga*24
                self.model.restricoes.add(sum(self.model.GHExist[UHEexist,cenario,periodo] for UHEexist in range(UHE_existente.numUHE))
                 + sum(self.model.GTExist[UTEexist,cenario,periodo] for UTEexist in range(UTE_existente.numUTE))
                 + sum(self.model.GOUTRAS_exp[OUTRAS_exp,cenario,periodo] for OUTRAS_exp in range(G_exp.numOUTRAS))
                 + sum(self.model.GUTE_exp[UTE_exp,cenario,periodo] for UTE_exp in range(G_exp.numUTE))
                 + sum(self.model.GUTE_Ret[uteret,cenario,periodo] for uteret in range(G_exp.numUTERet))
                 + sum(self.model.GUHE_exp[UHE_exp,cenario,periodo] for UHE_exp in range(G_exp.numUHE))
                 + sum(self.model.GPCH_exp[pchexp,cenario,periodo] for pchexp in range(PCH_exp.numPCH))
                 >= carga.carga[cenario][periodocarga][horacarga])

        #restrição de geração limitada pela capacidade instalada e garantia física para hidrelétricas existentes
        for cenario in range(numcenario):
            for UHE_exist in range (UHE_existente.numUHE):
                #Garantia Física
                self.model.restricoes.add(sum(self.model.GHExist[UHE_exist,cenario,periodo] for periodo in range(24*numperiodo)) <= dados.GSF[cenario]*UHE_existente.UHE[UHE_exist][3]*24*float(numperiodo))        
                for periodo in range(24*numperiodo):
                    #Potencia
                    self.model.restricoes.add(self.model.GHExist[UHE_exist,cenario,periodo] <= UHE_existente.UHE[UHE_exist][2])
                    #Geração Hidrelétrica Mínima
                    if (UHE_existente.UHE[UHE_exist][4] > dados.GSF[cenario]*UHE_existente.UHE[UHE_exist][3]):
                        self.model.restricoes.add(self.model.GHExist[UHE_exist,cenario,periodo] >= dados.GSF[cenario]*UHE_existente.UHE[UHE_exist][3])
                    else:
                        self.model.restricoes.add(self.model.GHExist[UHE_exist,cenario,periodo] >= UHE_existente.UHE[UHE_exist][4])

        #restrição de geração limitada pela capacidade instalada e garantia física para hidrelétricas expansão
        for cenario in range(numcenario):
            for UHEexp in range (G_exp.numUHE):
                #Garantia Física
                self.model.restricoes.add(sum(self.model.GUHE_exp[UHEexp,cenario,periodo] for periodo in range(24*numperiodo)) <= dados.GSF[cenario]*G_exp.UHE_exp[UHEexp][3]*24*numperiodo)        
                for periodo in range(24*numperiodo):
                    #Expansão de capacidade
                    self.model.restricoes.add(self.model.GUHE_exp[UHEexp,cenario,periodo] <= self.model.binaryUHE_exp[UHEexp]*G_exp.UHE_exp[UHEexp][2])
                    #Geração Hidrelétrica Mínima
                    if (G_exp.UHE_exp[UHEexp][5] > dados.GSF[cenario]*G_exp.UHE_exp[UHEexp][3]):
                        self.model.restricoes.add(self.model.GUHE_exp[UHEexp,cenario,periodo] >= self.model.binaryUHE_exp[UHEexp]*dados.GSF[cenario]*G_exp.UHE_exp[UHEexp][3])
                    else:
                        self.model.restricoes.add(self.model.GUHE_exp[UHEexp,cenario,periodo] >= self.model.binaryUHE_exp[UHEexp]*G_exp.UHE_exp[UHEexp][5])
        #Restrição de expansão por configuração (soma das binárias <= 1)
        for repetida in range(G_exp.numConfsUHEexp):
            self.model.restricoes.add(sum(self.model.binaryUHE_exp[UHEexp]*G_exp.MatrizConfUHE[repetida][UHEexp] for UHEexp in range(G_exp.numUHE))<= 1)

        #restrição de geração limitada pela capacidade instalada e GTminima para termelétricas existentes
        for periodo in range(24*numperiodo):
            for cenario in range(numcenario):
                for UTEexist in range (UTE_existente.numUTE):
                    self.model.restricoes.add(self.model.GTExist[UTEexist,cenario,periodo] <= UTE_existente.UTE[UTEexist][2])
                    self.model.restricoes.add(self.model.GTExist[UTEexist,cenario,periodo] >= UTE_existente.UTE[UTEexist][3])

        #restrição de geração limitada pela capacidade instalada e GTminima para termelétricas expansão
        for periodo in range(24*numperiodo):
            for cenario in range(numcenario):
                for UTEexp in range (G_exp.numUTE):
                    self.model.restricoes.add(self.model.GUTE_exp[UTEexp,cenario,periodo] <= self.model.CapacidadeUTE_exp[UTEexp])
                    self.model.restricoes.add(self.model.GUTE_exp[UTEexp,cenario,periodo] >= G_exp.UTE_exp[UTEexp][cenario][0]*self.model.CapacidadeUTE_exp[UTEexp])
                    self.model.restricoes.add(self.model.CapacidadeUTE_exp[UTEexp] >= G_exp.UTE_exp[UTEexp][cenario][3])
                    self.model.restricoes.add(self.model.CapacidadeUTE_exp[UTEexp] <= G_exp.UTE_exp[UTEexp][cenario][4])

        #!restrição de geração limitada pela capacidade instalada e GTminima para termelétricas Retrofit
        for periodo in range(24*numperiodo):
            for cenario in range(numcenario):
                for uteret in range (G_exp.numUTERet):
                    self.model.restricoes.add(self.model.GUTE_Ret[uteret,cenario,periodo] <= self.model.IntegerUTE_Ret[uteret]*G_exp.UTE_Ret[uteret][cenario][3])
                    self.model.restricoes.add(self.model.GUTE_Ret[uteret,cenario,periodo] >= self.model.IntegerUTE_Ret[uteret]*G_exp.UTE_Ret[uteret][cenario][0]*G_exp.UTE_Ret[uteret][cenario][3])
                    self.model.restricoes.add(self.model.IntegerUTE_Ret[uteret] <= 1)

        #restrição de fator de forma para GOUTRAS_exp
        for periodo in range(24*numperiodo):
            for cenario in range(numcenario):
                for outras in range (G_exp.numOUTRAS):
                    periodofator = math.trunc(periodo/24)
                    horafator = periodo - periodofator*24
                    self.model.restricoes.add(self.model.GOUTRAS_exp[outras,cenario,periodo] == G_exp.OUTRAS_exp[outras][periodofator][horafator+3]*self.model.CapacidadeOUTRAS_exp[outras])
                    self.model.restricoes.add(self.model.CapacidadeOUTRAS_exp[outras] >= G_exp.OUTRAS_exp[outras][periodofator][1])
                    self.model.restricoes.add(self.model.CapacidadeOUTRAS_exp[outras] <= G_exp.OUTRAS_exp[outras][periodofator][2])
        
        #restrição de geração limitada pela capacidade instalada e garantia física para PCH Expansão
        for cenario in range(numcenario):
            for pchexp in range (PCH_exp.numPCH):
                #Garantia Física
                self.model.restricoes.add(sum(self.model.GPCH_exp[pchexp,cenario,periodo] for periodo in range(24*numperiodo)) <= self.model.IntegerPCH_exp[pchexp]*dados.GSF[cenario]*PCH_exp.PCH_exp[pchexp][5]*24*float(numperiodo))        
                for periodo in range(24*numperiodo):
                    #Potencia
                    self.model.restricoes.add(self.model.GPCH_exp[pchexp,cenario,periodo] <= self.model.IntegerPCH_exp[pchexp]*PCH_exp.PCH_exp[pchexp][4])
                    #numero de PCHs positivo ou zero
                    self.model.restricoes.add(self.model.IntegerPCH_exp[pchexp] >= 0)
                    #e numero de PCHs respeita o limite de número de PCHs
                    #numero de PCHs positivo ou zero
                    self.model.restricoes.add(self.model.IntegerPCH_exp[pchexp] >= PCH_exp.PCH_exp[pchexp][2])
                    self.model.restricoes.add(self.model.IntegerPCH_exp[pchexp] <= PCH_exp.PCH_exp[pchexp][3])

        for cenario in range(numcenario):
            for periodo in range(24*numperiodo):
                self.model.restricoes.add(self.model.Total_GHExist[cenario, periodo] == sum(self.model.GHExist[uheexist, cenario, periodo] for uheexist in range(UHE_existente.numUHE)))
                self.model.restricoes.add(self.model.Total_GTExist[cenario, periodo] == sum(self.model.GTExist[uteexist, cenario, periodo] for uteexist in range(UTE_existente.numUTE)))
                self.model.restricoes.add(self.model.Total_GOUTRAS_exp[cenario, periodo] == sum(self.model.GOUTRAS_exp[outras, cenario, periodo] for outras in range(G_exp.numOUTRAS)))
                self.model.restricoes.add(self.model.Total_GUTE_exp[cenario, periodo] == sum(self.model.GUTE_exp[uteexp, cenario, periodo] for uteexp in range(G_exp.numUTE)))
                self.model.restricoes.add(self.model.Total_GUTE_Ret[cenario,periodo] == sum(self.model.GUTE_Ret[uteret, cenario, periodo] for uteret in range(G_exp.numUTERet)))
                self.model.restricoes.add(self.model.Total_GUHE_exp[cenario, periodo] == sum(self.model.GUHE_exp[uheexp, cenario, periodo] for uheexp in range(G_exp.numUHE))) 
                self.model.restricoes.add(self.model.Total_GPCH_exp[cenario, periodo] == sum(self.model.GPCH_exp[pchexp, cenario, periodo] for pchexp in range(PCH_exp.numPCH)))

        #Custo de geração termelétrica existente, expansão outras
        self.model.restricoes.add(self.model.CustoGTExist == sum(dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*365*self.model.GTExist[UTEexist,cenario,periodo]*UTE_existente.UTE[UTEexist][4] for UTEexist in range(UTE_existente.numUTE) for periodo in range(numperiodo*24) for cenario in range(numcenario)))
        self.model.restricoes.add(self.model.CustoexpOutras == sum(self.model.CapacidadeOUTRAS_exp[outras]*G_exp.OUTRAS_exp[outras][0][0] for outras in range(G_exp.numOUTRAS)))
        self.model.restricoes.add(self.model.CustoexpUTEs == sum(dados.ProbCenario[cenario]*self.model.CapacidadeUTE_exp[utes]*G_exp.UTE_exp[utes][cenario][2] for utes in range(G_exp.numUTE) for cenario in range(numcenario)) + sum(dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*365*self.model.GUTE_exp[utes,cenario,periodo]*G_exp.UTE_exp[utes][cenario][1] for utes in range(G_exp.numUTE) for periodo in range(24*numperiodo) for cenario in range(numcenario)))
        self.model.restricoes.add(self.model.CustoexpUTERet == sum(dados.ProbCenario[cenario]*self.model.IntegerUTE_Ret[uteret]*G_exp.UTE_Ret[uteret][cenario][2] for uteret in range(G_exp.numUTERet) for cenario in range(numcenario)) + sum(dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*365*self.model.GUTE_Ret[uteret,cenario,periodo]*G_exp.UTE_Ret[uteret][cenario][1] for uteret in range(G_exp.numUTERet) for periodo in range(24*numperiodo) for cenario in range(numcenario)))
        self.model.restricoes.add(self.model.CustoexpUHEs == sum(self.model.binaryUHE_exp[uhes]*G_exp.UHE_exp[uhes][4] for uhes in range(G_exp.numUHE)))
        #A soma dos custos de PCH consideram o degrau por capacidade, representado por uma PA de A1 = CAPEX e r = Degrau
        self.model.restricoes.add(self.model.CustoexpPCHs == sum(((self.model.IntegerPCH_exp[pchexp])*PCH_exp.PCH_exp[pchexp][7]*PCH_exp.PCH_exp[pchexp][4] + 2*self.model.IntegerPCH_exp[pchexp]*PCH_exp.PCH_exp[pchexp][4]*(PCH_exp.PCH_exp[pchexp][6]-PCH_exp.PCH_exp[pchexp][7]))/2 for pchexp in range(PCH_exp.numPCH)))

        def FObjetivo (model):
            return self.model.CustoGTExist + self.model.CustoexpOutras + self.model.CustoexpUTEs + self.model.CustoexpUTERet + self.model.CustoexpUHEs + self.model.CustoexpPCHs

        self.model.objetivo = pyo.Objective(rule = FObjetivo, sense = pyo.minimize)

        self.solver = SolverFactory('cbc', executable=r"C:\\CoinAll\\bin\\cbc.exe")
        self.solver.options['mipgap'] = 0.005
        results = self.solver.solve(self.model, load_solutions=True, tee=True)
        self.model.solutions.store_to(results)

        results.write(filename = os.path.join(sys.path[0], "resultados.json"), format='json')