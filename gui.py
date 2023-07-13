import tkinter as tk
import sys

class StackView(tk.Frame):
    def __init__(self, master, stm):
        super().__init__(master)
        self.pack()

        self.stm = stm
        self.master.geometry("640x480")
        self.master.title("Stack View")
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
        self.create_widgets()

    def close_window(self):
        sys.exit(0)

    def create_widgets(self):
        self.pc = tk.Label(self, text=f"{self.stm.pc}")
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        self.pc.pack()
        self.canvas.pack()

    def update(self):
        self.canvas.delete("all")
        
        self.pc["text"] = f"{self.stm.pc}"

        self.canvas.update()
        super().update()
    
    def callback(self):
        pass

