# Tomás Abril


import time
import ambiente
import agente


def main():
    print("Criando ambiente")
    while 1:
        try:
            linha = int(input("quantas linhas: "))
            coluna = int(input("quantas colunas: "))
            x = int(input("quantas paredes? "))
            break
        except ValueError:
            print("Não é um numero!")

    amb = ambiente.Ambiente(linha, coluna)
    amb.add_obstaculo_rand(x)
    amb.print_ambiente()

    while 1:
        try:
            print("Posição inicial do agente:")
            linha = int(input("linha: "))
            coluna = int(input("coluna: "))
            break
        except ValueError:
            print("Não é um numero!")

    agt = agente.Agente(linha, coluna, amb.get_ambiente())
    amb.atualiza_agente(linha, coluna)
    amb.print_ambiente()
    agt.ler_posicao(amb.get_agentPos())

    # executa do ultimo ao primeiro, é uma pilha
    comandos = [2, 6, 6, 7, 2, 9]
    while comandos:
        comando = comandos.pop()
        if amb.mover(comando):
            agt.mover(comando)
            print()
            time.sleep(1)
            amb.print_ambiente()


if __name__ == "__main__":
    # execute only if run as a script
    main()
