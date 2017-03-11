### Tomás Abril

def printGrid():
    print('\n'.join(map(str, grid)))


linha = int(input("quantas linhas: "))
coluna = int(input("quantas colunas: "))

agentPos = [0, 0]
grid = [['_' for i in range(coluna)] for j in range(linha)]

printGrid()
while (1):
    print("posicao do obstaculo a adicionar")
    grid[int(input("linha: "))][int(input("coluna:"))] = '#'
    printGrid()
    if int(input("1 para sair da insercao de paredes ")) == 1:
        break

print("posição inicial do agente")
agentPos = [int(input("linha: ")), int(input("coluna:"))]
grid[agentPos[0]][agentPos[1]] = 'A'
printGrid()

