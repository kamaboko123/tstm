import tkinter as tk
from tkinter import ttk
import sys

class StackView(tk.Frame):
    def __init__(self, master, stm):
        super().__init__(master)

        self.stm = stm
        self.master.geometry("600x800")
        self.master.title("Stack View")
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
        self.master.attributes("-topmost", True)
        self.create_widgets()
        self.pack()
        
        self.sp_row = None

    def close_window(self):
        sys.exit(0)

    def create_widgets(self):
        self.pc = tk.Label(self)
        self.pc.pack()
        #self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        #self.canvas.pack()
        self.frame = tk.Frame()
        column = ("addr", "data", "sp", "bp")
        self.stview = ttk.Treeview(self.frame, columns=column, height=35)
        self.stview.column("#0", width=0, stretch="no")
        self.stview.column("addr", width=150, stretch="no")
        self.stview.column("data", width=300, stretch="no")
        self.stview.column("sp", width=60, stretch="no")
        self.stview.column("bp", width=60, stretch="no")
        self.stview.heading("#0", text="")
        self.stview.heading("addr", text="addr")
        self.stview.heading("data", text="data")
        self.stview.heading("sp", text="sp")
        self.stview.heading("bp", text="bp")

        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.stview.yview)
        self.stview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.stview.pack(pady=5)
        self.frame.pack()
        
        self.btn_goto_pc = tk.Button(self, text="Go to SP", command=self.goto_pc)
        self.btn_goto_pc.pack()
    
    def goto_pc(self, *args):
        if self.sp_row is not None:
            self.stview.see(self.sp_row)

    def update(self):
        self.pc["text"] = f"pc: %5d" % (self.stm.pc)

        self.stview.delete(*self.stview.get_children())
        for i in range(len(self.stm.stack)):
            sp = "<-" if self.stm.sp == i else ""
            bp = "<-" if self.stm.bp == i else ""
            row = self.stview.insert(parent="", index="end", values=(i,self.stm.stack[i], sp, bp))
            if self.stm.sp == i:
                self.sp_row = row
        
        super().update()
    
    def callback(self):
        pass

