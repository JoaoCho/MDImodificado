from importaCarga import importaCarga
from importaUHE_existente import importaUHE_existente
from importaUTE_existente import importaUTE_existente
from importaEXP import importaEXP
from importaPCHexp import importaPCHexp
from importaDadosGerais import importaDadosGerais
from imprimeresultados import imprimeresultados
from Problema import Problema

dados = importaCarga()

print(dados.numperiodo)
