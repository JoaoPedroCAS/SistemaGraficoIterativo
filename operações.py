import numpy as np
import math


def tranlacao (tx,ty):
    Mtranslacao = np.array([[1,0,tx],
                           [0,1,ty],
                           [0,0,1]])
    return Mtranslacao

def cisalhamentoX (shx):
    McisalhamentoX = np.array([[1,shx,0],
                               [0,1,0],
                               [0,0,1]])
    return McisalhamentoX

def cisalhamentoY (shy):
    McisalhamentoY = np.array([[1,0,0],
                               [shy,1,0],
                               [0,0,1]])
    return McisalhamentoY

def escala (sx,sy):
    Mescala = np.array([[sx,0,0],
                        [0,sy,0],
                        [0,0,1]])
    return Mescala

def rotacao (teta):
    Mrotacao = np.array([[math.cos(teta), (math.sin(teta) * -1),0],
                            [math.sin(teta), math.cos(teta),0],
                            [0,0,1]])
    return Mrotacao

def reflexaoX ():
    MreflexaoX = np.array([[-1,0,0],
                           [0,1,0],
                           [0,0,1]])
    return MreflexaoX

def reflexaoY ():
    MreflexaoY = np.array([[1,0,0],
                           [0,-1,0],
                           [0,0,1]])
    return MreflexaoY