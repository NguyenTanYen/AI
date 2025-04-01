import time
from collections import deque
import tkinter as tk
from tkinter import messagebox

def tim_o_trong(trang_thai):
    for i, hang in enumerate(trang_thai):
        if 0 in hang:
            return i, hang.index(0)

def di_chuyen_o_trong(trang_thai, di, dj):
    i, j = tim_o_trong(trang_thai)
    ni, nj = i + di, j + dj
    if 0 <= ni < 3 and 0 <= nj < 3:
        trang_thai_moi = [hang[:] for hang in trang_thai]
        trang_thai_moi[i][j], trang_thai_moi[ni][nj] = trang_thai_moi[ni][nj], trang_thai_moi[i][j]
        return trang_thai_moi
    return None

def tim_loi_giai_bfs(trang_thai_ban_dau, dich):
    hang_doi = deque([(trang_thai_ban_dau, [])])
    da_xet = set()
    huong_di_chuyen = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while hang_doi:
        trang_thai_hien_tai, duong_di = hang_doi.popleft()
        if trang_thai_hien_tai == dich:
            return duong_di + [trang_thai_hien_tai]
        
        da_xet.add(tuple(map(tuple, trang_thai_hien_tai)))
        for di, dj in huong_di_chuyen:
            trang_thai_moi = di_chuyen_o_trong(trang_thai_hien_tai, di, dj)
            if trang_thai_moi and tuple(map(tuple, trang_thai_moi)) not in da_xet:
                hang_doi.append((trang_thai_moi, duong_di + [trang_thai_hien_tai]))
    return None 

class GiaoDienPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Trình Giải 8-Puzzle")
        self.trang_thai_dich = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.buoc_hien_tai = 0

        self.center_window(600, 400)

        self.o_nhap = []
        tk.Label(root, text="Nhập trạng thái ban đầu (0 là ô trống):", font=("Arial", 14)).pack()
        for i in range(3):
            hang = []
            khung = tk.Frame(root)
            khung.pack()
            for j in range(3):
                o = tk.Entry(khung, width=3, justify="center", font=("Arial", 14))
                o.grid(row=i, column=j, padx=5, pady=5)
                hang.append(o)
            self.o_nhap.append(hang)
        
        self.nut_giai = tk.Button(root, text="Giải bài toán", command=self.giai_puzzle, bg="lightblue", font=("Arial", 12))
        self.nut_giai.pack(pady=10)
        
        self.khung_ket_qua = tk.Frame(root)
        self.khung_ket_qua.pack(expand=True, anchor="center")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def lay_du_lieu(self):
        try:
            trang_thai_ban_dau = []
            for hang in self.o_nhap:
                trang_thai_ban_dau.append([int(o.get()) for o in hang])
            return trang_thai_ban_dau
        except ValueError:
            messagebox.showerror("Lỗi", "Hãy nhập các số nguyên từ 0 đến 8.")
            return None

    def hien_buoc_tiep_theo(self, loi_giai):
        if self.buoc_hien_tai < len(loi_giai):
            trang_thai = loi_giai[self.buoc_hien_tai]
            for widget in self.khung_ket_qua.winfo_children():
                widget.destroy()

            for hang in trang_thai:
                tk.Label(self.khung_ket_qua, text=" ".join(str(so) if so != 0 else " " for so in hang),
                         font=("Consolas", 16), pady=5).pack(anchor="center")
            
            self.buoc_hien_tai += 1
            self.root.after(1000, self.hien_buoc_tiep_theo, loi_giai)

    def giai_puzzle(self):
        trang_thai_ban_dau = self.lay_du_lieu()
        if not trang_thai_ban_dau:
            return
        
        if sorted(sum(trang_thai_ban_dau, [])) != list(range(9)):
            messagebox.showerror("Lỗi", "Trạng thái không hợp lệ! Các số phải từ 0 đến 8, không lặp lại.")
            return
        
        messagebox.showinfo("Đang tìm kiếm...", "Hệ thống đang tìm kiếm giải pháp. Vui lòng đợi!")
        loi_giai = tim_loi_giai_bfs(trang_thai_ban_dau, self.trang_thai_dich)

        if loi_giai:
            self.buoc_hien_tai = 0  
            self.hien_buoc_tiep_theo(loi_giai)
        else:
            messagebox.showinfo("Không tìm thấy", "Không tìm thấy lời giải cho trạng thái ban đầu này.")

def main():
    root = tk.Tk()
    app = GiaoDienPuzzle(root)
    root.mainloop()

if __name__ == "__main__":
    main()
