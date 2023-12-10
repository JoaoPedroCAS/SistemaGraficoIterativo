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


lista_operacoes= ["Translação","Cisalhamento em X","Cisalhamento em Y","Escala","Rotação","Reflexão em X","Reflexão em Y"]
tkcanvas = None
def defineAx():
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Interactive 2D Cartesian Plane')

    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.plot()


def update(vertex, matrix):
    vertex = ApplyTransformation(vertex,matrix)
    tkcanvas.get_tk_widget().pack_forget()
    fig, ax= plot_2d_object(vertex, 'r')
    defineAx()
    draw_figure(window['-CANVAS-'].TKCanvas, fig)



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

def plot_2d_object(vertex, color):


    polygon = Polygon(vertex, closed=True, edgecolor=color, facecolor=color, alpha=0.5)
    ax.add_patch(polygon)

    return fig, ax
 
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
    McisalhamentoY = np.array([[1,shy,0],
                               [0,1,0],
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

def ApplyTransformation(vertex,matrix):
    for i in range(len(vertex)):
        point = np.array([vertex[i][0], vertex[i][1], 1])
        transformed_point = np.dot(matrix, point)
        vertex[i] = (transformed_point[0], transformed_point[1])
    return vertex


def draw_figure(canvas, figure):
   global tkcanvas
   tkcanvas = FigureCanvasTkAgg(figure, canvas)
   tkcanvas.draw()
   tkcanvas.get_tk_widget().pack(side='top', fill='both', expand=1)



class MouseNavigation:
    def __init__(self, ax):
        self.ax = ax
        self.press = None
        self.previous_xlim = ax.get_xlim()
        self.previous_ylim = ax.get_ylim()

    def on_scroll(self, event):
        if event.button == 'down':
            self.ax.set_xlim(self.ax.get_xlim()[0] * 1.1, self.ax.get_xlim()[1] * 1.1)
            self.ax.set_ylim(self.ax.get_ylim()[0] * 1.1, self.ax.get_ylim()[1] * 1.1)
        elif event.button == 'up':
            self.ax.set_xlim(self.ax.get_xlim()[0] / 1.1, self.ax.get_xlim()[1] / 1.1)
            self.ax.set_ylim(self.ax.get_ylim()[0] / 1.1, self.ax.get_ylim()[1] / 1.1)
        plt.draw()

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.press = event.xdata, event.ydata
        self.previous_xlim = self.ax.get_xlim()
        self.previous_ylim = self.ax.get_ylim()

    def on_release(self, event):
        self.press = None

    def on_motion(self, event):
        if self.press is None or event.inaxes != self.ax:
            return
        dx = (event.xdata - self.press[0])*0.7
        dy = (event.ydata - self.press[1])*0.7
        self.ax.set_xlim(self.previous_xlim[0] - dx, self.previous_xlim[1] - dx)
        self.ax.set_ylim(self.previous_ylim[0] - dy, self.previous_ylim[1] - dy)
        plt.draw()

# Create a figure and axis



sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [ 
            [sg.Text('Enter the name of the object you want to load (triangle, square, cross):'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
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


###################### Definições da janela ######################

fig, ax = plt.subplots()

cursor = mplcursors.cursor(hover=True)


mouse_nav = MouseNavigation(ax)
fig.canvas.mpl_connect('scroll_event', mouse_nav.on_scroll)
fig.canvas.mpl_connect('button_press_event', mouse_nav.on_press)
fig.canvas.mpl_connect('button_release_event', mouse_nav.on_release)
fig.canvas.mpl_connect('motion_notify_event', mouse_nav.on_motion)


fig, ax = plot_2d_object(vertex, 'r')
defineAx()


###################### Definições de layout ######################
left_column = [
    [sg.Canvas(key='-CANVAS-')]
]

# Define the right column
right_column = [
    [sg.Text("Escolha a operação que deseja realizar"), sg.Combo(lista_operacoes), sg.Button('Ok')]
]

# Create the layout with two columns
layout = [
    [
        sg.Column(left_column, element_justification='l'),  # 'l' for left justification
        sg.Column(right_column, element_justification='l')  # 'r' for right justification
    ],
]

window = sg.Window('Matplotlib In PySimpleGUI', layout,finalize=True)
draw_figure(window['-CANVAS-'].TKCanvas, fig)



while True:             # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    tranformation = values[0] 
    print(tranformation)
    if tranformation == "Translação":
        tx = float(sg.popup_get_text('Insira o valor de tx'))
        ty = float(sg.popup_get_text('Insira o valor de ty'))
        matrix = tranlacao(tx,ty)
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Cisalhamento em X":
        shx = float(sg.popup_get_text('Insira o valor de shx'))
        matrix = cisalhamentoX(shx)
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Cisalhamento em Y":
        shy = float(sg.popup_get_text('Insira o valor de shy'))
        matrix = cisalhamentoY(shy)
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Escala":
        sx = float(sg.popup_get_text('Insira o valor de sx'))
        sy = float(sg.popup_get_text('Insira o valor de sy'))
        matrix = escala(sx,sy)
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Rotação":
        teta = float(sg.popup_get_text('Insira o valor de teta'))
        teta = math.radians(teta)
        matrix = rotacao(teta)
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Reflexão em X":
        matrix = reflexaoX()
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    elif tranformation == "Reflexão em Y":
        matrix = reflexaoY()
        tkcanvas.get_tk_widget().pack_forget()
        ax.clear()
        update(vertex, matrix)
    else:
        sg.popup('Nenhuma operação foi selecionada. Por favor, tente novamente.')
        break

        
window.close()

#print(texto)




