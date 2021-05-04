import math 
from pyomo.opt import SolverFactory
import pyomo.environ as pyo
import matplotlib.pyplot as plt
import matplotlib.ticker
from itertools import chain
import numpy as np 
import sys
import os
        
class imprimeresultados():
    def __init__(self, carga, UHE_existente, UTE_existente, G_exp, PCH_exp, dados, Modelo):
        numcenario = carga.numcenario
        numperiodo = carga.numperiodo

        #Imprime em csv os resultados de geração das UHEs existentes
        file1 = open(os.path.join(sys.path[0], "Resultados\\Planilhas\\UHE_existente.csv"),"w") 

        txt_UHEexist = "Nome;Cenario;Capacidade Instalada;Garantia Física"

        for periodo in range(24*numperiodo):
            txt_UHEexist = txt_UHEexist+";G_periodo"+str(periodo+1)

        file1.write(txt_UHEexist+"\n")

        for cenario in range(numcenario):
            for uhe_exist in range(UHE_existente.numUHE):
                txt_UHEexist = UHE_existente.UHE[uhe_exist][1]+";"+str(cenario+1)+";"+str(UHE_existente.UHE[uhe_exist][2]).replace(".",",")+";"+str(UHE_existente.UHE[uhe_exist][3]).replace(".",",")
                for periodo in range(24*numperiodo):
                    txt_UHEexist = txt_UHEexist +";"+ str(pyo.value(Modelo.model.GHExist[uhe_exist,cenario,periodo])).replace(".",",")
                file1.write(txt_UHEexist+"\n")


        #Imprime em csv o resultado de operação das UTEs existentes
        file1 = open(os.path.join(sys.path[0], "Resultados\\Planilhas\\UTE_existente.csv"),"w")
        txt_UTEexist = "Nome;Cenario;Capacidade Instalada;GT Mínimo; CVU"

        for periodo in range(24*numperiodo):
            txt_UTEexist = txt_UTEexist+";G_periodo"+str(periodo+1)
        file1.write(txt_UTEexist+"\n")

        for cenario in range(numcenario):
            for ute_exist in range(UTE_existente.numUTE):
                txt_UTEexist = UTE_existente.UTE[ute_exist][1]+";"+str(cenario+1)+";"+str(UTE_existente.UTE[ute_exist][2]).replace(".",",")+";"+str(UTE_existente.UTE[ute_exist][3]).replace(".",",")+";"+str(UTE_existente.UTE[ute_exist][4]).replace(".",",")
                for periodo in range(24*numperiodo):
                    txt_UTEexist = txt_UTEexist +";"+ str(pyo.value(Modelo.model.GTExist[ute_exist,cenario,periodo])).replace(".",",")
                file1.write(txt_UTEexist+"\n")

        #Imprime em csv a capacidade de expansão planejada e o resultado de operação das usinas "Outras"
        file1 = open(os.path.join(sys.path[0], "Resultados\\Planilhas\\OUTRAS_expansao.csv"),"w")

        txt_OUTRASexp = "Nome;Cenario;Capacidade mínima;Capacidade máxima;Capacidade Instalada Projetada;LCOE"
        for periodo in range(24*numperiodo):
            txt_OUTRASexp = txt_OUTRASexp+";G_periodo"+str(periodo+1)
        file1.write(txt_OUTRASexp+"\n")

        for cenario in range(numcenario):
            for OUTRAS_exp in range(G_exp.numOUTRAS):
                txt_OUTRASexp = G_exp.nomeOUTRAS_exp[OUTRAS_exp]+";"+str(cenario+1)+";"+str(G_exp.OUTRAS_exp[OUTRAS_exp][cenario][1]).replace(".",",")+";"+str(G_exp.OUTRAS_exp[OUTRAS_exp][cenario][2]).replace(".",",")+";"+str(pyo.value(Modelo.model.CapacidadeOUTRAS_exp[OUTRAS_exp])).replace(".",",")+";"+str(G_exp.OUTRAS_exp[OUTRAS_exp][cenario][0]).replace(".",",")

                for periodo in range(24*numperiodo):
                    txt_OUTRASexp = txt_OUTRASexp +";"+ str(pyo.value(Modelo.model.GOUTRAS_exp[OUTRAS_exp,cenario,periodo])).replace(".",",")

                file1.write(txt_OUTRASexp+"\n")     

        #Imprime em csv a capacidade de expansão planejada e o resultado de operação das usinas "UHEs"
        file1 = open(os.path.join(sys.path[0], "Resultados\\Planilhas\\UHE_expansao.csv"),"w")

        txt_UHEexp = "Nome;Cenario;Capacidade;Garantia Física;CAPEX; Investimento"

        for periodo in range(24*numperiodo):
            txt_UHEexp = txt_UHEexp+";G_periodo"+str(periodo+1)

        file1.write(txt_UHEexp+"\n")

        for cenario in range(numcenario):
            for UHE_exp in range(G_exp.numUHE):
                txt_UHEexp = G_exp.UHE_exp[UHE_exp][1]+";"+str(cenario+1)+";"+str(G_exp.UHE_exp[UHE_exp][2]).replace(".",",")+";"+str(G_exp.UHE_exp[UHE_exp][3]).replace(".",",")+";"+str(G_exp.UHE_exp[UHE_exp][4]).replace(".",",")+";"+str(pyo.value(Modelo.model.binaryUHE_exp[UHE_exp]))

                for periodo in range(24*numperiodo):
                    txt_UHEexp = txt_UHEexp +";"+ str(pyo.value(Modelo.model.GUHE_exp[UHE_exp,cenario,periodo])).replace(".",",")

                file1.write(txt_UHEexp+"\n")  

        #Imprime em csv a capacidade de expansão planejada e o resultado de operação das usinas "UTEs"
        file1 = open(os.path.join(sys.path[0], "Resultados\\Planilhas\\UTE_expansao.csv"),"w")

        txt_UTEexp = "Nome;Cenario;Cap Mínimo;Cap Máximo;Capacidade Instalada Projetada;GT Mínimo; CVU; CAPEX"

        for periodo in range(24*numperiodo):
            txt_UTEexp = txt_UTEexp+";G_periodo"+str(periodo+1)

        file1.write(txt_UTEexp+"\n")

        for cenario in range(numcenario):
            for UTE_exp in range(G_exp.numUTE):
                txt_UTEexp = G_exp.nomeUTE_exp[UTE_exp]+";"+str(cenario+1)+";"+str(G_exp.UTE_exp[UTE_exp][cenario][3]).replace(".",",")+";"+str(G_exp.UTE_exp[UTE_exp][cenario][4]).replace(".",",")+";"+str(pyo.value(Modelo.model.CapacidadeUTE_exp[UTE_exp])).replace(".",",")+";"+str(G_exp.UTE_exp[UTE_exp][cenario][0]).replace(".",",")+";"+str(G_exp.UTE_exp[UTE_exp][cenario][1]).replace(".",",")+";"+str(G_exp.UTE_exp[UTE_exp][cenario][2]).replace(".",",")

                for periodo in range(24*numperiodo):
                    txt_UTEexp = txt_UTEexp +";"+ str(pyo.value(Modelo.model.GUTE_exp[UTE_exp,cenario,periodo])).replace(".",",")

                file1.write(txt_UTEexp+"\n")  

        #Imprime em csv a capacidade de expansão planejada e o resultado de operação das usinas "UTERet"
        file1 = open(os.path.join(sys.path[0], "Resultados\\Planilhas\\UTE_retrofit.csv"),"w")

        txt_UTERet = "Nome;Cenario;CAPEX;Capacidade;GT Mínimo;CVU;Investimento"

        for periodo in range(24*numperiodo):
            txt_UTERet = txt_UTERet+";G_periodo"+str(periodo+1)

        file1.write(txt_UTERet+"\n")

        for cenario in range(numcenario):
            for UTE_ret in range(G_exp.numUTERet):
                txt_UTERet = G_exp.nomeUTERet[UTE_ret]+";"+str(cenario+1)+";"+str(G_exp.UTE_Ret[UTE_ret][cenario][2]).replace(".",",")+";"+str(G_exp.UTE_Ret[UTE_ret][cenario][3]).replace(".",",")+";"+str(G_exp.UTE_Ret[UTE_ret][cenario][0]).replace(".",",")+";"+str(G_exp.UTE_Ret[UTE_ret][cenario][1]).replace(".",",")+";"+str(pyo.value(Modelo.model.IntegerUTE_Ret[UTE_ret])).replace(".",",")

                for periodo in range(24*numperiodo):
                    txt_UTERet = txt_UTERet +";"+ str(pyo.value(Modelo.model.GUTE_Ret[UTE_ret,cenario,periodo])).replace(".",",")

                file1.write(txt_UTERet+"\n")  

        #Imprime em csv a capacidade de expansão planejada e o resultado de operação das usinas "PCHs"
        file1 = open(os.path.join(sys.path[0], "Resultados\\Planilhas\\PCH_expansao.csv"),"w")

        txt_PCHexp = "Nome;Cenario;Capacidade;Garantia Física;CAPEX; Degrau de CAPEX; Numero mínimo de PCHs;Numero máximo de PCHs; Numero de PCHs Planejadas"

        for periodo in range(24*numperiodo):
            txt_PCHexp = txt_PCHexp+";G_periodo"+str(periodo+1)

        file1.write(txt_PCHexp+"\n")

        for cenario in range(numcenario):
            for pchexp in range(PCH_exp.numPCH):
                txt_PCHexp = PCH_exp.PCH_exp[pchexp][1]+";"+str(cenario+1)+";"+str(PCH_exp.PCH_exp[pchexp][4]).replace(".",",")+";"+str(PCH_exp.PCH_exp[pchexp][5]).replace(".",",")+";"+str(PCH_exp.PCH_exp[pchexp][6]).replace(".",",")+";"+str(PCH_exp.PCH_exp[pchexp][7]).replace(".",",")+";"+str(PCH_exp.PCH_exp[pchexp][2]).replace(".",",")+";"+str(PCH_exp.PCH_exp[pchexp][3]).replace(".",",")+";"+str(pyo.value(Modelo.model.IntegerPCH_exp[pchexp]))

                for periodo in range(24*numperiodo):
                    txt_PCHexp = txt_PCHexp +";"+ str(pyo.value(Modelo.model.GPCH_exp[pchexp,cenario,periodo])).replace(".",",")

                file1.write(txt_PCHexp+"\n")
        
        #Cria Gráfico de Geração por categoria vs Demanda com separação para "outras" fontes em eólica e solar
        GHExist_total = [[0]*24*numperiodo for i in range(numcenario)]
        GTExist_total = [[0]*24*numperiodo for i in range(numcenario)]
        GOUTRAS_exp_total = [[0]*24*numperiodo for i in range(numcenario)]
        GUTE_exp_total = [[0]*24*numperiodo for i in range(numcenario)]
        GUTE_ret_total = [[0]*24*numperiodo for i in range(numcenario)]
        GUHE_exp_total = [[0]*24*numperiodo for i in range(numcenario)]
        GPCH_exp_total = [[0]*24*numperiodo for i in range(numcenario)]
        Demanda = [[0]*24*numperiodo for i in range(numcenario)]
        EixoX_num = [[0]*24*numperiodo for i in range(numcenario)]

        FVExpTotal = [[0]*24*numperiodo for i in range(numcenario)]
        EOLExpTotal = [[0]*24*numperiodo for i in range(numcenario)]
        OutrasExpTotal = [[0]*24*numperiodo for i in range(numcenario)]

        FVExpTotalAcum = [[0]*24*numperiodo for i in range(numcenario)]
        EOLExpTotalAcum = [[0]*24*numperiodo for i in range(numcenario)]
        OutrasExpTotalAcum = [[0]*24*numperiodo for i in range(numcenario)]               

        for cenario in range(numcenario):
            for periodo in range(24*numperiodo):
                periodocarga = math.trunc(periodo/24)
                horacarga = periodo - periodocarga*24
                Demanda[cenario][periodo] = carga.carga[cenario][periodocarga][horacarga]
                if (pyo.value(Modelo.model.Total_GHExist[cenario, periodo]) != 0):                 
                    GHExist_total[cenario][periodo] = pyo.value(Modelo.model.Total_GHExist[cenario, periodo])
                else:                
                    GHExist_total[cenario][periodo] = 0
                
                if (pyo.value(Modelo.model.Total_GTExist[cenario, periodo]) != 0):
                    GTExist_total[cenario][periodo] = pyo.value(Modelo.model.Total_GTExist[cenario, periodo]) + pyo.value(Modelo.model.Total_GHExist[cenario, periodo])
                else:
                    GTExist_total[cenario][periodo] = GHExist_total[cenario][periodo]
                
                if (pyo.value(Modelo.model.Total_GOUTRAS_exp[cenario, periodo]) != 0):
                    GOUTRAS_exp_total[cenario][periodo] = pyo.value(Modelo.model.Total_GOUTRAS_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GTExist[cenario, periodo]) + pyo.value(Modelo.model.Total_GHExist[cenario, periodo])
                else:
                    GUTE_exp_total[cenario][periodo] = GTExist_total[cenario][periodo]

                if (pyo.value(Modelo.model.Total_GUHE_exp[cenario, periodo]) != 0):
                    GUHE_exp_total[cenario][periodo] = pyo.value(Modelo.model.Total_GUHE_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GOUTRAS_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GTExist[cenario, periodo]) + pyo.value(Modelo.model.Total_GHExist[cenario, periodo])
                else:
                    GUHE_exp_total[cenario][periodo] = GUTE_exp_total[cenario][periodo] 

                if (pyo.value(Modelo.model.Total_GUTE_Ret[cenario, periodo]) != 0):                 
                    GUTE_ret_total[cenario][periodo] = pyo.value(Modelo.model.Total_GUHE_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GOUTRAS_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GTExist[cenario, periodo]) + pyo.value(Modelo.model.Total_GHExist[cenario, periodo]) + pyo.value(Modelo.model.Total_GUTE_Ret[cenario, periodo])
                else:
                    GUTE_ret_total[cenario][periodo] = 0

                if (pyo.value(Modelo.model.Total_GUTE_exp[cenario, periodo]) != 0):                 
                    GUTE_exp_total[cenario][periodo] = pyo.value(Modelo.model.Total_GUTE_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GUHE_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GOUTRAS_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GTExist[cenario, periodo]) + pyo.value(Modelo.model.Total_GHExist[cenario, periodo]) + pyo.value(Modelo.model.Total_GUTE_Ret[cenario, periodo])
                else:
                    GUTE_exp_total[cenario][periodo] = GUTE_ret_total[cenario][periodo]                

                if (pyo.value(Modelo.model.Total_GPCH_exp[cenario, periodo]) != 0):                 
                    GPCH_exp_total[cenario][periodo] = pyo.value(Modelo.model.Total_GPCH_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GUTE_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GUHE_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GOUTRAS_exp[cenario, periodo]) + pyo.value(Modelo.model.Total_GTExist[cenario, periodo]) + pyo.value(Modelo.model.Total_GHExist[cenario, periodo]) + pyo.value(Modelo.model.Total_GUTE_Ret[cenario, periodo])
                else:
                    GPCH_exp_total[cenario][periodo] = GUTE_exp_total[cenario][periodo]

                EixoX_num[cenario][periodo] = periodo

                for usina in range(G_exp.numOUTRAS):
                    if "EOL" in G_exp.nomeOUTRAS_exp[usina]:
                        EOLExpTotal[cenario][periodo] = EOLExpTotal[cenario][periodo]+pyo.value(Modelo.model.GOUTRAS_exp[usina, cenario, periodo])
                    elif "Solar" in G_exp.nomeOUTRAS_exp[usina]:
                        FVExpTotal[cenario][periodo] = FVExpTotal[cenario][periodo]+pyo.value(Modelo.model.GOUTRAS_exp[usina, cenario, periodo])
                    else:
                        OutrasExpTotal[cenario][periodo] = OutrasExpTotal[cenario][periodo]+pyo.value(Modelo.model.GOUTRAS_exp[usina, cenario, periodo])
            
            for periodo in range (24*numperiodo):
                FVExpTotalAcum[cenario][periodo] = FVExpTotal[cenario][periodo]
                EOLExpTotalAcum[cenario][periodo] = EOLExpTotal[cenario][periodo] + FVExpTotal[cenario][periodo]
                OutrasExpTotalAcum[cenario][periodo] = OutrasExpTotal[cenario][periodo] + EOLExpTotal[cenario][periodo] + FVExpTotal[cenario][periodo]

            maximum = max(Demanda[cenario])
            fig, axs = plt.subplots(2,numperiodo)
            fig.set_size_inches(5*numperiodo, 6)
            for periodo in range(numperiodo):
                axs[0, periodo].set_title('Geração por tecnologia')
                #axs[0, periodo].set_xtickslabels(np.arange(24*periodo-1, 24*periodo + 23, 6))
                axs[0, periodo].set_xticks(np.arange(24*periodo, 24*periodo + 23, 6))
                axs[0, periodo].grid(True, which='both', axis='x', linestyle="--",)
                axs[0, periodo].set_xticklabels(np.arange(0, 23, 6))                       
                axs[0, periodo].step(EixoX_num[cenario], GPCH_exp_total[cenario], color='cyan', label="PCH Exp")
                axs[0, periodo].fill_between(EixoX_num[cenario], GPCH_exp_total[cenario], step="pre", color='cyan')
                axs[0, periodo].step(EixoX_num[cenario], GUTE_exp_total[cenario], color='red', label="GT Exp")
                axs[0, periodo].fill_between(EixoX_num[cenario], GUTE_exp_total[cenario], step="pre", color='red')
                axs[0, periodo].step(EixoX_num[cenario], GUTE_ret_total[cenario], color='#8b0000', label="UTE Retrofit")
                axs[0, periodo].fill_between(EixoX_num[cenario], GUTE_ret_total[cenario], step="pre", color='#8b0000')
                axs[0, periodo].step(EixoX_num[cenario], GUHE_exp_total[cenario], color='blue', label="GH Exp")
                axs[0, periodo].fill_between(EixoX_num[cenario], GUHE_exp_total[cenario], step="pre", color='blue')
                axs[0, periodo].step(EixoX_num[cenario], GOUTRAS_exp_total[cenario], color='orange', label="Outras Exp")
                axs[0, periodo].fill_between(EixoX_num[cenario], GOUTRAS_exp_total[cenario], step="pre", color='orange')
                axs[0, periodo].step(EixoX_num[cenario], GTExist_total[cenario], color='#ffcccb', label="GT exist")
                axs[0, periodo].fill_between(EixoX_num[cenario], GTExist_total[cenario], step="pre", color='#ffcccb')
                axs[0, periodo].step(EixoX_num[cenario], GHExist_total[cenario], color='#ADD8E6', label="GH exist")
                axs[0, periodo].fill_between(EixoX_num[cenario], GHExist_total[cenario], step="pre", color='#ADD8E6')
                axs[0, periodo].step(EixoX_num[cenario], Demanda[cenario], lw=2,color='black', label="Demanda") 
                axs[0, periodo].set(xlabel='Período '+str(periodo)+" (Prob: "+str(dados.ProbPeriodo[periodo]*100)+"%)", ylabel='Geração por categoria (MWméd)')
                axs[0, periodo].legend(bbox_to_anchor=(1.04,0.5), loc="center left")
                axs[0, periodo].set_ylim(0, 1.05*maximum)
                axs[0, periodo].set_xlim(24*periodo, 24*periodo + 23)
                 
                maximum2 = max(max(EOLExpTotalAcum[cenario]), max(FVExpTotalAcum[cenario]), max(OutrasExpTotalAcum[cenario]))
                axs[1, periodo].set_title('Geração "Outras" por fonte')
                axs[1, periodo].set_xticks(np.arange(24*periodo, 24*periodo + 23, 6))
                axs[1, periodo].set_xticklabels(np.arange(0, 23, 6))
                axs[1, periodo].grid(True, which='both', axis='x', linestyle="--",)
                axs[1, periodo].step(EixoX_num[cenario], OutrasExpTotalAcum[cenario], color='orange', label="Outras Exp")
                axs[1, periodo].fill_between(EixoX_num[cenario], OutrasExpTotalAcum[cenario], step="pre", color='orange')                 
                axs[1, periodo].step(EixoX_num[cenario], EOLExpTotalAcum[cenario], color='grey', label="Eólica Exp")
                axs[1, periodo].fill_between(EixoX_num[cenario], EOLExpTotalAcum[cenario], step="pre", color='grey')
                axs[1, periodo].step(EixoX_num[cenario], FVExpTotal[cenario], color='yellow', label="FV Exp")
                axs[1, periodo].fill_between(EixoX_num[cenario], FVExpTotal[cenario], step="pre", color='yellow') 
                axs[1, periodo].set(xlabel='Período '+str(periodo)+" (Prob: "+str(dados.ProbPeriodo[periodo]*100)+"%)", ylabel='Geração por categoria (MWméd)')
                axs[1, periodo].legend(bbox_to_anchor=(1.04,0.5), loc="center left")
                axs[1, periodo].set_ylim(0, 1.05*maximum2)
                axs[1, periodo].set_xlim(24*periodo, 24*periodo + 23) 
                if (periodo == numperiodo - 1):
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    descricao = "Cenario "+str(cenario+1)+"\nProb:"+str(dados.ProbCenario[cenario]*100)+"%\nGSF:"+str(dados.GSF[cenario]*100)+"%"
                    axs[1, periodo].text(1.05, 1.3, descricao, transform=axs[1, periodo].transAxes, fontsize=11,verticalalignment='bottom', bbox=props)

            fig.tight_layout()
            fig.savefig(os.path.join(sys.path[0], "Resultados\\Graficos\\Graph_Geracao_Cenario"+str(cenario)+".png"))

        #Cria Gráfico de distribuição de custos por tecnologia de geração

        VetorCusto = [pyo.value(Modelo.model.CustoGTExist)/1000000, pyo.value(Modelo.model.CustoexpOutras)/1000000, pyo.value(Modelo.model.CustoexpUTEs)/1000000, pyo.value(Modelo.model.CustoexpUTERet)/1000000, pyo.value(Modelo.model.CustoexpUHEs)/1000000, pyo.value(Modelo.model.CustoexpPCHs)/1000000]
        VetorCustoxString = ["","GT Existente", "Outras Expansão", "UTE Expansão", "UTE Retrofit", "UHE Expansão", "PCH Expansão"]
        VetorCustox = range(6)


        fig1, graph = plt.subplots()
        fig1.set_size_inches(10, 5)
        grupo = graph.bar(VetorCustox, VetorCusto, color="blue")
        graph.set_xticklabels(VetorCustoxString)
        graph.set_ylim(0, 1.1*max(VetorCusto))  
        graph.set_title('CAPEX e OPEX por fonte')
        graph.set(xlabel='Tecnologia', ylabel='Custo (10^6 reais)')
        for ponto in grupo:
            if ponto.get_height() != 0:
                altura = ponto.get_height()
                graph.annotate('{}'.format(altura), xy=(ponto.get_x() + ponto.get_width() / 2, altura), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')            
            
        fig1.savefig(os.path.join(sys.path[0], "Resultados\\Graficos\\Graph_Custos.png"))

        #Cria Gráfico de expansão de capacidade por tecnologia de geração
        capacidadeOUTRASexp = sum(pyo.value(Modelo.model.CapacidadeOUTRAS_exp[outras]) for outras in range(G_exp.numOUTRAS))
        capacidadeUTEexp = sum(pyo.value(Modelo.model.CapacidadeUTE_exp[uteexp]) for uteexp in range(G_exp.numUTE))
        capacidadeUTEret = sum(pyo.value(Modelo.model.IntegerUTE_Ret[uteret])*G_exp.UTE_Ret[uteret][0][3] for uteret in range(G_exp.numUTERet))
        capacidadeUHEexp = sum(pyo.value(Modelo.model.binaryUHE_exp[uhes])*G_exp.UHE_exp[uhes][2] for uhes in range (G_exp.numUHE))
        capacidadePCHexp = sum(pyo.value(Modelo.model.IntegerPCH_exp[pchexp])*PCH_exp.PCH_exp[pchexp][5] for pchexp in range(PCH_exp.numPCH))      
        
        VetorCapacidade = [capacidadeOUTRASexp, capacidadeUTEexp, capacidadeUTEret, capacidadeUHEexp, capacidadePCHexp]
        VetorCapacidadexString = ["Outras Expansão", "UTE Expansão", "UTE Retrofit", "UHE Expansão", "PCH Expansão"]
        VetorCapacidadex = range(5)

        fig2, graf2 = plt.subplots()
        fig2.set_size_inches(10, 5)
        grupo2 = graf2.bar(VetorCapacidadex, VetorCapacidade, color="blue")
        graf2.set_xticks(np.arange(0, 5, 1))
        graf2.set_xticklabels(VetorCapacidadexString)
        graf2.set_ylim(0, 1.1*max(VetorCapacidade))  
        graf2.set_title('Expansão de capacidade por tecnologia')
        graf2.set(xlabel='Tecnologia', ylabel='Capacidade (MW)')   


        for ponto in grupo2:
            if ponto.get_height() != 0:
                altura = ponto.get_height()
                graf2.annotate('{}'.format(altura), xy=(ponto.get_x() + ponto.get_width() / 2, altura), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')            
      
        fig2.savefig(os.path.join(sys.path[0], "Resultados\\Graficos\\Graph_Capacidade.png"))

        
        E_Total_GHExist = sum(365*dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*pyo.value(Modelo.model.Total_GHExist[cenario,periodo]) for cenario in range(numcenario) for periodo in range(numperiodo*24))/1000000
        E_Total_GTExist = sum(365*dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*pyo.value(Modelo.model.Total_GTExist[cenario,periodo]) for cenario in range(numcenario) for periodo in range(numperiodo*24))/1000000
        E_Total_GEOL_exp = sum(365*dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*EOLExpTotal[cenario][periodo] for cenario in range(numcenario) for periodo in range(numperiodo*24))/1000000
        E_Total_GFV_exp = sum(365*dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*FVExpTotal[cenario][periodo] for cenario in range(numcenario) for periodo in range(numperiodo*24))/1000000
        E_Total_GOUTRAS_exp = sum(365*dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*OutrasExpTotal[cenario][periodo] for cenario in range(numcenario) for periodo in range(numperiodo*24))/1000000
        E_Total_GUTE_exp = sum(365*dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*pyo.value(Modelo.model.Total_GUTE_exp[cenario,periodo]) for cenario in range(numcenario) for periodo in range(numperiodo*24))/1000000
        E_Total_GUTE_ret = sum(365*dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*pyo.value(Modelo.model.Total_GUTE_Ret[cenario,periodo]) for cenario in range(numcenario) for periodo in range(numperiodo*24))/1000000
        E_Total_GUHE_exp = sum(365*dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*pyo.value(Modelo.model.Total_GUHE_exp[cenario,periodo])for cenario in range(numcenario) for periodo in range(numperiodo*24))/1000000
        E_Total_GPCH_exp = sum(365*dados.ProbCenario[cenario]*dados.ProbPeriodo[math.trunc(periodo/24)]*pyo.value(Modelo.model.Total_GPCH_exp[cenario,periodo]) for cenario in range(numcenario) for periodo in range(numperiodo*24))/1000000

        fig3, graf3 = plt.subplots()
        fig3.set_size_inches(10, 5)
        graf3.bar([0, 1, 2, 3, 4, 5, 6, 7, 8], [E_Total_GHExist, E_Total_GTExist, E_Total_GEOL_exp, E_Total_GFV_exp, E_Total_GOUTRAS_exp, E_Total_GUTE_exp, E_Total_GUTE_ret, E_Total_GUHE_exp, E_Total_GPCH_exp], color=['#ADD8E6', '#ffcccb', 'grey', 'yellow','orange', 'red', '#8b0000', 'blue', 'cyan'])
        graf3.set_xticks(np.arange(0, 8, 1))
        graf3.set_xticklabels(["UHE Exist", "UTE Exist", "EOL Exp", "FV Exp","Outras Exp", "UTE exp", "UTE ret", "UHE exp", "PCH exp"])
        graf3.set_ylim(0, 1.1*max([E_Total_GHExist, E_Total_GTExist, E_Total_GOUTRAS_exp, E_Total_GUTE_exp, E_Total_GUTE_ret, E_Total_GUHE_exp, E_Total_GPCH_exp]))  
        graf3.set_title('Geração Esperada de Energia por fonte')
        graf3.set(xlabel='Tecnologia', ylabel='Geração (TWh)') 
        fig3.savefig(os.path.join(sys.path[0], "Resultados\\Graficos\\Graph_GeracaoEnergia.png")) 