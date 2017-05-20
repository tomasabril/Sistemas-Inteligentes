#!/usr/bin/env python3

# ----------------
# Tomás Abril
# Allan Patrick
# ----------------

import time
import ambiente
import agente
import arvore
import matplotlib.pyplot as plt


def main():

    linha = 9
    coluna = 9

    amb = ambiente.Ambiente(linha, coluna)

    # criando paredes como no pdf
    paredes = [[0, 0], [0, 1], [0, 4], [0, 5], [0, 6], [0, 7],
               [1, 0],
               [2, 3], [2, 4], [2, 5],
               [3, 3], [3, 4], [3, 5], [3, 6],
               [5, 2], [5, 5], [5, 7],
               [6, 1], [6, 4], [6, 5], [6, 7],
               [7, 1], [7, 4], [7, 7],
               [8, 1], [8, 2],
               ]

    for i in range(len(paredes)):
        amb.add_obstaculo(paredes[i][0], paredes[i][1])

    amb.colocar_frutas()
    pos_inicial = [8, 0]
    pos_objetivo = [2, 6]
    agt = agente.Agente(pos_inicial, amb.get_ambiente(), amb.andavel, amb.parede, amb.frutas)
    agt.set_objetivo(pos_objetivo)
    amb.set_agente(agt.minhaPosicao)

#    print("Executando LRTA*")
    total = 10000
    eng_rest_rand = []
    eng_rest_id3 = []
    custos_rand = []

    if True:
        vezes = 0
        cont = 0

        agt.id3 = False
    #    while(fim == ""):
        while(vezes < total):
            agt.atualiza_posicao(pos_inicial)
            amb.atualiza_agente(agt.minhaPosicao)
            amb.reseta_chao()
    #        amb.reset_frutas()
            amb.colocar_frutas()
            agt.reinicializar()

            agt.set_objetivo(pos_objetivo)

    #        print("ambiente no inicio: ")
    #        amb.print_ambiente()
    #        print("posicao do agente" + str(agt.get_posicao()))
    #        print("objetivo: " + str(agt.objetivo))

    #        print("executando LRTA* ... \n")
            if vezes == 0:
                comandos, custo, chegou, eng_rest = agt.busca_lrta(inicializar_h=True)
            else:
                comandos, custo, chegou, eng_rest = agt.busca_lrta()

    #        print("\nnumero de espacos vazios: " + str(linha * coluna - len(paredes)))
    #        print("solucao: " + str(agt.comandos))

    #        print("ambiente no fim: ")
    #        amb.print_ambiente()
    #        print(amb.get_agentpos())
    #        print(agt.get_posicao())
            if chegou:
                eng_rest_rand.append(eng_rest)
                custos_rand.append(custo)

            vezes += 1
            cont += chegou

    #        fim = input("fim da execução, enter para re-executar: ")
        print('cheguei {}/{} vezes comendo metade das frutas'.format(cont, total))

    cmds = []
    custos = []
    comp = []

    if True:
        vezes = 0
        cont = 0
        agt.id3 = True
        while(vezes < total):
    #        print('----------------')
            agt.atualiza_posicao(pos_inicial)
            amb.atualiza_agente(agt.minhaPosicao)
            amb.reseta_chao()
            amb.colocar_frutas()
            agt.reinicializar()

            agt.set_objetivo(pos_objetivo)

            if vezes == 0:
                comandos, custo, chegou, eng_rest = agt.busca_lrta(inicializar_h=True)
            else:
                comandos, custo, chegou, eng_rest = agt.busca_lrta()

            vezes += 1
            cont += chegou

            # salvando caminhos
            if chegou:
                cmds.append(comandos)
                custos.append(custo)
                comp.append(12/custo)
                eng_rest_id3.append(eng_rest)
            else:
                comp.append(0)


        customin = min(custos)
        otimos = []
        for i, c in enumerate(cmds):
            if custos[i] <= customin:
                if c not in otimos:
                    otimos.append(c)

        print('cheguei {}/{} vezes com regras do ID3'.format(cont, total))
        print('custo minimo: {}'.format(customin))
        print('achei {} caminhos ótimos'.format(len(otimos)))
        print('\n'.join(map(str, otimos)))
        mediarand = sum(eng_rest_rand)/len(eng_rest_rand)
        print('media de energia no fim comendo 50% das frutas: {}'.format(mediarand))
        mediaid3 = sum(eng_rest_id3)/len(eng_rest_id3)
        print('media de energia no fim com id3: {}'.format(mediaid3))

        desemp_id3 = 0
        desemp_id3 = mediaid3/max(eng_rest_id3)
        desemp_id3 += min(custos)/(sum(custos)/len(custos))
        desemp_id3 += len(custos)/(len(custos)+len(custos_rand))
        print('Medida de desempenho do id3 = {}'.format(desemp_id3))

        desemp_r = 0
        desemp_r = mediarand/max(eng_rest_rand)
        desemp_r += min(custos_rand)/(sum(custos_rand)/len(custos_rand))
        desemp_r += len(custos_rand)/(len(custos)+len(custos_rand))
        print('Medida de desempenho comendo 50% = {}'.format(desemp_r))

        flag = 0
        for i, c in enumerate(comp):
            if c >= 1:
                flag += 1
            if flag >= 10:
                break
        comp = comp[:i+1]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.stem(comp)
        ax.grid(True)
        ax.set_xlabel('execução')
        ax.set_ylabel('comp(x)=c*/g(x)')


        fig2 = plt.figure()
        ax1 = fig2.add_subplot(111)
        ax1.plot(eng_rest_id3, 'r')
        ax1.plot(eng_rest_rand)
#        plt.show()

if __name__ == "__main__":
    # execute only if run from here
    main()
