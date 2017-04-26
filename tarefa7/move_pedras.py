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

        populacao = 50
        pcross = 0.85
        pmut = 0.05
        melhor_por_geracao = []
        geracoes = 0
        conft = 10
        pares = []

        # inicializando geração 1
        # [ [5,6,1,3,2,4,8,9,7], [outro] ]
        bixos = [self.ini_rand_inlist() for _ in range(populacao)]

        while(geracoes < 5000):
            geracoes += 1
            # avaliar fitness
            fit_list = [self.avaliar_inlist(x) for x in bixos]

            # ver se tem alguem que soluciona
            conft = min(fit_list)
            melhor_por_geracao.append(conft)
            if not conft:
                self.print_inlist(bixos[fit_list.index(conft)])
                break

            # fazendo cruzamento
            # ..criando pares
            pares.clear()
            for i in range(populacao//2):
                escolhido1 = self.roleta_genetica(bixos, fit_list)
                escolhido2 = self.roleta_genetica(bixos, fit_list)
                pares.append([escolhido1, escolhido2])

            # cruzamento entre os pares
            filhos = []
            for par in pares:
                if random.uniform(0, 1) < pcross:
                    # crossover
                    filho1, filho2 = self.crossover_simples(par[0], par[1])
                    
                    # corrigindo duplicações
                    filho1 = self.corrige_duplicados(filho1)
                    filho2 = self.corrige_duplicados(filho2)

                    # mutando filhos
                    filho1 = self.mutacao_ordem(filho1, pmut)
                    filho2 = self.mutacao_ordem(filho2, pmut)

                    filhos.append(filho1)
                    filhos.append(filho2)
            # juntando filhos aos pais
            bixos.extend(filhos)
            # cortando para deixar apenas os melhores
            bixos.sort(key=self.avaliar_inlist)
            bixos = bixos[:populacao]

        else:
            print("Não encontrou soluçao ")

        time_t = time.time() - func_time
        print("--- total time: " + str(time_t))
        print("time per generation: " + str(time_t/geracoes))
        return (melhor_por_geracao, geracoes)

    def corrige_duplicados(self, cromossomo):
        for i, gene in enumerate(cromossomo):
            if gene in cromossomo[i+1:]:
                cromossomo[i] = list(set([x for x in range(9)]) - set(cromossomo)).pop()
        return cromossomo

    def crossover_simples(self, crmsm1, crmsm2):
        ponto_de_cross = random.randint(1, len(crmsm1)-1)
        filho1 = crmsm1[:ponto_de_cross] + crmsm2[ponto_de_cross:]
        filho2 = crmsm2[:ponto_de_cross] + crmsm1[ponto_de_cross:]
        return filho1, filho2

    def crossover_pmx(self, crmsm1, crmsm2):
    
        pass

    def mutacao_posicao(self, lista):
        print("ainda nao implementado")
        pass

    def mutacao_ordem(self, lista, chance):
        for i in range(len(lista)):
            if random.uniform(0, 1) < chance:
#                print("Mutando !!")
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
#        print("total fit " + str(totalfit))
#        print("fitlist " + str(fitlist))
        marcador = random.uniform(0, totalfit)
#        print("marcador " + str(marcador))
        for i, bxo, in enumerate(fitlist):
            marcador -= bxo
            if marcador <= 0:
#                print("o escolhido foi: " + str(bixos[i]))
                return bixos[i]
        else:
            print("passou por tudo e nao escolheu")
            return bixos[i]

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
