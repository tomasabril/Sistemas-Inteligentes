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
        self.fronteira.sort(key=lambda no_de_fronteira: no_de_fronteira.custo)


class No():
    # pai = []
    filhos = []
    pos = []
    custo = 0

    def __init__(self, pai, filhos, pos, acao, custo):
        self.pai = pai
        self.filhos = filhos
        self.pos = pos
        self.acao = acao
        self.custo = custo

    def insert_filhos(self, filhos):
        self.filhos.extend(filhos)
