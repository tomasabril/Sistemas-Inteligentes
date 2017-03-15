# Tomás Abril

import ambiente
import agente


def main():
    print("Criando ambiente")
    while 1:
        try:
            linha = int(input("quantas linhas: "))
            coluna = int(input("quantas colunas: "))
            break
        except ValueError:
            print("Não é um numero!")
    amb = ambiente.Ambiente(linha, coluna)

    while 1:
        pass


if __name__ == "__main__":
    # execute only if run as a script
    main()


