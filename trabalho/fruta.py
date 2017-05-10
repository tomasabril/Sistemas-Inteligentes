# -----
#
# Tomás Abril
# Allan Patrick

import random

class Fruta():

    # 1 verde
    # 2 madura
    # 3 podre
    madureza = 0
    # 1 pouca
    # 2 moderada
    # 3 alta
    fibras = 0
    proteinas = 0
    lipideos = 0
    # 30, 140 ou 200
    energia = 0

    def __init__(self):
        self.madureza = random.randint(1,3)
        self.fibras = random.randint(1,3)
        self.proteinas = random.randint(1,3)
        self.lipideos = random.randint(1,3)
        self.energia =  = random.choice([30, 140, 200])



