# -----
#
# Tomás Abril
# Allan Patrick


class Arvore():
    nos = []
    visitados = []
    fronteira = []

    def inserir_nos(self, no):
        self.nos.append(no)

    def inserir_fronteira(self, no):
        self.fronteira.append(no)

    def reordenar_fronteira(self):
#        self.fronteira = sorted(self.fronteira, key=lambda no_de_fronteira: no_de_fronteira.custo)
        self.fronteira.sort(key=lambda no_de_fronteira: no_de_fronteira.custo)

    def reordenar_fronteira_f(self):
        self.fronteira.sort(key=lambda no_de_fronteira: no_de_fronteira.f)


class No():
    # pai = []
    filhos = []
    pos = []
    custo = 0   # do inicio até aqui
    h = 0       # estimativa de distancia do nó até o objetivo
    f = 0       # f = custo + h

    def __init__(self, pai, filhos, pos, acao, custo, h=0):
        self.pai = pai
        self.filhos = filhos
        self.pos = pos
        self.acao = acao
        self.custo = custo
        self.h = h
        self.f = custo + h

    def insert_filhos(self, filhos):
        self.filhos.extend(filhos)

