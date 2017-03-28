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


class No():
    # pai = []
    filhos = []
    pos = []

    def __init__(self, pai, filhos, pos, acao):
        self.pai = pai
        self.filhos = filhos
        self.pos = pos
        self.acao = acao

    def insert_filhos(self, filhos):
        self.filhos.extend(filhos)
