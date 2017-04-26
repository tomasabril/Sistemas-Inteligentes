#!/usr/bin/env python3

# ----------------
# Tomás Abril
# ----------------
# NAO ESTA PRONTO AINDA
# !!!

import random
import time
import itertools



class Main():

    linhas = 0
    colunas = 0
    numeros = []
    grid = []

    def __init__(self):
        self.start_time = time.time()
        # tamanho da grade
        self.linhas = 3
        self.colunas = 4
        # inicializando grade
        self.grid = [['█' for i in range(self.colunas)] for j in range(self.linhas)]

        lista = self.ini_rand_inlist()

        conf_r, vez_r = self.random_shuffle(lista)
        print("iteracoes: " + str(vez_r))

        conf_r, vez_r = self.random_shuffle_inlist(lista[:])
        print("iteracoes: " + str(vez_r))

        conf_hc, vez_hc = self.hill_climb_all_permutations(lista[:])
        print("iteracoes: " + str(vez_hc))

        conf_hc, vez_hc = self.hill_climb(lista[:])
        print("iteracoes: " + str(vez_hc))

        conf_gd, vez_gd = self.genetico_decimal()
        print("iteracoes: " + str(vez_gd))

        print("\n--- %s seconds ---" % (time.time() - self.start_time))

    def genetico_decimal(self):
        print("\n> executando algoritmo genetico_decimal")
        func_time = time.time()

        populacao = 3
        pcross = 0.8
        pmut = 0.05
        melhor_por_geracao = []
        geracoes = 1
        conft = 10
        pares = []
        
        # inicializando geração 1
        # [ [5,6,1,3,2,4,8,9,7], [outro] ]
        bixos = [self.ini_rand_inlist() for _ in range(populacao)]
        print(bixos)
        while(True):
            fit_list = [self.avaliar_inlist(x) for x in bixos]
            conft = min(fit_list)
            if not conft:
                break
            pares.clear()
            #for i in enumerate(bixos):
            escolhido = self.roleta_genetica(bixos, fit_list)
            print(escolhido)
            break

        # imprimindo a população
        for bixo in bixos:
            self.print_inlist(bixo)
            print()

        time_t = time.time() - func_time
        print("--- total time: " + str(time_t))
        print("time per generation: " + str(time_t/geracoes))
        return (melhor_por_geracao, geracoes)

    def mutacao_posicao(self, lista):
        print("ainda nao implementado")
        pass

    def mutacao_ordem(self, lista):
        chance = 0.05
        if random.uniform(0, 1) > chance:
            pos1 = random.randrange(0, len(lista))
            pos2 = random.randrange(0, len(lista))
            lista[pos1], lista[pos2] = lista[pos2], lista[pos1]
        return lista

    def mutacao_aleatoria(self, lista):
        print("ainda nao implementado")
        pass

    def roleta_genetica(self, bixos, fitlist):
        fitlist = [1/x for x in fitlist]
        totalfit = sum(fitlist)
#        fitperc = [0 for _ in fitlist]
#        fitperc[0] = fitlist[0]/totalfit*100
#        for i in range(1, len(fitlist)):
#            fitperc[i] = fitperc[i-1] + fitlist[i]/totalfit*100

        marcador = random.uniform(0, totalfit)
        for i, bxo, in enumerate(fitlist):
            if marcador <= 0:
                break
            marcador -= bxo
        vencedor = bixos[i]        
        
        return vencedor


    def random_shuffle(self, lista):
        print("\n> executando random_shuffle")
        func_time = time.time()
        conflitos = []
        vezes = 0
        x = 10
        while(x > 1):
            self.ini_rand()
            x = self.avaliar()
            conflitos.append(x)
            vezes += 1
        self.print_ambiente()
        time_t = time.time() - func_time
        print("--- total time: " + str(time_t))
        print("time per iteration: " + str(time_t/vezes))
        return (conflitos, vezes)

    def random_shuffle_inlist(self, lista):
        print("\n> executando random_shuffle_inlist")
        func_time = time.time()
        conflitos = []
        vezes = 0
        x = 10
        while(x):
            random.shuffle(lista)
            x = self.avaliar_inlist(lista)
            conflitos.append(x)
            vezes += 1
        self.print_inlist(lista)
        time_t = time.time() - func_time
        print("--- total time: " + str(time_t))
        print("time per iteration: " + str(time_t/vezes))
        return (conflitos, vezes)

    def hill_climb_all_permutations(self, lista):
        print("\n> executando hill_climb_all_permutations")
        func_time = time.time()
        conflitos = [0]
        vezes = 1
        
        vizinhos = list(itertools.permutations(lista))
        
        # reordenar tudo parece ser lento
        # demora 0,2 segundos. 10x mais que fazer todas as permutacoes
#        vizinhos.sort(key=self.avaliar_inlist)
#        atual = vizinhos.pop(0) 

        # pegando o primeiro com 0 conflitos, ficou 5 vezes mais rapido assim
        for item in vizinhos:
            if self.avaliar_inlist(item) == 0:
                atual = item
                break

        self.print_inlist(list(atual))
        time_t = time.time() - func_time
        print("--- total time: " + str(time_t))
        print("time per iteration: " + str(time_t/vezes))
        return (conflitos, vezes)

    def hill_climb(self, lista):
        # nota: não pode deixar o algoritmo andar pra onde ele já foi,
        #       senao fica preso em plateau
        print("\n> executando hill_climb")
        func_time = time.time()
        conflitos = []
        vizinhos = []
        vezes = 0
        x = 10
        atual = lista[:]
        andados = []
        while x:
            andados.append(atual[:])
            # gerar vizinhos
            vizinhos.clear()
            for i in range(len(lista)):
                for j in range(i + 1, len(lista)):
                    tmp = atual[:]
                    tmp[i], tmp[j] = tmp[j], tmp[i]
                    vizinhos.append(tmp)
            vizinhos.sort(key=self.avaliar_inlist)
            proximo = vizinhos.pop(0)
            while proximo in andados:
                proximo = vizinhos.pop(0)
#            while self.avaliar_inlist(proximo) > self.avaliar_inlist(atual):
#                proximo = vizinhos.pop(0)
            atual = proximo
#            print(atual)
            x = self.avaliar_inlist(atual)
            conflitos.append(x)
            vezes += 1
        self.print_inlist(list(atual))
        time_t = time.time() - func_time
        print("--- total time: " + str(time_t))
        print("time per iteration: " + str(time_t/vezes))
        return (conflitos, vezes)

    def avaliar_inlist(self, lista):
        cnft = 0
        case = {0: (1, 2, 3, 4),
                1: (0, 3, 4, 5),
                2: (0, 3, 6),
                3: (0, 1, 2, 4, 6, 7),
                4: (0, 1, 3, 5, 6, 7),
                5: (1, 4, 7),
                6: (2, 3, 4, 7),
                7: (3, 4, 5, 6)}
        for i, num in enumerate(lista):
            conflitos = [lista[j] for j in case[i]]
            if (num + 1) in conflitos:
                cnft += 1
            if (num - 1) in conflitos:
                cnft += 1
        return cnft

    def print_inlist(self, lista):
        grid = grid = [['' for i in range(self.colunas)] for j in range(self.linhas)]
#        print()
        for lin in range(self.linhas):
            for col in range(self.colunas):
                if (lin == 0 and (col == 0 or col == self.colunas - 1)) \
                   or ((lin == self.linhas - 1)
                       and (col == 0 or col == self.colunas - 1)):
                    grid[lin][col] = '█'
                else:
                    grid[lin][col] = lista.pop(0)
                print(grid[lin][col], end=" ")
            print()

    def ini_rand_inlist(self):
        espacos = (self.linhas*self.colunas - 3)
        lista = [x for x in range(1, espacos)]
        random.shuffle(lista)
        return lista

    def avaliar(self):
        conflitos = 0
        for lin in range(self.linhas):
            for col in range(self.colunas):
                if (lin == 0 and (col == 0 or col == self.colunas - 1)) \
                   or ((lin == self.linhas - 1)
                       and (col == 0 or col == self.colunas - 1)):
                    pass
                else:
                    # numero na celula
                    num_at = self.grid[lin][col]
                    achecar = []
                    # linha
                    if 0 <= lin + 1 < self.linhas:
                        achecar.append(self.grid[lin + 1][col])
                    if 0 <= lin - 1 < self.linhas:
                        achecar.append(self.grid[lin - 1][col])
                    # coluna
                    if 0 <= col + 1 < self.colunas:
                        achecar.append(self.grid[lin][col + 1])
                    if 0 <= col - 1 < self.colunas:
                        achecar.append(self.grid[lin][col - 1])
                    # diagonais
                    if 0 <= lin + 1 < self.linhas:
                        if 0 <= col + 1 < self.colunas:
                            achecar.append(self.grid[lin + 1][col + 1])
                        if 0 <= col - 1 < self.colunas:
                            achecar.append(self.grid[lin + 1][col - 1])
                    if 0 <= lin - 1 < self.linhas:
                        if 0 <= col + 1 < self.colunas:
                            achecar.append(self.grid[lin - 1][col + 1])
                        if 0 <= col - 1 < self.colunas:
                            achecar.append(self.grid[lin - 1][col - 1])
                    # contando conflitos
                    conflitos += achecar.count(num_at + 1)
                    conflitos += achecar.count(num_at - 1)
        return conflitos

    def ini_rand(self):
        espacos = (self.linhas*self.colunas - 3)
        self.numeros = [x for x in range(1, espacos)]
        random.shuffle(self.numeros)
#        self.numeros = [5, 3, 2, 8, 1 ,7 ,6 ,4]
#        self.numeros.reverse()
        for lin in range(self.linhas):
            for col in range(self.colunas):
                if (lin == 0 and (col == 0 or col == self.colunas - 1)) \
                   or ((lin == self.linhas - 1)
                       and (col == 0 or col == self.colunas - 1)):
                    pass
                else:
                    self.grid[lin][col] = self.numeros.pop()

    def print_ambiente(self):
        for l in range(self.linhas):
            for c in range(self.colunas):
                print(self.grid[l][c], end=" ")
            print()


main = Main()
