
import matplotlib.pyplot as plt

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

