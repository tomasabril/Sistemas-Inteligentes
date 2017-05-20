#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 2017

@author: Tomás Abril
"""

### madureza
# 1 verde
# 2 madura
# 3 podre
### fibras, proteinas, lipideos
# 1 pouca
# 2 moderada
# 3 alta


def write_tofile(string):
    if False:
        with open('energia-da-fruta.arff', 'a') as file:
            file.write(string)


def write_header():
    header = ('@relation energia-da-fruta\n\n' +

              '@attribute madureza {verde, madura, podre}\n' +
              '@attribute carboidratos {pouca, moderada, alta}\n' +
              '@attribute fibras {pouca, moderada, alta}\n' +
              '@attribute proteinas {pouca, moderada, alta}\n' +
              '@attribute lipideos {pouca, moderada, alta}\n' +
#              '@attribute energia {30, 140, 200}\n' +
#              '@attribute delta_energia {-15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160}\n\n' +
              '@attribute delta_energia {-10, 100, 160}\n\n' +

              '@data\n')
    write_tofile(header)

def translate(num):
    st = ''
    if num == 1:
        st = 'pouca'
    elif num == 2:
        st = 'moderada'
    elif num == 3:
        st = 'alta'
    return st

def write_data(m, c, f, p, l, de):
    if m == 1:
        m = 'verde'
    elif m == 2:
        m = 'madura'
    elif m == 3:
        m = 'podre'
    c = translate(c)
    f = translate(f)
    p = translate(p)
    l = translate(l)

    data = '{}, {}, {}, {}, {}, {}\n'.format(m, c, f, p, l, de)
    write_tofile(data)
