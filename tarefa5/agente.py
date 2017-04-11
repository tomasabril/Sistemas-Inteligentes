# -----
#
# Tomás Abril
# Allan Patrick

import math
import arvore
import random

class Agente():
   # representação do ambiente
    repr_amb = []
    linhaTamanho = 0
    colunaTamanho = 0
    minhaPosicao = []
    objetivo = []
    # para executar
    comandos = []
    # estimativa h { (linha, coluna): estimativa }
    est_h = {}


    def __init__(self, agentepos, ambiente, andavel, parede):
        self.repr_amb = ambiente
        self.minhaPosicao = agentepos
        self.linhaTamanho = len(ambiente)
        self.colunaTamanho = len(ambiente[0])
        self.andavel = andavel
        self.parede = parede

    def set_comandos(self, lista):
        self.comandos = lista[:]

    def executa_cmds(self):
        while self.comandos:
            comando = self.comandos.pop(0)
#            print("ação a ser executada: " + str(comando))
            if comando in self.acoes_possiveis():
                self.mover(comando)
            else:
                print("Ação " + str(comando) + " não pode ser executada")

    def executa_um_cmd(self):
        comando = self.comandos.pop(0)
#            print("ação a ser executada: " + str(comando))
        if comando in self.acoes_possiveis():
            self.mover(comando)
        else:
            print("Ação " + str(comando) + " não pode ser executada")

    def set_objetivo(self, obj):
        self.objetivo = obj
        self.repr_amb[obj[0]][obj[1]] = 'o'

    def get_posicao(self):
        return self.minhaPosicao

    def busca_dfs(self):
        solucao = []
        acoes = [8, 9, 6, 3, 2, 1, 4, 7]
        custo = 0
        custo1 = (8, 4, 6, 2)
        custo15 = (7, 9, 1, 3)
        # { (linha, coluna) : [coisas, daquela, posicao] }
        result = {}
        untried = {}
        unbacktracked = {}

        a_pos = tuple(self.minhaPosicao)

        while self.minhaPosicao != self.objetivo:
            if a_pos not in untried:
                untried[a_pos] = acoes[:]
                result[a_pos] = [0 for i in range(10)]
                unbacktracked[a_pos] = []
            if untried[a_pos]:
                acao = untried[a_pos].pop(0)
            else:
                if not unbacktracked[a_pos]:
                    print ("Sem acoes para fazer")
                    break
                else:
                    print("Backtracking !")
                    acao = unbacktracked[a_pos].pop(0)
            if acao in self.acoes_possiveis():
                pos_anterior = tuple(self.minhaPosicao)
                self.mover(acao)
                a_pos = tuple(self.minhaPosicao)
                if a_pos not in unbacktracked:
                    unbacktracked[a_pos] = []
                unbacktracked[a_pos].insert(0, pos_anterior)
                if pos_anterior not in result:
                    result[pos_anterior] = ()
                result[pos_anterior][acao] = a_pos
                print("untried: " + str(untried[pos_anterior]))
            else:
                result[a_pos][acao] = a_pos
                print("untried: " + str(untried[a_pos]))
            solucao.append(acao)
            custo += 1 if acao in custo1 else 1.5
            print("acao: " + str(acao))
            self.print_repr()
            input()

        print("Custo: " + str(custo))
        print("função result: ")
        print(result)
        return solucao

    def busca_lrta(self, inicializar_h = False):
        solucao = []
        custo = 0
        custo1 = (8, 4, 6, 2)
        custo15 = (7, 9, 1, 3)
        # proximo = [movimento, [pos], custo + estimativa]
        proximo = []
        # h { (linha, coluna) : estimativa }
        if inicializar_h:
            for lin in range(self.linhaTamanho):
                for col in range(self.colunaTamanho):
                    # euristica euclidiana
                    self.est_h[tuple([lin, col])] = math.sqrt(abs(lin - self.objetivo[0])**2 + abs(col- self.objetivo[1])**2)
        while self.minhaPosicao != self.objetivo:
            proximo.clear()
            for acao in self.acoes_com_result(self.minhaPosicao):
                pos_resultante = (acao[1][0], acao[1][1])
                proximo.append([ acao[0], acao[1], acao[2] + self.est_h[pos_resultante] ])
            random.shuffle(proximo)
            proximo.sort(key=lambda prox: prox[2])
            # atualizando estimativas
            if self.est_h[tuple(self.minhaPosicao)] < proximo[0][2]:
                self.est_h[tuple(self.minhaPosicao)] = proximo[0][2]
            movimento = proximo[0][0]
            self.mover(movimento)

            solucao.append(movimento)
            custo += 1 if movimento in custo1 else 1.5
            print("acao: " + str(proximo[0]))
            self.print_repr()
            input()

        print("Estimativas: " + str(self.est_h))
        print("Custo: " + str(custo))
        return solucao

    def acoes_possiveis(self):
        acoes = []
        if 0 <= self.minhaPosicao[0] - 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] - 1][self.minhaPosicao[1] - 1] in self.andavel:
                acoes.append(7)
        if 0 <= self.minhaPosicao[0] - 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] - 1][self.minhaPosicao[1]] in self.andavel:
                acoes.append(8)
        if 0 <= self.minhaPosicao[0] - 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] - 1][self.minhaPosicao[1] + 1] in self.andavel:
                acoes.append(9)
        if 0 <= self.minhaPosicao[0] < self.linhaTamanho and 0 <= self.minhaPosicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1] - 1] in self.andavel:
                acoes.append(4)
        if 0 <= self.minhaPosicao[0] < self.linhaTamanho and 0 <= self.minhaPosicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1] + 1] in self.andavel:
                acoes.append(6)
        if 0 <= self.minhaPosicao[0] + 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] + 1][self.minhaPosicao[1] - 1] in self.andavel:
                acoes.append(1)
        if 0 <= self.minhaPosicao[0] + 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] + 1][self.minhaPosicao[1]] in self.andavel:
                acoes.append(2)
        if 0 <= self.minhaPosicao[0] + 1 < self.linhaTamanho and 0 <= self.minhaPosicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[self.minhaPosicao[0] + 1][self.minhaPosicao[1] + 1] in self.andavel:
                acoes.append(3)
        return acoes

    def acoes_com_result(self, posicao):
        # retorna [ movimento, [linha, coluna], custo ]
        acoes = []
        if 0 <= posicao[0] - 1 < self.linhaTamanho and 0 <= posicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0] - 1][posicao[1] - 1] in self.andavel:
                acoes.append([7, [posicao[0] - 1, posicao[1] - 1], 1.5])
        if 0 <= posicao[0] - 1 < self.linhaTamanho and 0 <= posicao[1] < self.colunaTamanho:
            if self.repr_amb[posicao[0] - 1][posicao[1]] in self.andavel:
                acoes.append([8, [posicao[0] - 1, posicao[1]], 1])
        if 0 <= posicao[0] - 1 < self.linhaTamanho and 0 <= posicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0] - 1][posicao[1] + 1] in self.andavel:
                acoes.append([9, [posicao[0] - 1, posicao[1] + 1], 1.5])
        if 0 <= posicao[0] < self.linhaTamanho and 0 <= posicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0]][posicao[1] - 1] in self.andavel:
                acoes.append([4, [posicao[0], posicao[1] - 1], 1])
        if 0 <= posicao[0] < self.linhaTamanho and 0 <= posicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0]][posicao[1] + 1] in self.andavel:
                acoes.append([6, [posicao[0], posicao[1] + 1], 1])
        if 0 <= posicao[0] + 1 < self.linhaTamanho and 0 <= posicao[1] - 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0] + 1][posicao[1] - 1] in self.andavel:
                acoes.append([1, [posicao[0] + 1, posicao[1] - 1], 1.5])
        if 0 <= posicao[0] + 1 < self.linhaTamanho and 0 <= posicao[1] < self.colunaTamanho:
            if self.repr_amb[posicao[0] + 1][posicao[1]] in self.andavel:
                acoes.append([2, [posicao[0] + 1, posicao[1]], 1])
        if 0 <= posicao[0] + 1 < self.linhaTamanho and 0 <= posicao[1] + 1 < self.colunaTamanho:
            if self.repr_amb[posicao[0] + 1][posicao[1] + 1] in self.andavel:
                acoes.append([3, [posicao[0] + 1, posicao[1] + 1], 1.5])
        return acoes

    def mover(self, movimento):
        if movimento == 7:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '+'
            self.minhaPosicao[0] -= 1
            self.minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 8:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '+'
            self.minhaPosicao[0] -= 1
            # minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 9:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '+'
            self.minhaPosicao[0] -= 1
            self.minhaPosicao[1] += 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 4:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '+'
            # self.minhaPosicao[0] -= 1
            self.minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 6:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '+'
            # self.minhaPosicao[0] -= 1
            self.minhaPosicao[1] += 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 1:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '+'
            self.minhaPosicao[0] += 1
            self.minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 2:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '+'
            self.minhaPosicao[0] += 1
            # self.minhaPosicao[1] -= 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'
        elif movimento == 3:
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = '+'
            self.minhaPosicao[0] += 1
            self.minhaPosicao[1] += 1
            self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'A'

    def print_repr(self):
        # print('\n'.join(map(str, self.grid)))
        print("  ", end='')
        for i in range(self.linhaTamanho):
            print(str(i) + " ", end='')
        print()
        for lin in range(self.linhaTamanho):
            print(str(lin) + " ", end='')
            for col in range(self.colunaTamanho):
                print(self.repr_amb[lin][col], end=" ")
            print()
