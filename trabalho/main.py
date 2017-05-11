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

    linha = 9
    coluna = 9

    amb = ambiente.Ambiente(linha, coluna)

    # criando paredes como no pdf
    paredes = [[0, 0], [0, 1], [0, 4], [0, 5], [0, 6], [0, 7],
               [1, 0],
               [2, 3], [2, 4], [2, 5],
               [3, 3], [3, 4], [3, 5], [3, 6],
               [5, 2], [5, 5], [5, 7],
               [6, 1], [6, 4], [6, 5], [6, 7],
               [7, 1], [7, 4], [7, 7],
               [8, 1], [8, 2],
               ]

    for i in range(len(paredes)):
        amb.add_obstaculo(paredes[i][0], paredes[i][1])

    frutas = amb.colocar_frutas()
    pos_inicial = [8, 0]
    pos_objetivo = [2, 6]
    agt = agente.Agente(pos_inicial, amb.get_ambiente(), amb.andavel, amb.parede, frutas)
    agt.set_objetivo(pos_objetivo)
    amb.set_agente(agt.minhaPosicao)

#    print("Executando LRTA*")

    vezes = 0
    fim = ""
    while(fim == ""):
        agt.atualiza_posicao(pos_inicial)
        amb.atualiza_agente(agt.minhaPosicao)
        amb.reseta_chao()
        amb.reset_frutas()
        agt.reinicializar()

        agt.set_objetivo(pos_objetivo)

#        print("ambiente no inicio: ")
#        amb.print_ambiente()
#        print("posicao do agente" + str(agt.get_posicao()))
#        print("objetivo: " + str(agt.objetivo))

        print("executando LRTA* ... \n")
        if vezes == 0:
            agt.set_comandos(agt.busca_lrta(inicializar_h=True))
        else:
            agt.set_comandos(agt.busca_lrta())

#        print("\nnumero de espacos vazios: " + str(linha * coluna - len(paredes)))
        print("solucao: " + str(agt.comandos))

#        print("ambiente no fim: ")
        amb.print_ambiente()
#        print(amb.get_agentpos())
#        print(agt.get_posicao())
        vezes += 1

        fim = input("fim da execução, enter para re-executar: ")


if __name__ == "__main__":
    # execute only if run from here
    main()
