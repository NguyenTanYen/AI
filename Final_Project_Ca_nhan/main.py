import tkinter as tk
from GUI import GiaoDien


if __name__ == "__main__":
    root = tk.Tk()
    app = GiaoDien(chuong_trinh=root)
    root.mainloop()  