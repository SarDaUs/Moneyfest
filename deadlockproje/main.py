import tkinter as tk

from gui import DeadlockSimulatorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockSimulatorApp(root)
    root.mainloop()
