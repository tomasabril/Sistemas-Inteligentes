# Tomás Abril


import time
import ambiente
import agente
import arvore


def main():
    print("Criando ambiente")

    linha = 9
    coluna = 9

    amb = ambiente.Ambiente(linha, coluna)

    # criando paredes como no pdf
    paredes = [[1, 0], [0, 0], [8, 1], [7, 1], [6, 1], [5, 1], [0, 1], [8, 2], [6, 2], [2, 3], [3, 3], [7, 4], [6, 4],
               [3, 4], [2, 4], [0, 4], [6, 5], [5, 5], [3, 5], [2, 5], [1, 5], [0, 5], [5, 6], [3, 6], [0, 6], [7, 7],
               [6, 7], [5, 7], [4, 7], [3, 7], [2, 7], [1, 7], [0, 7]]
    for i in range(len(paredes)):
        amb.add_obstaculo(paredes[i][0], paredes[i][1])

    amb.print_ambiente()
    print()

    agt = agente.Agente([8, 0], amb.get_ambiente())
    amb.set_agente(agt.minhaPosicao)
    print("ambiente no inicio: ")
    amb.print_ambiente()
    print(agt.get_posicao())
    agt.set_objetivo([7, 2])
    # agt.set_objetivo([0, 8])
    # agt.set_comandos([8, 8, 8, 9, 6, 6, 2, 2, 1])
    print("objetivo: " + str(agt.objetivo))
    agt.set_comandos(agt.busca_largura())
    print("numero de espacos vazios: " + str(linha * coluna - len(paredes)))
    print("solucao: " + str(agt.comandos))

    agt.executa_cmds()

    print("ambiente no fim: ")
    amb.print_ambiente()

    print(amb.get_agentpos())
    print(agt.get_posicao())


if __name__ == "__main__":
    # execute only if run from here
    main()
