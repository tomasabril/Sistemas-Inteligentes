# -----
#
# Tomás Abril
# Allan Patrick

import math
import arvore


class Agente():
    # representação do ambiente
    repr_amb = []
    linhaTamanho = 0
    colunaTamanho = 0
    minhaPosicao = []
    objetivo = []
    comandos = []


    def __init__(self, agentepos, ambiente, andavel, parede):
        self.repr_amb = ambiente
        self.minhaPosicao = agentepos
        self.linhaTamanho = len(ambiente)
        self.colunaTamanho = len(ambiente[0])
        self.andavel = andavel
        self.parede = parede

    def set_comandos(self, lista):
        self.comandos = lista

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

    def a_estrela(self):
        solucao = []
        arv = arvore.Arvore()
        no = arvore.No([], [], self.minhaPosicao[:], [], 0)
        arv.inserir_nos(no)
        arv.inserir_fronteira(no)
        while (arv.fronteira):
            arv.reordenar_fronteira_f()
            no = arv.fronteira.pop(0)
            arv.visitados.append(no.pos)
            self.repr_amb[no.pos[0]][no.pos[1]] = '◫'
            if no.pos == self.objetivo:
                print("custo: " + str(no.custo))
                # go for solution
                while no.pai:
                    solucao.append(no.acao)
                    no = no.pai
                solucao.reverse()
                break
            possib = self.acoes_com_result(no.pos)
            for acao in possib:
                # estimativa pitagorica 
                estimativa = math.sqrt(abs(acao[1][0] - self.objetivo[0])**2 + abs(acao[1][1] - self.objetivo[1])**2)
                # estimativa manhatan
                #estimativa = abs(acao[1][0] - self.objetivo[0])+ abs(acao[1][1] - self.objetivo[1])
                no_tmp = arvore.No(no, [], acao[1], acao[0],
                                   no.custo + acao[2], h=estimativa)
                flag = False
                if no_tmp.pos not in arv.visitados:
                    for i in arv.fronteira:
                        if no_tmp.pos == i.pos:
                            if no_tmp.f > i.f:
                                flag = True
                    if flag == False:
                        arv.inserir_nos(no_tmp)
                        arv.inserir_fronteira(no_tmp)
                        self.repr_amb[no_tmp.pos[0]][no_tmp.pos[1]] = '□'

            else:
                continue
            break
        print("quantidade de nós na arvore: " + str(len(arv.nos)))
        print("nós explorados: " + str(len(arv.visitados)))
#        print(arv.visitados)
        return solucao
    
    def busca_custo_uniforme(self):
        solucao = []
        arv = arvore.Arvore()
        no = arvore.No([], [], self.minhaPosicao[:], [], 0)
        arv.inserir_nos(no)
        arv.inserir_fronteira(no)
        while (arv.fronteira):
            
            arv.reordenar_fronteira()
            no = arv.fronteira.pop(0)
            arv.visitados.append(no.pos)
            self.repr_amb[no.pos[0]][no.pos[1]] = '◫'
            if no.pos == self.objetivo:
                print("custo: " + str(no.custo))
                # go for solution
                while no.pai:
                    solucao.append(no.acao)
                    no = no.pai
                solucao.reverse()
                break
            possib = self.acoes_com_result(no.pos)
            for acao in possib:
                no_tmp = arvore.No(no, [], acao[1], acao[0], no.custo + acao[2])
                if no_tmp.pos not in arv.visitados and no_tmp.pos not in [x.pos for x in arv.fronteira]:
#                    self.print_repr()
#                    print(acao)
#                    print(possib)
#                    input()
                    arv.inserir_nos(no_tmp)
                    arv.inserir_fronteira(no_tmp)
                    self.repr_amb[no_tmp.pos[0]][no_tmp.pos[1]] = '□'

            else:
                continue
            break
        print("quantidade de nós na arvore: " + str(len(arv.nos)))
        print("nós explorados: " + str(len(arv.visitados)))
#        print(arv.visitados)
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

