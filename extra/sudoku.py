#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 19:05:52 2017

@author: Tomás Abril
"""
# --- sudoku com feixe local ---
# ---

import random
import time
import itertools
#import matplotlib.pyplot as plt


class Main():

    def __init__(self):
        #
        graficos = False
        # linhas e colunas do campo
        grid = [x for x in range(9*9)]
        campolc = []
        for i, x in enumerate(grid):
            campolc.append((i // 9, i % 9))
#        print(campolc)

        # gerando onde checar por conflito ------------
        self.caso = {}
        for x, val in enumerate(grid):
            checar = []
            # linha
            for i in range(9):
                pos = (x//9)*9 + i
                if pos != x:
                    checar.append(pos)
            # coluna
            for i in range(9):
                pos = x % 9 + i * 9
                if pos != x:
                    checar.append(pos)
            # grupo
            for i, v in enumerate(grid):
                if self.grupo(campolc[x]) == self.grupo(campolc[i]) and x != i:
                    checar.append(i)
            checar = list(set(checar))
            self.caso[x] = checar
#        print(caso)

        # dicionario de posicoes por grupo
        dicgrupo = {}
        for i in range(9):
            dicgrupo[i] = []
        for x, val in enumerate(grid):
            dicgrupo[self.grupo(campolc[x])].append(x)
#        print(dicgrupo)

        # construindo campo ---------------------------
        numeros = [[x for x in range(1, 10)] for y in range(9)]
        for x in range(9):
            random.shuffle(numeros[x])
        for i, val in enumerate(grid):
            grid[i] = numeros[self.grupo(campolc[i])].pop()

        print("estado inicial - randomico ----------------")
        self.print_grid(grid)
        print(" -> aleatorio: ----------------------------")
        conf_r, v = self.aleatorio(grid, campolc)
        print(" -> all_permutations 81! possibilidades ---")
        #\n = 5797126020747367985879734231578109105412357244731625958745865049716390179693892056256184534249745940480000000000000000000")
        conf_ap, v = self.all_permut(grid[:], campolc)
        print(" -> hill_climb: ---------------------------")
        conf_hc, v = self.hill_climb(grid, campolc, dicgrupo)
        print(" -> local_beam_search: ", end='')
        conf_f, v = self.local_beam_search(grid[:], campolc, dicgrupo)
        print(" -> genético: -----------------------------")
        conf_g, v = self.genetic(grid[:], campolc, dicgrupo)
        if(graficos):
            import matplotlib.pyplot as plt
            fig = plt.figure()
            ax1 = fig.add_subplot(511)
            ax2 = fig.add_subplot(512)
            ax3 = fig.add_subplot(513)
            ax4 = fig.add_subplot(514)
            ax5 = fig.add_subplot(515)
            ax1.set_ylabel("conflitos")
            ax2.set_ylabel("conflitos")
            ax3.set_ylabel("conflitos")
            ax4.set_ylabel("conflitos")
            ax5.set_ylabel("conflitos")
            
            ax1.plot(conf_r)
            ax1.set_title("random")
            ax2.plot(conf_ap)
            ax2.set_title("all permutations")
            ax3.plot(conf_hc)
            ax3.set_title("hill climb")
            ax4.plot(conf_f)
            ax4.set_title("feixe")
            ax5.plot(conf_g)
            ax5.set_title("genetico")
            fig.tight_layout()
            plt.show()

    def sucessores(self, campo, campolc, dicgrupo):
        '''Todas as possibilidades de trocar apenas dois numeros dentro de um grupo. \n
            Retorna uma lista de grids. \n
            729 vizinhos
        '''
        # gerar vizinhos
        vizinhos = []
        for i, e in enumerate(campo):
            grupo = self.grupo(campolc[i])
            for j in dicgrupo[grupo]:
                tmp = list(campo[:])
                tmp[i], tmp[j] = tmp[j], tmp[i]
                vizinhos.append(tmp)
        return vizinhos

    def local_beam_search(self, campo, campolc, dicgrupo):
        k = 10
        max_plateau = 15
        print("k={} ----------------".format(k))
        flag = False
        vezes = 0
        conflitos_list = []
        andados = []
        x = 100
        minx = 100
        contador_de_parada = 0
        # cria k estados aleatorios
        estados = []
        for i in range(k):
            grid = [x for x in range(9*9)]
            numeros = [[x for x in range(1, 10)] for y in range(9)]
            for x in range(9):
                random.shuffle(numeros[x])
            for i, val in enumerate(grid):
                grid[i] = numeros[self.grupo(campolc[i])].pop()
            estados.append(grid)
        while x:
            # sucessores de todos os estados
            suc = []
            viz2 = []
            for i in range(k):
                andados.append(estados[i])
                viz = self.sucessores(estados[i], campolc, dicgrupo)
                viz2.clear()
                for cont, el in enumerate(viz):
                    if self.conflitos(el, campolc) == 0:
                        print("\nAchei a solução! em {} vezes".format(vezes))
                        self.print_grid(el)
                        flag = True
                        break
                    # retirando lugares ja andados
#                    if (el not in andados):
#                        viz2.append(el)
#                    else:
#                        print("ja estive aqui")
                if flag: break
                tup_viz = map(tuple, viz)
                tup_andados = map(tuple, andados)
                viz2 = list(set(tup_viz) - set(tup_andados))

#                viz2 = viz
#                print("len vizinhos: {}".format(len(viz)))
                if not viz2:
                    print("\nBeam_search ficou preso depois de {} vezes".format(vezes))
                    flag = True
                    break
                # ------------------------------------------------
                suc.extend(viz2)
#            print("len(andados) = " + str(len(andados)))
#            print("quantidade de sucessores:" + str(len(suc)))
            if flag: break
            estados.extend(suc)
            novos = []
            for i in range(k):
                idmin, valmin = min(enumerate(estados), key=lambda x: self.conflitos(x[1], campolc))
                novos.append(estados.pop(idmin))
            estados = novos
#            estados.sort(key=lambda x: self.conflitos(x, campolc), reverse=False)
            if len(estados) > k:
                estados = estados[:k]
            vezes += 1
#                xlist = []
#                for j in estados:
#                    xlist.append(self.conflitos(j, campolc))
#                print(xlist)
            x = self.conflitos(estados[0], campolc)
            conflitos_list.append(x)

            if x < minx:
                contador_de_parada = 0
                minx = x
            # para imprimir no terminal --------- ---
#                print()
#                print(x, end='')
#            print('.', end='', flush=True)
            # ----------------------------------- ---
            if x == minx:
                contador_de_parada += 1
            if contador_de_parada > max_plateau:
                flag = True
                print("\nparando local_beam_search, provavelmente está em um plateau e demoraria demais")
                print("executado {} vezes".format(vezes))
                break

        return conflitos_list, vezes

    def hill_climb(self, campo, campolc, dicgrupo):
        flag = False
        vezes = 0
        conflitos_list = []
        andados = []
        x = 100
        minx = 100
        atual = campo[:]
        while x:
            andados.append(atual)
            viz = self.sucessores(atual, campolc, dicgrupo)
            viz2 = []
            for cont, el in enumerate(viz):
                if self.conflitos(el, campolc) == 0:
                    print("\nAchei a solução! em {} vezes".format(vezes))
                    self.print_grid(el)
                    flag = True
                    break
                if el not in andados:
                    viz2.append(el)
            if flag: break
            viz = viz2
            if not viz:
                print("\nHill Climb ficou preso depois de {} vezes".format(vezes))
                flag = True
                break
            idmin, valmin = min(enumerate(viz), key=lambda x: self.conflitos(x[1], campolc))
            atual = viz[idmin]
            x = self.conflitos(atual, campolc)
            # para imprimir no terminal --------- ---
#            if x < minx:
#                minx = x
#                print()
#                print(x, end='')
#            print('.', end='', flush=True)
            # ----------------------------------- ---
            vezes += 1
            conflitos_list.append(x)
        return conflitos_list, vezes

    def genetic(self, campo, campolc, dicgrupo):
        flag = False
        populacao = 100
        max_geracao = 4000
        print("População = {}".format(populacao))
        pcross = 0.95
        pmut = 0.1
        melhor_por_geracao = []
        geracoes = 0
        conft = 100
        minc = 100
        pares = []
        # cria populacao estados aleatorios
        estados = [campo]
        for i in range(populacao - 1):
            grid = [x for x in range(9*9)]
            numeros = [[x for x in range(1, 10)] for y in range(9)]
            for x in range(9):
                random.shuffle(numeros[x])
            for i, val in enumerate(grid):
                grid[i] = numeros[self.grupo(campolc[i])].pop()
            estados.append(grid)
        while geracoes < max_geracao:
            geracoes += 1
            # avaliar fitness
            fit_list = [self.conflitos(x, campolc) for x in estados]
            conft = min(fit_list)
            melhor_por_geracao.append(conft)
            if not conft:
                print("\nAchei solução! em {} geracoes".format(geracoes))
                self.print_grid(estados[fit_list.index(conft)])
                break
            # criando pares para cruzamento
            pares.clear()
            for i in range(populacao//2):
                escolhido1 = self.roleta_genetica(estados, fit_list)
                escolhido2 = self.roleta_genetica(estados, fit_list)
                pares.append([escolhido1, escolhido2])
            # cruzamento
            filhos = []
            for par in pares:
                if random.uniform(0, 1) < pcross:
                    # crossover
                    filho1, filho2 = self.crossover_simples(par[0], par[1])

                    # corrigindo duplicações
                    filho1 = self.corrige_duplicados(filho1, campolc, dicgrupo)
                    filho2 = self.corrige_duplicados(filho2, campolc, dicgrupo)

                    # mutando filhos
                    filho1 = self.mutacao_ordem(filho1, pmut, campolc, dicgrupo)
                    filho2 = self.mutacao_ordem(filho2, pmut, campolc, dicgrupo)

                    filhos.append(filho1)
                    filhos.append(filho2)
            # juntando filhos aos pais
            estados.extend(filhos)
            # cortando para deixar apenas os melhores
            estados.sort(key=lambda x: self.conflitos(x, campolc), reverse=False)
            estados = estados[:populacao]
            # para imprimir no terminal --------- ---
#            conft = self.conflitos(estados[0], campolc)
#            if conft < minc:
#                minc = conft
#                print()
#                print(conft, end='')
#            print('.', end='', flush=True)
            # ----------------------------------- ---
        else:
            print("\nparando ... ainda não encontrou soluçao")
            print("Gerações: {}".format(geracoes))
            flag = True
        return (melhor_por_geracao, geracoes)

    def mutacao_ordem(self, lista, chance, campolc, dicgrupo):
        '''Recebe um campo de sudoku e chance de mutação. \n
           Retorna o campo talvez mutado. \n
           A mutação pode acontecer para todos os elementos do campo.\n
           Mutar significa uma troca entre dois numeros de um mesmo grupo.
        '''
        for i, elm in enumerate(lista):
            if random.uniform(0, 1) < chance:
#                print("Mutando !!")
                posat = self.grupo(campolc[i])
                esse_grupo = [lista[dicgrupo[posat][x]] for x in range(len(dicgrupo[posat]))]
                atrocar = random.choice(esse_grupo)
                lista[i], lista[atrocar] = lista[atrocar], lista[i]
        return lista

    def corrige_duplicados(self, cromossomo, campolc, dicgrupo):
        for i, gene in enumerate(cromossomo):
            posat = self.grupo(campolc[i])
            esse_grupo = [cromossomo[dicgrupo[posat][x]] for x in range(len(dicgrupo[posat]))]
            if esse_grupo.count(gene) > 1:
                nao_usadas = list(set([x for x in range(1, 10)]) - set(esse_grupo))
                aleat = random.randint(0, len(nao_usadas) - 1)
                cromossomo[i] = nao_usadas.pop(aleat)
        return cromossomo

    def crossover_simples(self, crmsm1, crmsm2):
        ponto_de_cross = random.randint(1, len(crmsm1)-1)
        filho1 = crmsm1[:ponto_de_cross] + crmsm2[ponto_de_cross:]
        filho2 = crmsm2[:ponto_de_cross] + crmsm1[ponto_de_cross:]
        return filho1, filho2

    def roleta_genetica(self, bixos, fitlist):
        fitlist = [1/x for x in fitlist]
        totalfit = sum(fitlist)
        marcador = random.uniform(0, totalfit)
        for i, bxo, in enumerate(fitlist):
            marcador -= bxo
            if marcador <= 0:
                return bixos[i]
        else:
            print("passou por tudo e nao escolheu")
            return bixos[i]

    def simulated_anealing(self):
        print("Não implementado")
        pass

    def conflitos(self, campo, campolc):
        conflitos = 0
        for i, val in enumerate(campo):
            confs = [campo[j] for j in self.caso[i]]
            if val in confs:
                conflitos += 1
        return conflitos

    def random_swap(self, campo, campolc, dicgrupo):
        num = random.randint(0, 9*9)
        gnum = self.grupo(campolc[num])
        num2 = random.choice(dicgrupo[gnum])
        campo[num], campo[num2] = campo[num2], campo[num]
#        print(num)
#        print(gnum)
#        print(num2)
        return campo

    def grupo(self, pos):
        ''' pos is a tuple os line, column \n
            return group in sudoku grid. from 0 to 8
        '''
        g = 0
        if 0 <= pos[0] <= 2 and 0 <= pos[1] <= 2:
            g = 0
        elif 3 <= pos[0] <= 5 and 0 <= pos[1] <= 2:
            g = 1
        elif 6 <= pos[0] <= 8 and 0 <= pos[1] <= 2:
            g = 2
        elif 0 <= pos[0] <= 2 and 3 <= pos[1] <= 5:
            g = 3
        elif 3 <= pos[0] <= 5 and 3 <= pos[1] <= 5:
            g = 4
        elif 6 <= pos[0] <= 8 and 3 <= pos[1] <= 5:
            g = 5
        elif 0 <= pos[0] <= 2 and 6 <= pos[1] <= 8:
            g = 6
        elif 3 <= pos[0] <= 5 and 6 <= pos[1] <= 8:
            g = 7
        elif 6 <= pos[0] <= 8 and 6 <= pos[1] <= 8:
            g = 8

        return g

    def print_grid(self, campo):
        char = '⬤'
#        char = '⬛'
        plinha = 0
        pcolun = 0
        posicao = 0
        for linha in range(9+4):
            for coluna in range(9+4):
                if linha in (0, 4, 8, 12):
                    print(char, end=' ')
                    plinha += 1
                elif coluna in (0, 4, 8, 12):
                    print(char, end=' ')
                    pcolun += 1
                else:
                    print(campo[posicao], end=' ')
                    posicao += 1
            print()
            plinha = 0

    def all_permut(self, grid, campolc):
        '''
        '''
#        possib = list(itertools.permutations(grid))
#        for item in possib:
#            if self.conflitos(item) == 0:
#                self.print_grid(grid)
#                break
#        pass
        cftlist = []
        vezes = 0
        cmin = 100
        for item in itertools.permutations(grid):
            c = self.conflitos(item, campolc)
            cftlist.append(c)
            vezes += 1
            if c == 0:
                print("Achei solução com {} vezes".format(vezes))
                self.print_grid(grid)
                break
            # para imprimir no terminal --------- ---
#            if c < cmin:
#                cmin = c
#                print()
#                print(c, end='')
#            print('.', end='', flush=True)
            # ----------------------------------- ---
            if vezes > 10000:
                print("\nParando depois de {} vezes".format(vezes))
                break
        return cftlist, vezes

    def aleatorio(self, grid, campolc):
        '''demora demais
        '''
        cont = 0
        cftlist = []
        cmin = 100
        while cont < 10000:
            numeros = [[x for x in range(1, 10)] for y in range(9)]
            for x in range(9):
                random.shuffle(numeros[x])
            for i, val in enumerate(grid):
                grid[i] = numeros[self.grupo(campolc[i])].pop()
            c = self.conflitos(grid, campolc)
            # para imprimir no terminal
#            if c < cmin:
#                cmin = c
#                print(cmin)
            cftlist.append(c)
            cont += 1
            if not c:
                self.print_grid(grid)
                print("Achei solução com {} vezes".format(cont))
                break
        else:
            print("Parando depos de {} vezes. Ainda não achou solução".format(cont))
        return cftlist, cont

main = Main()
