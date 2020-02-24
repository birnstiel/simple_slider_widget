import matplotlib.pyplot as plt
import matplotlib.widgets as w
import numpy as np
import pkg_resources
import argparse
# import os


class Widget():

    def __init__(self, fname=None):
        """
        Initialize the widget to compare model and data

        fname : str
            file name to the data file
        """

        # Get the data

        if fname is None:
            fname = pkg_resources.resource_filename(__name__, 'data.dat')

        data = np.loadtxt(fname)
        self.data = data

        # self.r     = np.loadtxt(os.path.join(fname, 'radius.dat'))
        # self.sigma = np.loadtxt(os.path.join(fname, 'sigma_averaged.dat'))
        # self.t     = np.loadtxt(os.path.join(fname, 'time.dat'))

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
        self._slider_A = w.Slider(self._ax_A, "A", -2, 2, valinit=0, valfmt='%.1f')
        self._ax_A.set_title("A", fontsize='small')
        self._slider_A.on_changed(self.update)

        self.model_line, = self.ax.plot(data[:, 0], np.ones_like(data[:, 0]))

        # call the callback function once to make the plot agree with state of the buttons

        self.update(None)

    def update(self, event):
        """
        The callback for updating the figure when the sliders are moved
        """

        # calculate our toy model

        model = self.data[:, 0]**(-self._slider_A.val)

        # update the model line

        self.model_line.set_ydata(model)

        # update our slider title

        self._ax_A.set_title("$y = x^{{{:.1f}}}$".format(-self._slider_A.val), fontsize='small')

        plt.draw()


def main():

    RTHF   = argparse.RawTextHelpFormatter
    PARSER = argparse.ArgumentParser(description='Widget to test planetary gap profiles', formatter_class=RTHF)
    PARSER.add_argument('-d', '--data-path', help='path to the data files', type=str, default=None)
    ARGS  = PARSER.parse_args()

    _ = Widget(fname=ARGS.data_path)
    plt.show()


if __name__ == '__main__':
    main()
