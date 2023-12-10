import random
import tkinter as tk
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
canvas = None

def cplot():
    global canvas
    xCord = [random.randint(0,10) for i in range(5)]
    yCord = [random.randint(0,10) for i in range(5)]

    #defining heatmap dimensions
    fig, ax = plt.subplots()

    #ploting heat map with x and y coordinates
    sb.kdeplot(xCord, yCord, shade = True, cmap = "Reds")
    ax.invert_yaxis()
    plt.axis("off")
    
    if canvas: canvas.get_tk_widget().pack_forget()  # remove previous image
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    root.after(100, cplot)
        
root.after(1, cplot)
root.mainloop()