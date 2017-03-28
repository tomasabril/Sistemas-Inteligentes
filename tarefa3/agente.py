# -----
#
# Tomás Abril
# Allan Patrick

import arvore


class Agente():
    # representação do ambiente
    repr_amb = []
    linhaTamanho = 0
    colunaTamanho = 0
    minhaPosicao = []
    objetivo = []
    comandos = []

    def __init__(self, agentepos, ambiente):
        self.repr_amb = ambiente
        self.minhaPosicao = agentepos
        self.linhaTamanho = len(ambiente)
        self.colunaTamanho = len(ambiente[0])

    def set_comandos(self, lista):
        self.comandos = lista

    def executa_cmds(self):
        while self.comandos:
            comando = self.comandos.pop(0)
            print("ação a ser executada: " + str(comando))
            if comando in self.acoes_possiveis():
                self.mover(comando)
            else:
                print("Ação " + str(comando) + " não pode ser executada")

    def set_objetivo(self, obj):
        self.objetivo = obj

    def get_posicao(self):
        return self.minhaPosicao

    def busca_largura(self):
        solucao = []
        arv = arvore.Arvore()
        no = arvore.No([], [], self.minhaPosicao[:], [])
        arv.inserir_nos(no)
        arv.inserir_fronteira(no)
        while (arv.fronteira):
            no = arv.fronteira.pop(0)
            possib = self.acoes_com_result(no.pos)
            for acao in possib:
                no_tmp = arvore.No(no, [], acao[1], acao[0])
                if no_tmp.pos not in arv.visitados and no_tmp.pos not in [x.pos for x in arv.fronteira]:
                    arv.inserir_nos(no_tmp)
                    arv.inserir_fronteira(no_tmp)
                    arv.visitados.append(no.pos)
                    if no_tmp.pos == self.objetivo:
                        # go for solution
                        while no_tmp.pai:
                            solucao.append(no_tmp.acao)
                            no_tmp = no_tmp.pai
                        solucao.reverse()
                        break
            else:
                #arv.visitados.append(no)
                continue
            break
        print("quantidade de nós na arvore: " + str(len(arv.nos)))
        print("nós explorados: " + str(len(arv.visitados)))
        print(arv.visitados)
        return solucao

    def acoes_possiveis(self):
        acoes = []
        if 0 <= self.minhaPosicao[0] - 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] - 1][self.minhaPosicao[1] - 1] == '_':
                acoes.append(7)
        if 0 <= self.minhaPosicao[0] - 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] - 1][self.minhaPosicao[1]] == '_':
                acoes.append(8)
        if 0 <= self.minhaPosicao[0] - 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] - 1][self.minhaPosicao[1] + 1] == '_':
                acoes.append(9)
        if 0 <= self.minhaPosicao[0] < self.linhaTamanho and 0 <= self.minhaPosicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1] - 1] == '_':
                acoes.append(4)
        if 0 <= self.minhaPosicao[0] < self.linhaTamanho and 0 <= self.minhaPosicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1] + 1] == '_':
                acoes.append(6)
        if 0 <= self.minhaPosicao[0] + 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] + 1][self.minhaPosicao[1] - 1] == '_':
                acoes.append(1)
        if 0 <= self.minhaPosicao[0] + 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] + 1][self.minhaPosicao[1]] == '_':
                acoes.append(2)
        if 0 <= self.minhaPosicao[0] + 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] + 1][self.minhaPosicao[1] + 1] == '_':
                acoes.append(3)
        return acoes

    def acoes_com_result(self, posicao):
        # retorna [ movimento, [linha, coluna] ]
        acoes = []
        if 0 <= posicao[0] - 1 < self.linhaTamanho and 0 <= posicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0] - 1][posicao[1] - 1] == '_':
                acoes.append([7, [posicao[0] - 1, posicao[1] - 1]])
        if 0 <= posicao[0] - 1 < self.linhaTamanho and 0 <= posicao[1] < self.colunaTamanho:
            if self.repr_amb[posicao[0] - 1][posicao[1]] == '_':
                acoes.append([8, [posicao[0] - 1, posicao[1]]])
        if 0 <= posicao[0] - 1 < self.linhaTamanho and 0 <= posicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0] - 1][posicao[1] + 1] == '_':
                acoes.append([9, [posicao[0] - 1, posicao[1] + 1]])
        if 0 <= posicao[0] < self.linhaTamanho and 0 <= posicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0]][posicao[1] - 1] == '_':
                acoes.append([4, [posicao[0], posicao[1] - 1]])
        if 0 <= posicao[0] < self.linhaTamanho and 0 <= posicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0]][posicao[1] + 1] == '_':
                acoes.append([6, [posicao[0], posicao[1] + 1]])
        if 0 <= posicao[0] + 1 < self.linhaTamanho and 0 <= posicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0] + 1][posicao[1] - 1] == '_':
                acoes.append([1, [posicao[0] + 1, posicao[1] - 1]])
        if 0 <= posicao[0] + 1 < self.linhaTamanho and 0 <= posicao[1] < self.colunaTamanho:
            if self.repr_amb[posicao[0] + 1][posicao[1]] == '_':
                acoes.append([2, [posicao[0] + 1, posicao[1]]])
        if 0 <= posicao[0] + 1 < self.linhaTamanho and 0 <= posicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0] + 1][posicao[1] + 1] == '_':
                acoes.append([3, [posicao[0] + 1, posicao[1] + 1]])
        return acoes

    def mover(self, movimento):
        if movimento == 7:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '_'
            self.minhaPosicao[0] -= 1
            self.minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 8:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '_'
            self.minhaPosicao[0] -= 1
            # minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 9:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '_'
            self.minhaPosicao[0] -= 1
            self.minhaPosicao[1] += 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 4:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '_'
            # self.minhaPosicao[0] -= 1
            self.minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 6:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '_'
            # self.minhaPosicao[0] -= 1
            self.minhaPosicao[1] += 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 1:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '_'
            self.minhaPosicao[0] += 1
            self.minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 2:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '_'
            self.minhaPosicao[0] += 1
            # self.minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 3:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '_'
            self.minhaPosicao[0] += 1
            self.minhaPosicao[1] += 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
