# Tomás Abril
# Allan Patrick


import time
import ambiente
import agente
import arvore


def main():

    linha = 9
    coluna = 9

    amb = ambiente.Ambiente(linha, coluna)

    # criando paredes como no pdf
    paredes = [[1, 0], [0, 0],
               [8, 1], [7, 1], [6, 1], [5, 1], [0, 1],
               [8, 2], [5, 2],
               [2, 3], [3, 3],
               [7, 4], [6, 4], [3, 4], [2, 4], [0, 4],
               [6, 5], [5, 5], [3, 5], [2, 5], [0, 5],
               [0, 6],
               [7, 7], [6, 7], [5, 7], [3, 7], [1, 7], [0, 7]]

    for i in range(len(paredes)):
        amb.add_obstaculo(paredes[i][0], paredes[i][1])

    agt = agente.Agente([8, 0], amb.get_ambiente())
    amb.set_agente(agt.minhaPosicao)
    print("ambiente no inicio: ")
    amb.print_ambiente()
    print("posicao do agente" + str(agt.get_posicao()))
    agt.set_objetivo([2, 8])
    print("objetivo: " + str(agt.objetivo))

    if int(input("1 para A* \n0 para busca de custo uniforme: ")) == 1:
        print("executando A*")
        agt.set_comandos(agt.a_estrela())
    else:
        print("executando custo uniforme \n")
        agt.set_comandos(agt.busca_custo_uniforme())

    print("\nnumero de espacos vazios: " + str(linha * coluna - len(paredes)))
    print("solucao: " + str(agt.comandos))

    agt.executa_cmds()

    print("ambiente no fim: ")
    amb.print_ambiente()

    print(amb.get_agentpos())
    print(agt.get_posicao())


if __name__ == "__main__":
    # execute only if run from here
    main()
