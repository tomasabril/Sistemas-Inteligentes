# Tomás Abril


import time
import ambiente
import agente


def main():
    print("Criando ambiente")
    # while 1:
    #     try:
    #         linha = int(input("quantas linhas: "))
    #         coluna = int(input("quantas colunas: "))
    #         x = int(input("quantas paredes? "))
    #         break
    #     except ValueError:
    #         print("Não é um numero!")
    linha = 9
    coluna = 9

    amb = ambiente.Ambiente(linha, coluna)
    # amb.add_obstaculo_rand(x)

    # criando paredes como no pdf
    paredes = [[1, 0], [0, 0], [8, 1], [7, 1], [6, 1], [5, 1], [0, 1], [8, 2], [6, 2], [2, 3], [3, 3], [7, 4], [6, 4],
               [3, 4], [2, 4], [0, 4]]
    for i in range(len(paredes)):
        amb.add_obstaculo(paredes[i][0], paredes[i][1])

    amb.print_ambiente()
    print("---")

    # while 1:
    #     try:
    #         print("Posição inicial do agente:")
    #         linha = int(input("linha: "))
    #         coluna = int(input("coluna: "))
    #         break
    #     except ValueError:
    #         print("Não é um numero!")
    linha = 8
    coluna = 0

    agt = agente.Agente(linha, coluna, amb.get_ambiente())
    amb.atualiza_agente(linha, coluna)
    amb.print_ambiente()
    agt.ler_posicao(amb.get_agentPos())
    agt.set_objetivo(7, 2)
    agt.set_comandos([8, 8, 8, 9, 6, 6, 3, 2, 1])

    for i in range(len(agt.comandos)):
        comando = agt.comandos.pop(0)
        if amb.mover(comando):
            print()
            amb.print_ambiente()
            agt.mover(comando)
            print()
            amb.print_ambiente()


if __name__ == "__main__":
    # execute only if run as a script
    main()
