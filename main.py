#!/usr/bin/env python3

import tkinter as tk
from tkinter import simpledialog
import os
from timer import Timer

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")

        # Initialize the UI elements
        self.add_timer_button = tk.Button(root, text="+ Add Timer", command=self.add_timer)
        self.add_timer_button.pack(pady=10)

        self.timers_frame = tk.Frame(root)
        self.timers_frame.pack(pady=20)

        # Set the common sound file path
        self.common_sound = os.path.join(os.path.dirname(__file__), 'assets', 'alarm.mp3')

    def add_timer(self):
        timer = Timer(self.timers_frame)
        timer.sound_file = self.common_sound

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
