class Agente():
    representacao_ambiente = []
    minhaPosicao = [0, 0]

    def __init__(self, linha, coluna, ambiente):
        self.representacao_ambiente = ambiente

    def lerPosicao(self, posicao_real):
        print (posicao_real)
        self.minhaPosicao = posicao_real

    def mover(self, direcao):
        if movimento == 7:
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] -= 1
                    self.agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 8:
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] -= 1
                    # agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 9:
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] -= 1
                    self.agentPos[1] += 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 4:
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    # self.agentPos[0] -= 1
                    self.agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 6:
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    # self.agentPos[0] -= 1
                    self.agentPos[1] += 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 1:
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] += 1
                    self.agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 2:
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] += 1
                    # self.agentPos[1] -= 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
        elif movimento == 3:
                    self.grid[self.agentPos[0]][self.agentPos[1]] = '_'
                    self.agentPos[0] += 1
                    self.agentPos[1] += 1
                    self.grid[self.agentPos[0]][self.agentPos[1]] = 'A'
