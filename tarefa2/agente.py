class Agente():
    representacao_ambiente = []
    minhaPosicao = [0, 0]

    def __init__(self, linha, coluna, ambiente):
        self.representacao_ambiente = ambiente

    def lerPosicao(self, posicao_real):
        print (posicao_real)
        self.minhaPosicao = posicao_real

    def mover(self, direcao):
