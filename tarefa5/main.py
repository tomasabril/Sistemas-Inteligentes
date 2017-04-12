#!/usr/bin/env python3

# ----------------
# Tomás Abril
# Allan Patrick
# ----------------

import time
import ambiente
import agente
import arvore


def main():

    linha = 5
    coluna = 5

    amb = ambiente.Ambiente(linha, coluna)

    # criando paredes como no pdf
    paredes = [[2, 1], [1, 1], [3, 1],
                        [1, 2], [3, 2], [1, 3]
                        ]

    for i in range(len(paredes)):
        amb.add_obstaculo(paredes[i][0], paredes[i][1])

    pos_inicial = [2, 0]
    pos_objetivo = [2, 2]
    agt = agente.Agente(pos_inicial, amb.get_ambiente(), amb.andavel, amb.parede)
    agt.set_objetivo(pos_objetivo)
    amb.set_agente(agt.minhaPosicao)

    qual = int(input("1 para DFS \n0 para LRTA*: "))

    vezes = 0
    fim = ""
    while(fim == ""):
        agt.atualiza_posicao(pos_inicial)
        amb.atualiza_agente(agt.minhaPosicao)
        amb.reseta_chao()
        
        agt.set_objetivo(pos_objetivo)

        print("ambiente no inicio: ")
        amb.print_ambiente()
        print("posicao do agente" + str(agt.get_posicao()))
        print("objetivo: " + str(agt.objetivo))

        if qual == 1:
            print("executando DFS ...")
            agt.set_comandos(agt.busca_dfs())
        else:
            print("executando LRTA* ... \n")
            if vezes == 0:
                agt.set_comandos(agt.busca_lrta(inicializar_h=True))
            else:
                agt.set_comandos(agt.busca_lrta())

        print("\nnumero de espacos vazios: " + str(linha * coluna - len(paredes)))
        print("solucao: " + str(agt.comandos))
#       agt.executa_cmds()
        print("ambiente no fim: ")
        amb.print_ambiente()
        print(amb.get_agentpos())
        print(agt.get_posicao())
        vezes += 1

        fim = input("fim da execução, enter para re-executar: ")


if __name__ == "__main__":
    # execute only if run from here
    main()

