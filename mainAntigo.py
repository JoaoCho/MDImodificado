from importaCarga import importaCarga
from importaUHE_existente import importaUHE_existente
from importaUTE_existente import importaUTE_existente
from importaEXP import importaEXP
from importaDadosGerais import importaDadosGerais
from pyomo.opt import SolverFactory
from pyomo.environ import *
import math 
import numpy

#.carga[cenario][periodo][carga] onde a carga é discriminada para cada hora do dia
carga = importaCarga()
numcenario = carga.numcenario
numperiodo = carga.numperiodo

#.UHE[UHE][caracteristica] onde caracteristica[0] = ID, caracteristica[1] = nome, caracteristica[2] = Capacidade e caracteristica[3] = Garantia Física
#.numUHE é o numero de UHEs existnetes considerados
UHE_existente = importaUHE_existente()

#.UTE[UTE][caracteristica] onde caracteristica[0] = ID, caracteristica[1] = nome, caracteristica[2] = Capacidade, caracteristica[3] = GTMin, e   caracteristica[4] = CVU
#.numUTE é o numero de UTEs existentes consideradas
UTE_existente = importaUTE_existente()

#.OUTRAS_exp[tecnologia][periodo][fator capacidade] onde o fator capacidade é discriminado para cada hora do dia
#.UTE_exp[IDUTE][cenario][propriedade] onde o propriedade[0] é GTMin (em %), propriedade[1] é o CVU e propriedade[2] é o CAPEX
#.UHE_exp[UHE][caracteristica] onde caracteristica[0] = ID, caracteristica[1] = nome, caracteristica[2] = Capacidade, caracteristica[3] = Garantia Física e caracteristica[4] = CAPEX
G_exp = importaEXP()

#GSF[cenario] que estabelece cada GSF para cada cenário e CVU[cenario] que estabelece cada multiplicador do CVU para cada cenário
dados = importaDadosGerais()

#cria concrete model no pyomo
model = ConcreteModel()

#cria variáveis de decisão para geração[usina][cenario][periodo]

model.GHExist = Var(range(UHE_existente.numUHE), range(numcenario), range(24*numperiodo), domain = NonNegativeReals)
model.GTExist = Var(range(UTE_existente.numUTE), range(numcenario), range(24*numperiodo), domain = NonNegativeReals)

model.CustoGTExist = Var(initialize = 0, domain = NonNegativeReals)
model.CustoexpOutras = Var(initialize = 0, domain = NonNegativeReals)
model.CustoexpUTEs = Var(initialize = 0, domain = NonNegativeReals)
model.CustoexpUHEs = Var(initialize = 0, domain = NonNegativeReals)

model.CustoTotal = Var(initialize = 0, domain = NonNegativeReals)

model.CapacidadeOUTRAS_exp = Var(range(G_exp.numOUTRAS), domain = NonNegativeReals)

model.CapacidadeUTE_exp = Var(range(G_exp.numUTE), domain = NonNegativeReals)


model.GOUTRAS_exp = Var(range(G_exp.numOUTRAS), range(numcenario), range(24*numperiodo), domain = NonNegativeReals)
model.GUTE_exp = Var(range(G_exp.numUTE), range(numcenario), range(24*numperiodo), domain = NonNegativeReals)
model.GUHE_exp = Var(range(G_exp.numUHE), range(numcenario), range(24*numperiodo), domain = NonNegativeReals)
model.binaryUHE_exp = Var(range(G_exp.numUHE), domain=Binary)

model.restricoes = ConstraintList()

#restrição de atendimento de carga
for periodo in range(24*numperiodo):
    for cenario in range(numcenario):
        periodocarga = math.trunc(periodo/24)
        horacarga = periodo - periodocarga*24
        model.restricoes.add(sum(model.GHExist[UHEexist,cenario,periodo] for UHEexist in range(UHE_existente.numUHE))
         + sum(model.GTExist[UTEexist,cenario,periodo] for UTEexist in range(UTE_existente.numUTE))
         + sum(model.GOUTRAS_exp[OUTRAS_exp,cenario,periodo] for OUTRAS_exp in range(G_exp.numOUTRAS))
         + sum(model.GUTE_exp[UTE_exp,cenario,periodo] for UTE_exp in range(G_exp.numUTE))
         + sum(model.GUHE_exp[UHE_exp,cenario,periodo] for UHE_exp in range(G_exp.numUHE))
         == carga.carga[cenario][periodocarga][horacarga])

#restrição de geração limitada pela capacidade instalada e garantia física para hidrelétricas existentes
for cenario in range(numcenario):
    for UHE_exist in range (UHE_existente.numUHE):
        #Garantia Física
        model.restricoes.add(sum(model.GHExist[UHE_exist,cenario,periodo] for periodo in range(24*numperiodo)) <= dados.GSF[cenario]*UHE_existente.UHE[UHE_exist][3]*24*float(numperiodo))        
        for periodo in range(24*numperiodo):
            #Potencia
            model.restricoes.add(model.GHExist[UHE_exist,cenario,periodo] <= UHE_existente.UHE[UHE_exist][2])

#restrição de geração limitada pela capacidade instalada e garantia física para hidrelétricas expansão
for cenario in range(numcenario):
    for UHEexp in range (G_exp.numUHE):
        #Garantia Física
        model.restricoes.add(sum(model.GUHE_exp[UHEexp,cenario,periodo] for periodo in range(24*numperiodo)) <= dados.GSF[cenario]*G_exp.UHE_exp[UHEexp][3]*24*numperiodo)        
        for periodo in range(24*numperiodo):
            #Expansão de capacidade
            model.restricoes.add(model.GUHE_exp[UHEexp,cenario,periodo] <= model.binaryUHE_exp[UHEexp]*G_exp.UHE_exp[UHEexp][2])

#restrição de geração limitada pela capacidade instalada e GTminima para termelétricas existentes
for periodo in range(24*numperiodo):
    for cenario in range(numcenario):
        for UTEexist in range (UTE_existente.numUTE):
            model.restricoes.add(model.GTExist[UTEexist,cenario,periodo] <= UTE_existente.UTE[UTEexist][2])
            model.restricoes.add(model.GTExist[UTEexist,cenario,periodo] >= UTE_existente.UTE[UTEexist][3])

#restrição de geração limitada pela capacidade instalada e GTminima para termelétricas expansão
for periodo in range(24*numperiodo):
    for cenario in range(numcenario):
        for UTEexp in range (G_exp.numUTE):
            model.restricoes.add(model.GUTE_exp[UTEexp,cenario,periodo] <= model.CapacidadeUTE_exp[UTEexp])
            model.restricoes.add(model.GUTE_exp[UTEexp,cenario,periodo] >= G_exp.UTE_exp[UTEexp][cenario][0]*model.CapacidadeUTE_exp[UTEexp])

#restrição de fator de forma para GOUTRAS_exp
for periodo in range(24*numperiodo):
    for cenario in range(numcenario):
        for outras in range (G_exp.numOUTRAS):
            periodofator = math.trunc(periodo/24)
            horafator = periodo - periodofator*24
            model.restricoes.add(model.GOUTRAS_exp[outras,cenario,periodo] == G_exp.OUTRAS_exp[outras][periodofator][horafator+2]*model.CapacidadeOUTRAS_exp[outras])
            model.restricoes.add(model.CapacidadeOUTRAS_exp[outras] <= G_exp.OUTRAS_exp[outras][periodofator][1])
            
            #!!!INSERIR RESTRIÇÃO DE CAPACIDADE POR CENÁRIO!!!


#Custo de geração termelétrica existente, expansão outras
model.restricoes.add(model.CustoGTExist == sum(dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*365*model.GTExist[UTEexist,cenario,periodo]*UTE_existente.UTE[UTEexist][4] for UTEexist in range(UTE_existente.numUTE) for periodo in range(numperiodo*24) for cenario in range(numcenario)))
model.restricoes.add(model.CustoexpOutras == sum(model.CapacidadeOUTRAS_exp[outras]*G_exp.OUTRAS_exp[outras][0][0] for outras in range(G_exp.numOUTRAS)))
model.restricoes.add(model.CustoexpUTEs == sum(dados.ProbCenario[cenario]*model.CapacidadeUTE_exp[utes]*G_exp.UTE_exp[utes][cenario][2] for utes in range(G_exp.numUTE) for cenario in range(numcenario)) + sum(dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*365*model.GUTE_exp[utes,cenario,periodo]*G_exp.UTE_exp[utes][cenario][1] for utes in range(G_exp.numUTE) for periodo in range(24*numperiodo) for cenario in range(numcenario)))
model.restricoes.add(model.CustoexpUHEs == sum(model.binaryUHE_exp[uhes]*G_exp.UHE_exp[uhes][2]*G_exp.UHE_exp[uhes][4] for uhes in range(G_exp.numUHE)))

def FObjetivo (model):
    return model.CustoGTExist + model.CustoexpOutras + model.CustoexpUTEs + model.CustoexpUHEs

model.objetivo = Objective(rule = FObjetivo, sense = minimize)

solver = SolverFactory('cbc', executable="C:\\CoinAll\\bin\\cbc.exe")
results = solver.solve(model, load_solutions=True)
model.solutions.store_to(results)
results.write(filename=r'C:\JoaoCho\Python\MDI 24h\Versao main Antigo - Teste PDE\resultados.json', format='json')

file1 = open(r"C:\JoaoCho\Python\MDI 24h\Versao main Antigo - Teste PDE\Resultados\UHE_existente.csv","w") 

txt_UHEexist = "Nome;Cenario;Capacidade Instalada;Garantia Física"

for periodo in range(24*numperiodo):
    txt_UHEexist = txt_UHEexist+";G_periodo"+str(periodo+1)

file1.write(txt_UHEexist+"\n")

for cenario in range(numcenario):
    for uhe_exist in range(UHE_existente.numUHE):
        txt_UHEexist = UHE_existente.UHE[uhe_exist][1]+";"+str(cenario+1)+";"+str(UHE_existente.UHE[uhe_exist][2]).replace(".",",")+";"+str(UHE_existente.UHE[uhe_exist][3]).replace(".",",")
        for periodo in range(24*numperiodo):
            txt_UHEexist = txt_UHEexist +";"+ str(value(model.GHExist[uhe_exist,cenario,periodo])).replace(".",",")
        file1.write(txt_UHEexist+"\n")

file1 = open(r"C:\JoaoCho\Python\MDI 24h\Versao main Antigo - Teste PDE\Resultados\UTE_existente.csv","w")
txt_UTEexist = "Nome;Cenario;Capacidade Instalada;GT Mínimo; CVU"

for periodo in range(24*numperiodo):
    txt_UTEexist = txt_UTEexist+";G_periodo"+str(periodo+1)
file1.write(txt_UTEexist+"\n")

for cenario in range(numcenario):
    for ute_exist in range(UTE_existente.numUTE):
        txt_UTEexist = UTE_existente.UTE[ute_exist][1]+";"+str(cenario+1)+";"+str(UTE_existente.UTE[ute_exist][2]).replace(".",",")+";"+str(UTE_existente.UTE[ute_exist][3]).replace(".",",")+";"+str(UTE_existente.UTE[ute_exist][4]).replace(".",",")
        for periodo in range(24*numperiodo):
            txt_UTEexist = txt_UTEexist +";"+ str(value(model.GTExist[ute_exist,cenario,periodo])).replace(".",",")
        file1.write(txt_UTEexist+"\n")

file1 = open(r"C:\JoaoCho\Python\MDI 24h\Versao main Antigo - Teste PDE\Resultados\OUTRAS_expansao.csv","w")

txt_OUTRASexp = "Nome;Cenario;Capacidade máxima;Capacidade Instalada Projetada;LCOE"
for periodo in range(24*numperiodo):
    txt_OUTRASexp = txt_OUTRASexp+";G_periodo"+str(periodo+1)
file1.write(txt_OUTRASexp+"\n")

for cenario in range(numcenario):
    for OUTRAS_exp in range(G_exp.numOUTRAS):
        txt_OUTRASexp = G_exp.nomeOUTRAS_exp[OUTRAS_exp]+";"+str(cenario+1)+";"+str(G_exp.OUTRAS_exp[OUTRAS_exp][cenario][1]).replace(".",",")+";"+str(value(model.CapacidadeOUTRAS_exp[OUTRAS_exp])).replace(".",",")+";"+str(G_exp.OUTRAS_exp[OUTRAS_exp][cenario][0]).replace(".",",")

        for periodo in range(24*numperiodo):
            txt_OUTRASexp = txt_OUTRASexp +";"+ str(value(model.GOUTRAS_exp[OUTRAS_exp,cenario,periodo])).replace(".",",")

        file1.write(txt_OUTRASexp+"\n")     

file1 = open(r"C:\JoaoCho\Python\MDI 24h\Versao main Antigo - Teste PDE\Resultados\UHE_expansao.csv","w")

txt_UHEexp = "Nome;Cenario;Capacidade;Garantia Física;CAPEX; Investimento"

for periodo in range(24*numperiodo):
    txt_UHEexp = txt_UHEexp+";G_periodo"+str(periodo+1)

file1.write(txt_UHEexp+"\n")

for cenario in range(numcenario):
    for UHE_exp in range(G_exp.numUHE):
        txt_UHEexp = G_exp.nomeUHE_exp[UHE_exp]+";"+str(cenario+1)+";"+str(G_exp.UHE_exp[UHE_exp][2]).replace(".",",")+";"+str(G_exp.UHE_exp[UHE_exp][3]).replace(".",",")+";"+str(G_exp.UHE_exp[UHE_exp][4]).replace(".",",")+";"+str(value(model.binaryUHE_exp[UHE_exp]))

        for periodo in range(24*numperiodo):
            txt_UHEexp = txt_UHEexp +";"+ str(value(model.GUHE_exp[UHE_exp,cenario,periodo])).replace(".",",")

        file1.write(txt_UHEexp+"\n")  


file1 = open(r"C:\JoaoCho\Python\MDI 24h\Versao main Antigo - Teste PDE\Resultados\UTE_expansao.csv","w")

txt_UTEexp = "Nome;Cenario;Capacidade Instalada Projetada;GT Mínimo; CVU; CAPEX"

for periodo in range(24*numperiodo):
    txt_UTEexp = txt_UTEexp+";G_periodo"+str(periodo+1)

file1.write(txt_UTEexp+"\n")

for cenario in range(numcenario):
    for UTE_exp in range(G_exp.numUTE):
        txt_UTEexp = G_exp.nomeUTE_exp[UTE_exp]+";"+str(cenario+1)+";"+str(value(model.CapacidadeUTE_exp[UTE_exp])).replace(".",",")+";"+str(G_exp.UTE_exp[UTE_exp][cenario][0]).replace(".",",")+";"+str(G_exp.UTE_exp[UTE_exp][cenario][1]).replace(".",",")+";"+str(G_exp.UTE_exp[UTE_exp][cenario][2]).replace(".",",")

        for periodo in range(24*numperiodo):
            txt_UTEexp = txt_UTEexp +";"+ str(value(model.GUTE_exp[UTE_exp,cenario,periodo])).replace(".",",")

        file1.write(txt_UTEexp+"\n")  