from importaCarga import importaCarga
from importaUHE_existente import importaUHE_existente
from importaUTE_existente import importaUTE_existente
from importaEXP import importaEXP
from importaPCHexp import importaPCHexp
from importaDadosGerais import importaDadosGerais
from imprimeresultados import imprimeresultados
from Problema import Problema
import winsound

print("Leitura de Dados")
#.carga[cenario][periodo] [carga] onde a carga é discriminada para cada hora do dia
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

#importa o PCH_exp.csv e cria uma matriz[PCH][caracteristica] onde caracteristica[0] = ID, caracteristica[1] = nome, caracteristica[2] = Número máximo de PCHs para expansão, , caracteristica[3] = Capacidade, caracteristica[4] = Garantia Física, caracteristica[5] = CAPEX e caracteristica[6] = Degrau de CAPEX por nova usina
PCH_exp = importaPCHexp()

#GSF[cenario] que estabelece cada GSF para cada cenário e CVU[cenario] que estabelece cada multiplicador do CVU para cada cenário
dados = importaDadosGerais()

print("Montagem do problema e resolução do solver")
#Cria o problem de otimização no pyomo com base nos vetores criados e imprime summary dos resultados
Modelo = Problema(carga, UHE_existente, UTE_existente, G_exp, PCH_exp, dados)

print("Impressão dos resultados")
#Imprime os resultados em CSV na pasta Resultados
imprimeresultados(carga, UHE_existente, UTE_existente, G_exp, PCH_exp, dados, Modelo)

winsound.Beep(2500, 500)

print("Fim")
