#!/usr/bin/env python
# -*- coding: utf-8 -*-

if 'import':
    import os
    import sys
    import itertools
    import random
    path_script = os.path.dirname(os.path.abspath(sys.argv[0]))
    sys.path.append(os.path.join(path_script, 'API'))
    import colorprint as cp
    import clear_consol as cc


class Generator():
    def __init__(self, symbols='abcd', length=8, edging=''):
        self.symbols = symbols
        self.length = length
        self.edging = edging
        self.lgen = None
        self.generate()

    def generate(self):
        self.lgen = [''.join(item) for item in itertools.product(self.symbols, repeat=self.length)]
        if self.edging:
            self.lgen = [self.edging + n + self.edging for n in self.lgen]

    def rand_lgen(self):
        random.shuffle(self.lgen)

    def get_generate(self):
        return self.lgen



# ==============================================================================

if __name__ == '__main__':
    os.system('color 71')
    cc.clearConsol()  # очищаем консоль

    class_gen = Generator('hbdp', 8, 'q')
    gen = class_gen.get_generate()
    print len(gen)
    class_gen.rand_lgen()
    # print class_gen.lgen
    print class_gen.get_generate()[:10]

    # time.sleep(1)
    raw_input('-------------   END   ---------------')
    
# ------------------------------------------------------------------------------
# chdir /D D:\Яндекс Диск\_Python\A_Python\Encrypt_CMS
# python D:\Яндекс Диск\_Python\A_Python\Encrypt_CMS\Generatot.py
