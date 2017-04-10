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
    paredes = [[2, 1],
               [1, 2], [3, 2]]

    for i in range(len(paredes)):
        amb.add_obstaculo(paredes[i][0], paredes[i][1])

    agt = agente.Agente([2, 0], amb.get_ambiente(), amb.andavel, amb.parede)
    amb.set_agente(agt.minhaPosicao)
    agt.set_objetivo([2, 2])

    print("ambiente no inicio: ")
    amb.print_ambiente()
    print("posicao do agente" + str(agt.get_posicao()))
    print("objetivo: " + str(agt.objetivo))

    if int(input("1 para DFS \n0 para LRTA*: ")) == 1:
        print("executando DFS ...")
        agt.set_comandos(agt.busca_dfs())
    else:
        print("executando LRTA* ... \n")
        agt.set_comandos(agt.busca_lrta())

    print("\nnumero de espacos vazios: " + str(linha * coluna - len(paredes)))
    print("solucao: " + str(agt.comandos))

#    agt.executa_cmds()

    print("ambiente no fim: ")
    amb.print_ambiente()

    print(amb.get_agentpos())
    print(agt.get_posicao())


if __name__ == "__main__":
    # execute only if run from here
    main()
