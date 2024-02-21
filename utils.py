import sys
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Add this import
from mediapipe.tasks.python import audio

class Plotter(object):
    """A utility class to display the classification results."""

    _PAUSE_TIME = 0.05  # Time for matplotlib to wait for UI event.

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Audio classification')
        self.root.bind('<Escape>', self.close_window)

        self.figure, self._axes = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def plot(self, result: audio.AudioClassifierResult):
        """Plot the audio classification result."""
        # Clear the axes
        self._axes.clear()
        self._axes.set_title('Press ESC to exit.')
        self._axes.set_xlim((0, 1))

        # Plot the results so that the most probable category comes at the top.
        classification = result.classifications[0]
        label_list = [category.category_name for category in classification.categories]
        score_list = [category.score for category in classification.categories]
        self._axes.barh(label_list[::-1], score_list[::-1])

        # Draw the plot
        self.canvas.draw()

    def close_window(self, event=None):
        """Close the window."""
        self.root.quit()

def main():
    plotter = Plotter()

    # Simulate classification results (replace this with actual data)
    result = audio.AudioClassifierResult()
    result.classifications.append(audio.ClassificationResult())
    result.classifications[0].categories.append(audio.Classification())
    result.classifications[0].categories[0].category_name = 'Speech'
    result.classifications[0].categories[0].score = 0.8
    result.classifications[0].categories.append(audio.Classification())
    result.classifications[0].categories[1].category_name = 'Music'
    result.classifications[0].categories[1].score = 0.2

    plotter.plot(result)
    plotter.root.mainloop()

if __name__ == '__main__':
    main()
