# -----
#
# Tomás Abril
# Allan Patrick

import random


class Fruta():
    ### madureza
    # 1 verde
    # 2 madura
    # 3 podre
    ### fibras, proteinas, lipideos
    # 1 pouca
    # 2 moderada
    # 3 alta


    def __init__(self):
#        self.aqui = True
        self.madureza = random.randint(1, 3)
        self.carboidratos = random.randint(1, 3)
        self.fibras = random.randint(1, 3)
        self.proteinas = random.randint(1, 3)
        self.lipideos = random.randint(1, 3)

    def comer(self):
        '''Retorna quantidade de energia dependendo das caracteristicas da fruta
        '''
#        self.aqui = False
        if self.lipideos > 1:
            if self.carboidratos > 1:
                if self.madureza == 1:
                    return 140
                if self.madureza == 2:
                    return 200
                if self.madureza == 3:
                    return 30
            if self.carboidratos == 1:
                if self.madureza in (1, 3):
                    return 30
                if self.madureza == 2:
                    return 140
        if self.lipideos == 1:
            if self.carboidratos > 1:
                if self.madureza in (1, 3):
                    return 30
                if self.madureza == 2:
                    return 200
            else:
                if self.proteinas == 3 and self.fibras == 3 and self.madureza != 3:
                    return 140
        return 30

    def guardar(self):
        self.aqui = False
