import random


class Ambiente():
    grid = []

    # linha, coluna
    agentPos = [0, 0]
    linhaTamanho = 0
    colunaTamanho = 0

    def __init__(self, linhas, colunas):
        self.linhaTamanho = linhas
        self.colunaTamanho = colunas
        self.grid = [['_' for i in range(colunas)] for j in range(linhas)]
        # cada linha tem varias colunas

    def print_ambiente(self):
        # print('\n'.join(map(str, self.grid)))
        for lin in range(self.linhaTamanho):
            for col in range(self.colunaTamanho):
                print(self.grid[lin][col], end=" ")
            print()

    def add_obstaculo(self, linha, coluna):
        if 0 <= linha < self.linhaTamanho and 0 <= coluna < self.colunaTamanho:
            self.grid[linha][coluna] = '#'

    def add_obstaculo_rand(self, x):
        for i in range(x):
            linha = random.randint(0, self.linhaTamanho - 1)
            coluna = random.randint(0, self.colunaTamanho - 1)
            self.grid[linha][coluna] = '#'

    def atualiza_agente(self, linha, coluna):
        self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
        self.agentPos[0] = linha
        self.agentPos[1] = coluna
        self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'

    def get_ambiente(self):
        return self.grid

    def get_agentPos(self):
        return self.agentPos

    def mover(self, movimento):
        if movimento == 7:
            if 0 <= self.agentPos[0] - 1 < self.linhaTamanho and 0 <= self.agentPos[1] - 1 < self.colunaTamanho:
                if self.grid[self.agentPos[0] - 1][self.agentPos[1] - 1] == '_':
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] -= 1
                    self.agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 8:
            if 0 <= self.agentPos[0] - 1 < self.linhaTamanho and 0 <= self.agentPos[1] < self.colunaTamanho:
                if self.grid[self.agentPos[0] - 1][self.agentPos[1]] == '_':
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] -= 1
                    # agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 9:
            if 0 <= self.agentPos[0] - 1 < self.linhaTamanho and 0 <= self.agentPos[1] + 1 < self.colunaTamanho:
                if self.grid[self.agentPos[0] - 1][self.agentPos[1] + 1] == '_':
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] -= 1
                    self.agentPos[1] += 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 4:
            if 0 <= self.agentPos[0] < self.linhaTamanho and 0 <= self.agentPos[1] - 1 < self.colunaTamanho:
                if self.grid[self.agentPos[0]][self.agentPos[1] - 1] == '_':
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    # self.agentPos[0] -= 1
                    self.agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 6:
            if 0 <= self.agentPos[0] < self.linhaTamanho and 0 <= self.agentPos[1] + 1 < self.colunaTamanho:
                if self.grid[self.agentPos[0]][self.agentPos[1] + 1] == '_':
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    # self.agentPos[0] -= 1
                    self.agentPos[1] += 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 1:
            if 0 <= self.agentPos[0] + 1 < self.linhaTamanho and 0 <= self.agentPos[1] - 1 < self.colunaTamanho:
                if self.grid[self.agentPos[0] + 1][self.agentPos[1] - 1] == '_':
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] += 1
                    self.agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 2:
            if 0 <= self.agentPos[0] + 1 < self.linhaTamanho and 0 <= self.agentPos[1] < self.colunaTamanho:
                if self.grid[self.agentPos[0] + 1][self.agentPos[1]] == '_':
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] += 1
                    # self.agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 3:
            if 0 <= self.agentPos[0] + 1 < self.linhaTamanho and 0 <= self.agentPos[1] + 1 < self.colunaTamanho:
                if self.grid[self.agentPos[0] + 1][self.agentPos[1] + 1] == '_':
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] += 1
                    self.agentPos[1] += 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        else:
            return 0

        return 1
