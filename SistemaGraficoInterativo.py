import matplotlib.pyplot as plt
import matplotlib
import mplcursors
import numpy as np
import math
import os
from matplotlib.patches import Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
matplotlib.use('TkAgg')

import operações as op
from mouseNavigation import MouseNavigation


lista_operacoes= ["Translação","Cisalhamento em X","Cisalhamento em Y","Escala","Rotação","Reflexão em X","Reflexão em Y"]
tkcanvas = None

def defineAx():
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Interactive 2D Cartesian Plane')

    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.plot()

def plot_2d_object(vertex, color):
    polygon = Polygon(vertex, closed=True, edgecolor=color, facecolor=color, alpha=0.5)
    ax.add_patch(polygon)
    return fig, ax

def update(vertex, matrix):
    vertex = ApplyTransformation(vertex,matrix)
    tkcanvas.get_tk_widget().pack_forget()
    fig, ax= plot_2d_object(vertex, 'r')
    defineAx()
    draw_figure(window['-CANVAS-'].TKCanvas, fig)

def centroid(vertex):
    coordsX = [vertex[0] for vertex in vertex]
    coordsY = [vertex[1] for vertex in vertex]
    centroidX = np.mean(coordsX)
    centroidY = np.mean(coordsY)
    return centroidX, centroidY
 
def ApplyTransformation(vertex,matrix):
    for i in range(len(vertex)):
        point = np.array([vertex[i][0], vertex[i][1], 1])
        transformed_point = np.dot(matrix, point)
        vertex[i] = (transformed_point[0], transformed_point[1])
    return vertex

def read_2d_object(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close()
    vertex = []
    
    for line in lines:
        if line.startswith('v '):
            line = line.split()
            x,y = float(line[1]), float(line[2])
            vertex.append((x,y))
    return vertex

def draw_figure(canvas, figure):
   global tkcanvas
   tkcanvas = FigureCanvasTkAgg(figure, canvas)
   tkcanvas.draw()
   tkcanvas.get_tk_widget().pack(side='top', fill='both', expand=1)





sg.theme('DarkAmber')   

layout = [ 
            [sg.Text('Enter the name of the object you want to load (triangle, square, cross):'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        sg.popup('Nenhum objeto foi carregado. Inicie novamente o programa.')
        exit()

    chosen_object = values[0]
    path = os.path.dirname(os.path.abspath(__file__))   #Obtem a pasta atual
    path = path + "\\" + chosen_object + ".obj"

    
    try:
        vertex = read_2d_object(path)
        sg.popup('Object loaded succefully!')
        break
    except FileNotFoundError:
        print("Object not found. Please try again.")
        sg.popup('Object not found. Please try again.')

window.close()




fig, ax = plt.subplots()

cursor = mplcursors.cursor(hover=True)

mouse_nav = MouseNavigation(ax)
fig.canvas.mpl_connect('scroll_event', mouse_nav.on_scroll)
fig.canvas.mpl_connect('button_press_event', mouse_nav.on_press)
fig.canvas.mpl_connect('button_release_event', mouse_nav.on_release)
fig.canvas.mpl_connect('motion_notify_event', mouse_nav.on_motion)

fig, ax = plot_2d_object(vertex, 'r')
defineAx()


layout = [
    [sg.Canvas(key='-CANVAS-')],
    [sg.Text("Escolha a operação que deseja realizar"), sg.Combo(lista_operacoes), sg.Button('Ok')]
]

window = sg.Window('Matplotlib In PySimpleGUI', layout,finalize=True)
draw_figure(window['-CANVAS-'].TKCanvas, fig)



while True:             # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    tranformation = values[0] 
    if tranformation == "Translação":
        tx = float(sg.popup_get_text('Insira o valor de tx'))
        ty = float(sg.popup_get_text('Insira o valor de ty'))
        matrix = op.tranlacao(tx,ty)
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Cisalhamento em X":
        shx = float(sg.popup_get_text('Insira o valor de shx'))
        matrix = op.cisalhamentoX(shx)
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Cisalhamento em Y":
        shy = float(sg.popup_get_text('Insira o valor de shy'))
        matrix = op.cisalhamentoY(shy)
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Escala":
        sx = float(sg.popup_get_text('Insira o valor de sx'))
        sy = float(sg.popup_get_text('Insira o valor de sy'))
        matrix = op.escala(sx,sy)
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Rotação":
        teta = float(sg.popup_get_text('Insira o valor de teta'))
        teta = math.radians(teta)
        centroidX, centroidY = centroid(vertex)

        matrixAux = op.tranlacao(-centroidX,-centroidY)
        update(vertex, matrixAux)

        matrix = op.rotacao(teta)
        update(vertex, matrix)

        matrixAux = op.tranlacao(centroidX,centroidY)
        
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrixAux)
        
    elif tranformation == "Reflexão em X":
        matrix = op.reflexaoX()
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Reflexão em Y":
        matrix = op.reflexaoY()
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    else:
        sg.popup('Nenhuma operação foi selecionada. Por favor, tente novamente.')
        break
   
window.close()
