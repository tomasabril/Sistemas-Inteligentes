# -----
#
# Tomás Abril
# Allan Patrick

import math
import arvore
import random
import fruta
import arff_creator

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
    energia = 300
    id3 = False

    def __init__(self, agentepos, ambiente, andavel, parede, frutas):
        self.repr_amb = ambiente
        self.minhaPosicao = agentepos[:]
        self.linhaTamanho = len(ambiente)
        self.colunaTamanho = len(ambiente[0])
        self.andavel = andavel
        self.parede = parede
        self.frutas = frutas
        self.bolso = []

    def reinicializar(self):
        self.energia = 300
        self.bolso.clear()

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

    def atualiza_posicao(self, pos):
        self.minhaPosicao = pos[:]
        self.repr_amb[pos[0]][pos[1]] = 'A'


    def busca_lrta(self, inicializar_h = False):
        cheguei = 0
        solucao = []
        custo = 0
        custo1 = (8, 4, 6, 2)
        custo15 = (7, 9, 1, 3)
        # proximo = [movimento, [pos], custo + estimativa]
        proximo = []
        # h { (linha, coluna) : estimativa }
        if inicializar_h:
            # esvazia o arquivo
            with open('energia-da-fruta.arff', 'w') as file:
                pass
            arff_creator.write_header()
            # cria a euristica pro ambiente inteiro
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
#            print("acao: " + str(proximo[0]))
            if self.energia < 0:
#                print('Morri !!')
#                self.repr_amb[self.minhaPosicao[0]][self.minhaPosicao[1]] = 'X'
                break
#            self.print_repr()
#            print('energia: {}'.format(self.energia))
#            print('frutas no bolso: {}'.format(len(self.bolso)))

#            input()

#        print("Estimativas: " + str(self.est_h))
#        print("Custo: " + str(custo))
        else:
            cheguei = 1
#            print('.', end='')
        return solucao, cheguei

    def ver_fruta(self):
        ''' O que fazer quando ver uma fruta.

        '''
        energ = 0
        # comer ou nao aleatoriamente
        ant = self.energia
        fruta_daqui = self.frutas[tuple(self.minhaPosicao)]
        if not self.id3:
#            if random.random() > 0.2:
            if True:
#                    print('Comendo')
                energ = fruta_daqui.comer()
                self.energia += energ
                self.energia -= 40
            else:
                # se não comeu pode talvez guardar
                if self.energia > 400:
#                        print('Guardando')
                    self.bolso.append(fruta_daqui)
                    fruta_daqui.guardar()
        if self.id3:
            if self.id3table_final(fruta_daqui):
                if self.energia > 440:
#                        print('Guardando')
                    self.bolso.append(fruta_daqui)
                    fruta_daqui.guardar()
                else:
#                        print('Comendo')
                    energ = fruta_daqui.comer()
                    self.energia += energ
                    self.energia -= 40

        if self.energia > 600:
            self.energia = 600
        depois = self.energia
        delta = depois - ant

        # pode talvez ainda comer o que tem guardado
        if self.bolso and self.energia < 440:
#            print('Comendo do bolso')
            self.energia += self.bolso.pop(0).comer()
            self.energia -= 40

        f = fruta_daqui
        arff_creator.write_data(f.madureza, f.carboidratos, f.fibras, f.proteinas, f.lipideos, delta)
#        print('mudança de energia: {}'.format(delta))

    def id3table_final(self, frut):
        ### madureza
        # 1 verde
        # 2 madura
        # 3 podre
        ### fibras, proteinas, lipideos
        # 1 pouca
        # 2 moderada
        # 3 alta
        proteinas = frut.proteinas
        madureza = frut.madureza
        carboidratos= frut.carboidratos
        fibras = frut.fibras
        lipideos = frut.lipideos
#        print('caracts dessa fruta: prot:{} mad:{} carb:{} fibr:{} lip:{}'.format(proteinas, madureza, carboidratos, fibras, lipideos))
        verde = 1
        madura = 2
        podre = 3

        pouca = 1
        moderada = 2
        alta = 3

	    v = -1

	    if madureza == verde:
	        if carboidratos == pouca:
                if fibras == pouca: valor = -10
	    |  |  if fibras == moderada: v = -10
	    |  |  if fibras == alta:
	    |  |  |  proteinas = pouca: -10
	    |  |  |  proteinas = moderada: -10
	    |  |  |  proteinas = alta
	    |  |  |  |  lipideos = pouca: 100
	    |  |  |  |  lipideos = moderada: -10
	    |  |  |  |  lipideos = alta: -10
	    |  carboidratos = moderada
	    |  |  lipideos = pouca: -10
	    |  |  lipideos = moderada: 100
	    |  |  lipideos = alta: 100
	    |  carboidratos = alta
	    |  |  lipideos = pouca: -10
	    |  |  lipideos = moderada: 100
	    |  |  lipideos = alta: 100
	    madureza = madura
	    |  carboidratos = pouca
	    |  |  lipideos = pouca
	    |  |  |  proteinas = pouca: -10
	    |  |  |  proteinas = moderada: -10
	    |  |  |  proteinas = alta
	    |  |  |  |  fibras = pouca: -10
	    |  |  |  |  fibras = moderada: -10
	    |  |  |  |  fibras = alta: 100
	    |  |  lipideos = moderada: 100
	    |  |  lipideos = alta: 100
	    |  carboidratos = moderada
	    |  |  lipideos = pouca: 160
	    |  |  lipideos = moderada
	    |  |  |  fibras = pouca: 160
	    |  |  |  fibras = moderada
	    |  |  |  |  proteinas = pouca: 160
	    |  |  |  |  proteinas = moderada: 160
	    |  |  |  |  proteinas = alta: 160
	    |  |  |  fibras = alta
	    |  |  |  |  proteinas = pouca: 160
	    |  |  |  |  proteinas = moderada: 160
	    |  |  |  |  proteinas = alta: 160
	    |  |  lipideos = alta
	    |  |  |  fibras = pouca: 160
	    |  |  |  fibras = moderada
	    |  |  |  |  proteinas = pouca: 160
	    |  |  |  |  proteinas = moderada: 160
	    |  |  |  |  proteinas = alta: 160
	    |  |  |  fibras = alta: 160
	    |  carboidratos = alta
	    |  |  lipideos = pouca
	    |  |  |  fibras = pouca
	    |  |  |  |  proteinas = pouca: 160
	    |  |  |  |  proteinas = moderada: 160
	    |  |  |  |  proteinas = alta: 160
	    |  |  |  fibras = moderada: 160
	    |  |  |  fibras = alta
	    |  |  |  |  proteinas = pouca: 160
	    |  |  |  |  proteinas = moderada: 160
	    |  |  |  |  proteinas = alta: 160
	    |  |  lipideos = moderada
	    |  |  |  fibras = pouca: 160
	    |  |  |  fibras = moderada
	    |  |  |  |  proteinas = pouca: 160
	    |  |  |  |  proteinas = moderada: 160
	    |  |  |  |  proteinas = alta: 160
	    |  |  |  fibras = alta: 160
	    |  |  lipideos = alta: 160
	    madureza = podre: -10

        if v > 0:
            return True
        else:
            return False

    def id3table_3(self, frut):
        ### madureza
        # 1 verde
        # 2 madura
        # 3 podre
        ### fibras, proteinas, lipideos
        # 1 pouca
        # 2 moderada
        # 3 alta
        proteinas = frut.proteinas
        madureza = frut.madureza
        carboidratos= frut.carboidratos
        fibras = frut.fibras
        lipideos = frut.lipideos
#        print('caracts dessa fruta: prot:{} mad:{} carb:{} fibr:{} lip:{}'.format(proteinas, madureza, carboidratos, fibras, lipideos))
        valor = -1
        if madureza == 1:
            if lipideos == 1: valor = -10
            if lipideos == 2:
                if carboidratos == 1: valor = -10
                if carboidratos == 2: valor = 100
                if carboidratos == 3: valor = -1
            if lipideos == 3: valor = 100
        if madureza == 2:
            if carboidratos == 1:
                if proteinas == 1: valor = -1
                if proteinas == 2: valor = -10
                if proteinas == 3: valor = 100
            if carboidratos == 2: valor = 160
            if carboidratos == 3: valor = 160
        if madureza == 3: valor = -10

        if valor > 0:
            return True
        else:
            return False


    def id3table_2(self, frut):
        ### madureza
        # 1 verde
        # 2 madura
        # 3 podre
        ### fibras, proteinas, lipideos
        # 1 pouca
        # 2 moderada
        # 3 alta
        proteinas = frut.proteinas
        madureza = frut.madureza
        carboidratos= frut.carboidratos
        fibras = frut.fibras
        lipideos = frut.lipideos
        print('caracts dessa fruta: prot:{} mad:{} carb:{} fibr:{} lip:{}'.format(proteinas, madureza, carboidratos, fibras, lipideos))
        valor = -1
        if madureza == 1:
            if carboidratos == 1:
                if proteinas == 1: valor = -10
                if proteinas == 2: valor = -1
                if proteinas == 3: valor = 100
            if carboidratos == 2:
                if proteinas == 1: valor = 100
                if proteinas == 2: valor = -10
                if proteinas == 3: valor = 100
            if carboidratos == 3:
                if lipideos == 1: valor = -10
                if lipideos == 2: valor = 100
                if lipideos == 3: valor = 100
        if madureza == 2:
            if carboidratos == 1:
                if fibras == 1: valor = 100
                if fibras == 2: valor = -10
                if fibras == 3: valor = 100
            if carboidratos == 2: valor = 160
            if carboidratos == 3: valor = -1
        if madureza == 3: valor = -10

        if valor > 0:
            return True
        else:
            return False


    def id3table_1(self, frut):
        ### madureza
        # 1 verde
        # 2 madura
        # 3 podre
        ### fibras, proteinas, lipideos
        # 1 pouca
        # 2 moderada
        # 3 alta
        proteinas = frut.proteinas
        madureza = frut.madureza
        carboidratos= frut.carboidratos
        fibras = frut.fibras
        lipideos = frut.lipideos
        print('caracts dessa fruta: prot:{} mad:{} carb:{} fibr:{} lip:{}'.format(proteinas, madureza, carboidratos, fibras, lipideos))
        valor = -1
        if proteinas == 1:
            if madureza == 1:
                if carboidratos == 1: valor = -10
                if carboidratos == 2: valor = 100
                if carboidratos == 3: valor = 100
            if madureza == 2: valor = 160
            if madureza == 3: valor = -1
        if proteinas == 2:
            if madureza == 1: valor = -10
            if madureza == 2:
                if fibras == 1: valor = -10
                if fibras == 2: valor = -1
                if fibras == 3: valor = 100
            if madureza == 3: valor = -10
        if proteinas == 3:
            if carboidratos == 1: valor = -10
            if carboidratos == 2: valor = -10
            if carboidratos == 3: valor = 160
        if valor > 0:
            return True
        else:
            return False

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
        self.energia -= 100 - 5*len(self.bolso)
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
        self.ver_fruta()

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
