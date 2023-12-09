import matplotlib.pyplot as plt
import matplotlib
import mplcursors
import numpy as np
import math


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
matplotlib.use('TkAgg')

lista_operacoes= ["Translação","Cisalhamento","Escala","Rotação","Reflexão em X","Reflexão em Y"]


def set_layout(opcao):
    #print(opcao)

    left_column = [
        [sg.Canvas(key='-CANVAS-')]
    ]

    # Define the right column
    right_column = [
        [sg.Text('Enter the name of the object you want to load (cube, square, circle, etc.):'),  sg.InputText(), sg.Button('Ok')],
        [sg.Text("Escolha a operação que deseja realizar               "), sg.Combo(lista_operacoes)],
        [sg.Text("", key='campo1'), sg.InputText()],
        [sg.Text("", key='campo2'), sg.InputText()]


    ]

    # Create the layout with two columns
    layout = [
        [
            sg.Column(left_column, element_justification='l'),  # 'l' for left justification
            sg.Column(right_column, element_justification='l')  # 'r' for right justification
        ],
        [sg.Button('Button 5')]  # Button outside the columns
    ]

    return layout

    

def verificaOpcao(opcao):
    texto = []
    if opcao == "Translação":
        texto.append("Digite o valor de tx")
        texto.append("Digite o valor de ty")
        return texto
    elif opcao == "Cisalhamento":
        texto.append("Digite o valor de shx")
        texto.append("Digite o valor de ty")
        return texto	
    elif opcao == "Escala": 
        texto.append("Digite o valor de sx")
        texto.append("Digite o valor de sy")
        return texto
    elif opcao == "Rotação":
        texto.append("Digite o valor de teta")
        texto.append("CAMPO VAZIO")
        return texto
    elif opcao == "Reflexão em X": 
        texto.append("CAMPO VAZIO")
        texto.append("CAMPO VAZIO")
        return texto
    elif opcao == "Reflexão em Y": 
        texto.append("CAMPO VAZIO")
        texto.append("CAMPO VAZIO")
        return texto
    
        

def tranlacao (atual,tx,ty):
    Mtranslacao = np.array([[1,0,tx],
                           [0,1,ty],
                           [0,0,1]])
    nova = atual.dot(Mtranslacao)
    return nova

def cisalhamentoX (atual,shx):
    McisalhamentoX = np.array([[1,shx,0],
                               [0,1,0],
                               [0,0,1]])
    nova = atual.dot(McisalhamentoX)
    return nova

def cisalhamentoY (atual,shy):
    McisalhamentoY = np.array([[1,shy,0],
                               [0,1,0],
                               [0,0,1]])
    nova = atual.dot(McisalhamentoY)
    return nova

def escala (atual,sx,sy):
    Mescala = np.array([[sx,0,0],
                        [0,sy,0],
                        [0,0,1]])
    nova = atual.dot(Mescala)
    return nova

def rotacao (atual,teta):
    Mrotacao = np.array([[math.cos(teta), (math.sin(teta) * -1),0],
                            [math.sin(teta), math.cos(teta),0],
                            [0,0,1]])
    nova = atual.dot(Mrotacao)
    return nova

def reflexaoX (atual):
    MreflexaoX = np.array([[-1,0,0],
                           [0,1,0],
                           [0,0,1]])
    nova = atual.dot(MreflexaoX)
    return nova

def reflexaoY (atual):
    MreflexaoY = np.array([[1,0,0],
                           [0,-1,0],
                           [0,0,1]])
    nova = atual.dot(MreflexaoY)
    return nova



def draw_figure(canvas, figure):
   tkcanvas = FigureCanvasTkAgg(figure, canvas)
   tkcanvas.draw()
   tkcanvas.get_tk_widget().pack(side='top', fill='both', expand=1)
   return tkcanvas

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
fig, ax = plt.subplots()

# Initial position of the point
initial_x = 0.5
initial_y = 0.5

# Plot the initial point
point, = ax.plot(initial_x, initial_y, marker='o', color='red', markersize=10)

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Interactive 2D Cartesian Plane')

# Enable cursor interaction
cursor = mplcursors.cursor(hover=True)

# Create an instance of MouseNavigation and connect events
mouse_nav = MouseNavigation(ax)
fig.canvas.mpl_connect('scroll_event', mouse_nav.on_scroll)
fig.canvas.mpl_connect('button_press_event', mouse_nav.on_press)
fig.canvas.mpl_connect('button_release_event', mouse_nav.on_release)
fig.canvas.mpl_connect('motion_notify_event', mouse_nav.on_motion)

# Draw X and Y axes
ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)



#
# Show the plot
#plt.show()
opcao = None
layout = set_layout(opcao)
window = sg.Window('Matplotlib In PySimpleGUI', layout,finalize=True)
tkcanvas = draw_figure(window['-CANVAS-'].TKCanvas, fig)
#teste


while True:             # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    texto = verificaOpcao(values[1])
    window['campo1'].update(texto[0])
    window['campo2'].update(texto[1])
window.close()


#teste

# Create the window
#window = sg.Window('Matplotlib In PySimpleGUI', layout,finalize=True)

#tkcanvas = draw_figure(window['-CANVAS-'].TKCanvas, fig)
#event, values = window.read()

#layout = set_layout(values[1])




#window.close()

#print (values[1])	



