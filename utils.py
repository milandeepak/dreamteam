import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mediapipe.tasks.python import audio
import RPi.GPIO as GPIO  # Import GPIO library

class Plotter(object):
    """A utility class to display the classification results."""

    _PAUSE_TIME = 0.05  # Time for matplotlib to wait for UI event.

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Audio classification')
        self.root.bind('<Escape>', self.close_window)

        self.motor_label = tk.Label(self.root, text="Motor status: Stopped")
        self.motor_label.pack()

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

        # Update motor status
        motor_running = False
        for category in classification.categories:
            if category.category_name == '1 Crying' and category.score > 0.8:
                motor_running = True
                break

        if motor_running:
            self.motor_label.config(text="Motor status: Running")
            self.turn_servo()  # Call turn_servo if motor is running
            # Schedule to change the label after 20 seconds
            self.root.after(20000, self.set_motor_stopped)
        else:
            self.motor_label.config(text="Motor status: Stopped")

        # Draw the plot
        self.canvas.draw()

    def set_motor_stopped(self):
        """Change motor status label to Stopped after 20 seconds."""
        self.motor_label.config(text="Motor status: Stopped")

    def close_window(self, event=None):
        """Close the window."""
        GPIO.cleanup()  # Cleanup GPIO pins before closing
        self.root.quit()

    def turn_servo(self):
        """Turn the servo motor."""
        # in3 = 23
        # in4 = 24
        # en = 25
        # temp1=1

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(in3,GPIO.OUT)
        # GPIO.setup(in4,GPIO.OUT)
        # GPIO.setup(en,GPIO.OUT)
        # GPIO.output(in3,GPIO.LOW)
        # GPIO.output(in4,GPIO.LOW)
        # p=GPIO.PWM(en,1000)
        # p.start(25)

        # GPIO.output(in3,GPIO.HIGH)
        # GPIO.output(in4,GPIO.LOW)
        print("The motor is running")

def main():
    plotter = Plotter()

    # Simulate classification results (replace this with actual data)
    result = audio.AudioClassifierResult()
    result.classifications.append(audio.ClassificationResult())
    result.classifications[0].categories.append(audio.Classification())
    result.classifications[0].categories[0].category_name = 'Speech'
    result.classifications[0].categories[0].score = 0.8
    result.classifications[0].categories.append(audio.Classification())
    result.classifications[0].categories[1].category_name = '1 Crying'
    result.classifications[0].categories[1].score = 0.95  # Example score above 0.9

    plotter.plot(result)
    plotter.root.mainloop()

if __name__ == '__main__':
    main()
