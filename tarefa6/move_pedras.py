#!/usr/bin/env python3

# ----------------
# Tomás Abril
# ----------------

import random
import time
import itertools
import matplotlib.pyplot as plt


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

        fig = plt.figure()
        ax1 = fig.add_subplot(411)
        ax2 = fig.add_subplot(412)
        ax3 = fig.add_subplot(413)
        ax4 = fig.add_subplot(414)
        ax1.set_ylabel("conflitos")
        ax2.set_ylabel("conflitos")
        ax3.set_ylabel("conflitos")
        ax4.set_ylabel("conflitos")

        lista = self.ini_rand_inlist()

        conf_r, vez_r = self.random_shuffle(lista)
        print("iteracoes: " + str(vez_r))
        ax1.plot(conf_r)
        ax1.set_title("random 1")

        conf_r, vez_r = self.random_shuffle_inlist(lista[:])
        print("iteracoes: " + str(vez_r))
        ax2.plot(conf_r)
        ax2.set_title("random 2")

        conf_hc, vez_hc = self.hill_climb_all_permutations(lista[:])
        print("iteracoes: " + str(vez_hc))
        ax3.plot(conf_hc)
        ax3.set_title("all permutations")

        conf_hc, vez_hc = self.hill_climb(lista[:])
        print("iteracoes: " + str(vez_hc))
        ax4.plot(conf_hc)
        ax4.set_title("hill climb")

        fig.tight_layout()
        plt.show()

        print("\n--- %s seconds ---" % (time.time() - self.start_time))

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
