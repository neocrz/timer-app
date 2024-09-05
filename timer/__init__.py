import tkinter as tk
from tkinter import simpledialog, ttk
import threading
import time
import pygame

class Timer:
    def __init__(self, parent, title="Timer"):
        self.parent = parent
        self.title = title

        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10, fill=tk.X)

        self.title_var = tk.StringVar(value=self.title)
        self.title_label = tk.Label(self.frame, textvariable=self.title_var)
        self.title_label.pack()

        # Timer fields
        self.hours_var = tk.StringVar(value="0")
        self.minutes_var = tk.StringVar(value="0")
        self.seconds_var = tk.StringVar(value="0")

        self.hours_entry = ttk.Entry(self.frame, textvariable=self.hours_var, width=3)
        self.hours_entry.pack(side=tk.LEFT)
        tk.Label(self.frame, text="h").pack(side=tk.LEFT)

        self.minutes_entry = ttk.Entry(self.frame, textvariable=self.minutes_var, width=3)
        self.minutes_entry.pack(side=tk.LEFT)
        tk.Label(self.frame, text="m").pack(side=tk.LEFT)

        self.seconds_entry = ttk.Entry(self.frame, textvariable=self.seconds_var, width=3)
        self.seconds_entry.pack(side=tk.LEFT)
        tk.Label(self.frame, text="s").pack(side=tk.LEFT)

        self.time_label = tk.Label(self.frame, text="00:00:00")
        self.time_label.pack(pady=5)

        # Control buttons
        self.start_button = tk.Button(self.frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.frame, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.change_name_button = tk.Button(self.frame, text="Change Name", command=self.change_name)
        self.change_name_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.frame, text="-", command=self.delete)
        self.delete_button.pack(side=tk.RIGHT, padx=5)

        self.remaining_time = 0
        self.is_running = False
        self.thread = None
        self.paused_time = 0

        # Initialize pygame mixer
        pygame.mixer.init()

        # Variable to store the sound file path
        self.sound_file = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            if self.paused_time > 0:
                self.remaining_time = self.paused_time
            else:
                self.remaining_time = int(self.hours_var.get()) * 3600 + int(self.minutes_var.get()) * 60 + int(self.seconds_var.get())
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
        else:
            self.is_running = True
            self.paused_time = self.remaining_time
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def run(self):
        while self.is_running and self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            hours, mins = divmod(mins, 60)
            self.time_label.config(text=f"{hours:02}:{mins:02}:{secs:02}")
            time.sleep(1)
            self.remaining_time -= 1
        if self.remaining_time == 0:
            self.time_label.config(text="00:00:00")
            self.is_running = False
            self.play_sound()

    def play_sound(self):
        if self.sound_file:
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()

    def pause(self):
        self.is_running = False
        self.paused_time = self.remaining_time

    def reset(self):
        self.is_running = False
        self.paused_time = 0
        self.remaining_time = int(self.hours_var.get()) * 3600 + int(self.minutes_var.get()) * 60 + int(self.seconds_var.get())
        mins, secs = divmod(self.remaining_time, 60)
        hours, mins = divmod(mins, 60)
        self.time_label.config(text=f"{hours:02}:{mins:02}:{secs:02}")

    def delete(self):
        self.frame.destroy()

    def change_name(self):
        new_name = simpledialog.askstring("Change Name", "Enter new name:", initialvalue=self.title_var.get())
        if new_name:
            self.title_var.set(new_name)
