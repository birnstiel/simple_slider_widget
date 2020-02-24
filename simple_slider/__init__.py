import matplotlib.pyplot as plt
import matplotlib.widgets as w
import numpy as np
import pkg_resources

# Get the data

data_fname = pkg_resources.resource_filename(__name__, 'data.dat')
data = np.loadtxt(data_fname)


class Widget():

    def __init__(self):
        """
        Initialize the widget: draw model and data
        """

        # Make the figure

        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0.1, 0.3, 0.5, 0.6])

        # plot the reference profile

        self.data_line, = self.ax.plot(data[:, 0], data[:, 1], 'k-')

        # CREATE SLIDER(S)

        slider_x0 = self.ax.get_position().x0
        slider_y0 = 0.05
        slider_w  = self.ax.get_position().width
        slider_h  = 0.04

        # slider for parameter A

        self._ax_A = self.fig.add_axes([slider_x0, slider_y0, slider_w, slider_h], facecolor="lightgoldenrodyellow")
        self._slider_A = w.Slider(self._ax_A, "A", -2, 2, valinit=0, valfmt='%i')
        self._ax_A.set_title("A = {:9.3e}".format(self._slider_A.val), fontsize='small')
        self._slider_A.on_changed(self.update)

        self.model_line, = self.ax.plot(data[:, 0], np.ones_like(data[:, 0]))

        # call the callback function once to make the plot agree with state of the buttons

        self.update(None)

    def update(self, event):
        """
        The callback for updating the figure when the sliders are moved
        """

        # calculate our toy model
        model = data[:, 0]**(-self._slider_A.val)

        self.model_line.set_ydata(model)
        plt.draw()


def main():
    _ = Widget()
    plt.show()


if __name__ == '__main__':
    main()
