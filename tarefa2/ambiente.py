from agente_simples import linhatmp


class ambiente():
    grid =[]
    agentPos = [0, 0]
    linhaTamanho = 0
    colunaTamanho = 0


    def __init__(self, linhas, colunas):
        linhaTamanho = linhas
        colunaTamanho = colunas
        grid = [['_' for i in range(colunas)] for j in range(linhas)]

    def print_ambiente(self):
        print('\n'.join(map(str, self.grid)))

    def add_obstaculo(self, linha, coluna):
        if 0 <= linha < linhaTamanho and 0 <= coluna < colunaTamanho:
            grid[linhatmp][colunatmp] = '#'


