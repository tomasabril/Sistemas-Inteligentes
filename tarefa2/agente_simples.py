# Toms Abril


# funções -------------------------------------
def print_grid():
    print('\n'.join(map(str, grid)))


# criando ambiente  ----------------------------
while 1:
    try:
        linha = int(input("quantas linhas: "))
        coluna = int(input("quantas colunas: "))
        break
    except ValueError:
        print("Não é um numero!")

agentPos = [0, 0]
grid = [['_' for i in range(coluna)] for j in range(linha)]

print_grid()
while 1:
    try:
        print("posicao do obstaculo a adicionar")
        linhatmp = int(input("linha: "))
        colunatmp = int(input("coluna:"))
        if 0 <= linhatmp < linha and 0 <= colunatmp < coluna:
            grid[linhatmp][colunatmp] = '#'
    except ValueError:
        print("Não é um numero!")
    print_grid()
    try:
        if int(input("1 para sair da insercao de paredes ")) == 1:
            break
    except ValueError:
        pass

print("posição inicial do agente")
while 1:
    try:
        agentPos = [int(input("linha: ")), int(input("coluna:"))]
        break
    except ValueError:
        print("Não é um numero!")
grid[agentPos[0]][agentPos[1]] = 'A'
print_grid()

# movimentação do agente  ----------------------------

while 1:
    print("utilize o teclado numerico para movimentar. \n5 le a posição atual.\n0 sai.")
    try:
        movimento = int(input())
    except ValueError:
        print("Não é um numero!")
        movimento = 5
    if movimento == 0:
        break
    elif movimento == 5:
        print("Posição atual: " + str(agentPos))
    elif movimento == 7:
        if 0 <= agentPos[0] - 1 < linha and 0 <= agentPos[1] - 1 < coluna:
            if grid[agentPos[0] - 1][agentPos[1] - 1] == '_':
                grid[agentPos[0]][agentPos[1]] = '_'
                agentPos[0] -= 1
                agentPos[1] -= 1
                grid[agentPos[0]][agentPos[1]] = 'A'
    elif movimento == 8:
        if 0 <= agentPos[0] - 1 < linha and 0 <= agentPos[1] < coluna:
            if grid[agentPos[0] - 1][agentPos[1]] == '_':
                grid[agentPos[0]][agentPos[1]] = '_'
                agentPos[0] -= 1
                # agentPos[1] -= 1
                grid[agentPos[0]][agentPos[1]] = 'A'
    elif movimento == 9:
        if 0 <= agentPos[0] - 1 < linha and 0 <= agentPos[1] + 1 < coluna:
            if grid[agentPos[0] - 1][agentPos[1] + 1] == '_':
                grid[agentPos[0]][agentPos[1]] = '_'
                agentPos[0] -= 1
                agentPos[1] += 1
                grid[agentPos[0]][agentPos[1]] = 'A'
    elif movimento == 4:
        if 0 <= agentPos[0] < linha and 0 <= agentPos[1] - 1 < coluna:
            if grid[agentPos[0]][agentPos[1] - 1] == '_':
                grid[agentPos[0]][agentPos[1]] = '_'
                # agentPos[0] -= 1
                agentPos[1] -= 1
                grid[agentPos[0]][agentPos[1]] = 'A'
    elif movimento == 6:
        if 0 <= agentPos[0] < linha and 0 <= agentPos[1] + 1 < coluna:
            if grid[agentPos[0]][agentPos[1] + 1] == '_':
                grid[agentPos[0]][agentPos[1]] = '_'
                # agentPos[0] -= 1
                agentPos[1] += 1
                grid[agentPos[0]][agentPos[1]] = 'A'
    elif movimento == 1:
        if 0 <= agentPos[0] + 1 < linha and 0 <= agentPos[1] - 1 < coluna:
            if grid[agentPos[0] + 1][agentPos[1] - 1] == '_':
                grid[agentPos[0]][agentPos[1]] = '_'
                agentPos[0] += 1
                agentPos[1] -= 1
                grid[agentPos[0]][agentPos[1]] = 'A'
    elif movimento == 2:
        if 0 <= agentPos[0] + 1 < linha and 0 <= agentPos[1] < coluna:
            if grid[agentPos[0] + 1][agentPos[1]] == '_':
                grid[agentPos[0]][agentPos[1]] = '_'
                agentPos[0] += 1
                # agentPos[1] -= 1
                grid[agentPos[0]][agentPos[1]] = 'A'
    elif movimento == 3:
        if 0 <= agentPos[0] + 1 < linha and 0 <= agentPos[1] + 1 < coluna:
            if grid[agentPos[0] + 1][agentPos[1] + 1] == '_':
                grid[agentPos[0]][agentPos[1]] = '_'
                agentPos[0] += 1
                agentPos[1] += 1
                grid[agentPos[0]][agentPos[1]] = 'A'

    print_grid()
