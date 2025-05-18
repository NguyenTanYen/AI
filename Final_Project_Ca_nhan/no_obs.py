import tkinter as tk
from tkinter import ttk, messagebox
import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance
from algorithms import no_observation_belief_state_search

class CuaSoNiemTinKhongQuanSat:
    def __init__(self, chuong_trinh):
        self.chuong_trinh = chuong_trinh
        self.cua_so = tk.Toplevel(chuong_trinh)
        self.cua_so.title("Tìm kiếm Niềm tin Không Quan sát")
        self.cua_so.geometry("1000x700")
        self.cua_so.resizable(True, True)
        self.cua_so.minsize(900, 700)

        phong_chu = ("Roboto", 12)
        phong_chu_dam = ("Roboto", 16, "bold")

        # Biến lưu trữ trạng thái
        self.trang_thai_ban_dau = []
        self.trang_thai_muc_tieu = []
        self.so_lan_lap_toi_da = tk.IntVar(value=1000)
        self.gioi_han_thoi_gian = tk.DoubleVar(value=10.0)
        self.duong_di = []
        self.buoc_hien_tai = 0
        self.dang_chay = False

        # Tiêu đề
        nhan_tieu_de = ttk.Label(self.cua_so, text="Tìm kiếm Niềm tin Không Quan sát", font=phong_chu_dam)
        nhan_tieu_de.pack(pady=10)

        # Frame chính để chứa ô nhập liệu và bảng 3x3
        khung_chinh = ttk.Frame(self.cua_so)
        khung_chinh.pack(fill="both", expand=True, padx=10)

        # Frame cho nhập liệu (bên trái)
        khung_nhap = ttk.Frame(khung_chinh)
        khung_nhap.pack(side="left", padx=10, pady=10, fill="y")

        # Nhập trạng thái ban đầu
        nhan_ban_dau = ttk.Label(khung_nhap, text="Trạng Thái Niềm Tin Ban Đầu (9 số, mỗi dòng):", font=phong_chu)
        nhan_ban_dau.pack(anchor="w", pady=5)
        self.o_nhap_ban_dau = tk.Text(khung_nhap, height=5, width=30, font=phong_chu)
        self.o_nhap_ban_dau.pack(pady=5)
        mac_dinh_ban_dau = ["123405678", "123450678", "120453678"]
        self.o_nhap_ban_dau.insert(tk.END, "\n".join(mac_dinh_ban_dau) + "\n")
        vi_du_ban_dau = ttk.Label(khung_nhap, text="Ví dụ: 123456078", font=phong_chu)
        vi_du_ban_dau.pack(anchor="w", pady=5)

        # Nhập trạng thái mục tiêu
        nhan_muc_tieu = ttk.Label(khung_nhap, text="Trạng Thái Niềm Tin Mục Tiêu (9 số, mỗi dòng):", font=phong_chu)
        nhan_muc_tieu.pack(anchor="w", pady=5)
        self.o_nhap_muc_tieu = tk.Text(khung_nhap, height=5, width=30, font=phong_chu)
        self.o_nhap_muc_tieu.pack(pady=5)
        mac_dinh_muc_tieu = ["123456780", "123456708"]
        self.o_nhap_muc_tieu.insert(tk.END, "\n".join(mac_dinh_muc_tieu) + "\n")
        vi_du_muc_tieu = ttk.Label(khung_nhap, text="Ví dụ: 123456780", font=phong_chu)
        vi_du_muc_tieu.pack(anchor="w", pady=5)

        # Nhập số lần lặp tối đa
        khung_lap = ttk.Frame(khung_nhap)
        khung_lap.pack(anchor="w", pady=5)
        nhan_lap = ttk.Label(khung_lap, text="Số Lần Lặp Tối Đa:", font=phong_chu)
        nhan_lap.pack(side="left", padx=5)
        o_lap = ttk.Entry(khung_lap, textvariable=self.so_lan_lap_toi_da, font=phong_chu, width=10)
        o_lap.pack(side="left")

        # Nhập giới hạn thời gian
        khung_thoi_gian = ttk.Frame(khung_nhap)
        khung_thoi_gian.pack(anchor="w", pady=5)
        nhan_thoi_gian = ttk.Label(khung_thoi_gian, text="Giới Hạn Thời Gian (giây):", font=phong_chu)
        nhan_thoi_gian.pack(side="left", padx=5)
        o_thoi_gian = ttk.Entry(khung_thoi_gian, textvariable=self.gioi_han_thoi_gian, font=phong_chu, width=10)
        o_thoi_gian.pack(side="left")

        # Frame cho bảng 3x3 và bảng mục tiêu (bên phải)
        khung_ban = ttk.Frame(khung_chinh)
        khung_ban.pack(side="right", padx=20, pady=10)
        self.taoBan(khung_ban)

        # Frame kết quả
        khung_ket_qua = ttk.Frame(khung_nhap)
        khung_ket_qua.pack(pady=10, fill="x")
        self.o_ket_qua = tk.Text(khung_ket_qua, height=10, width=50, font=phong_chu)
        self.o_ket_qua.pack(pady=5)

        # Frame các nút điều khiển
        khung_dieu_khien = ttk.Frame(self.cua_so)
        khung_dieu_khien.pack(pady=5, anchor="center")

        self.nut_khoi_dong = ttk.Button(khung_dieu_khien, text="Khởi động", command=self.khoiDongThuatToan)
        self.nut_khoi_dong.pack(side=tk.LEFT, padx=5)

        self.nut_buoc_tiep = ttk.Button(khung_dieu_khien, text="Bước tiếp", command=self.buocTiep, state=tk.DISABLED)
        self.nut_buoc_tiep.pack(side=tk.LEFT, padx=5)

        self.nut_tu_dong = ttk.Button(khung_dieu_khien, text="Tự động", command=self.chayTuDong, state=tk.DISABLED)
        self.nut_tu_dong.pack(side=tk.LEFT, padx=5)

        self.nut_lui = ttk.Button(khung_dieu_khien, text="Lùi lại", command=self.luiBuoc, state=tk.DISABLED)
        self.nut_lui.pack(side=tk.LEFT, padx=5)

        self.nut_dat_lai = ttk.Button(khung_dieu_khien, text="Đặt lại", command=self.datLai, state=tk.DISABLED)
        self.nut_dat_lai.pack(side=tk.LEFT, padx=5)

        # Nhãn thông tin bước
        self.nhan_thong_tin_buoc = tk.Label(self.cua_so, text="Nhấn 'Khởi động' để chạy thuật toán", font=phong_chu)
        self.nhan_thong_tin_buoc.pack(pady=5)

        self.nhan_so_buoc = tk.Label(self.cua_so, text="Tổng số bước: 0", font=phong_chu)
        self.nhan_so_buoc.pack(pady=5)

        self.nhan_buoc_hien_tai = tk.Label(self.cua_so, text="Bước hiện tại: 0", font=phong_chu)
        self.nhan_buoc_hien_tai.pack(pady=5)

        # Nút Đóng
        nut_dong = ttk.Button(self.cua_so, text="Đóng", command=self.cua_so.destroy)
        nut_dong.pack(pady=10)

    def taoBan(self, khung_cha):
        khung_ban = ttk.Frame(khung_cha)
        khung_ban.pack(pady=20)

        khung_luoi = ttk.Frame(khung_ban)
        khung_luoi.pack()

        self.o_vuong = []
        for i in range(3):
            hang = []
            for j in range(3):
                o = tk.Label(
                    khung_luoi,
                    text="",
                    font=("Roboto", 24, "bold"),
                    width=4,
                    height=2,
                    relief="raised",
                    bg="white"
                )
                o.grid(row=i, column=j, padx=2, pady=2)
                hang.append(o)
            self.o_vuong.append(hang)

        # Hiển thị trạng thái mục tiêu
        self.khung_muc_tieu = ttk.Frame(khung_cha)
        self.khung_muc_tieu.pack(pady=10)

        tk.Label(self.khung_muc_tieu, text="Mục tiêu:", font=("Roboto", 12)).pack()

        self.khung_luoi_muc_tieu = ttk.Frame(self.khung_muc_tieu)
        self.khung_luoi_muc_tieu.pack()

        for i in range(3):
            for j in range(3):
                tk.Label(
                    self.khung_luoi_muc_tieu,
                    text="",
                    font=("Roboto", 16),
                    width=4,
                    height=2,
                    relief="sunken"
                ).grid(row=i, column=j, padx=2, pady=2)

    def capNhatBan(self, trang_thai):
        if isinstance(trang_thai, list) and len(trang_thai) == 1 and all(isinstance(row, list) for row in trang_thai[0]):
            trang_thai = trang_thai[0]
        elif isinstance(trang_thai, str):
            trang_thai = [int(trang_thai[i * 3 + j]) for i in range(3) for j in range(3)]
            trang_thai = [trang_thai[i:i + 3] for i in range(0, 9, 3)]
        elif isinstance(trang_thai, list) and len(trang_thai) == 9 and all(isinstance(x, (int, str)) for x in trang_thai):
            trang_thai = [trang_thai[i:i + 3] for i in range(0, 9, 3)]

        if not (isinstance(trang_thai, list) and len(trang_thai) == 3 and all(len(row) == 3 for row in trang_thai)):
            self.nhan_thong_tin_buoc.config(text="Lỗi: Trạng thái không hợp lệ!")
            return

        for i in range(3):
            for j in range(3):
                value = trang_thai[i][j] if trang_thai[i][j] != 0 else ""
                self.o_vuong[i][j].config(text=str(value), bg="white")

        if hasattr(self, 'trang_thai_muc_tieu_2d') and self.trang_thai_muc_tieu_2d is not None:
            for i in range(3):
                for j in range(3):
                    if trang_thai[i][j] == 0:
                        self.o_vuong[i][j].config(bg="lightgray")
                    elif trang_thai[i][j] == self.trang_thai_muc_tieu_2d[i][j]:
                        self.o_vuong[i][j].config(bg="lightgreen")
                    else:
                        self.o_vuong[i][j].config(bg="lightyellow")

    def capNhatBanMucTieu(self, trang_thai_muc_tieu):
        if isinstance(trang_thai_muc_tieu, list) and len(trang_thai_muc_tieu) == 1 and all(isinstance(row, list) for row in trang_thai_muc_tieu[0]):
            trang_thai_muc_tieu = trang_thai_muc_tieu[0]
        elif isinstance(trang_thai_muc_tieu, str):
            trang_thai_muc_tieu = [int(trang_thai_muc_tieu[i * 3 + j]) for i in range(3) for j in range(3)]
            trang_thai_muc_tieu = [trang_thai_muc_tieu[i:i + 3] for i in range(0, 9, 3)]
        elif isinstance(trang_thai_muc_tieu, list) and len(trang_thai_muc_tieu) == 9 and all(isinstance(x, (int, str)) for x in trang_thai_muc_tieu):
            trang_thai_muc_tieu = [trang_thai_muc_tieu[i:i + 3] for i in range(0, 9, 3)]

        if not (isinstance(trang_thai_muc_tieu, list) and len(trang_thai_muc_tieu) == 3 and all(len(row) == 3 for row in trang_thai_muc_tieu)):
            return

        self.trang_thai_muc_tieu_2d = trang_thai_muc_tieu
        for i in range(3):
            for j in range(3):
                value = trang_thai_muc_tieu[i][j] if trang_thai_muc_tieu[i][j] != 0 else ""
                self.khung_luoi_muc_tieu.grid_slaves(row=i, column=j)[0].config(text=str(value))

    def phanTichTrangThai(self, van_ban):
        trang_thai = []
        dong = van_ban.splitlines()
        for d in dong:
            if not d.strip():
                continue
            try:
                sach_se = d.replace(' ', '')
                if len(sach_se) != 9 or not all(c in '012345678' for c in sach_se):
                    raise ValueError("Định dạng trạng thái không hợp lệ")
                trang_thai.append(sach_se)
            except ValueError as e:
                messagebox.showerror("Lỗi", f"Đầu vào không hợp lệ: {e}")
                return None
        return trang_thai if trang_thai else None

    def khoiDongThuatToan(self):
        self.o_ket_qua.delete(1.0, tk.END)
        self.duong_di = []
        self.buoc_hien_tai = 0

        trang_thai_ban_dau = self.phanTichTrangThai(self.o_nhap_ban_dau.get(1.0, tk.END))
        trang_thai_muc_tieu = self.phanTichTrangThai(self.o_nhap_muc_tieu.get(1.0, tk.END))

        if not trang_thai_ban_dau or not trang_thai_muc_tieu:
            messagebox.showerror("Lỗi", "Vui lòng nhập trạng thái ban đầu và mục tiêu hợp lệ.")
            return

        self.trang_thai_ban_dau = trang_thai_ban_dau
        self.trang_thai_muc_tieu = trang_thai_muc_tieu

        thuat_toan = no_observation_belief_state_search.NoObservationBeliefStateSearchAlgorithm()
        duong_di, chi_phi, bo_dem, do_sau, thoi_gian_chay, tong_khong_gian = thuat_toan.NoObsBeliefStateSearch(
            trang_thai_ban_dau, trang_thai_muc_tieu,
            max_iterations=self.so_lan_lap_toi_da.get(),
            time_limit=self.gioi_han_thoi_gian.get()
        )

        self.o_ket_qua.insert(tk.END, f"Thời Gian Thực Thi: {thoi_gian_chay:.2f} giây\n")
        self.o_ket_qua.insert(tk.END, f"Chi Phí (Số Bước): {chi_phi}\n")
        self.o_ket_qua.insert(tk.END, f"Số Trạng Thái Khám Phá: {bo_dem}\n")
        self.o_ket_qua.insert(tk.END, f"Độ Sâu: {do_sau}\n")
        self.o_ket_qua.insert(tk.END, f"Tổng Không Gian Sử Dụng: {tong_khong_gian} nút\n")
        self.o_ket_qua.insert(tk.END, "\nĐường Đi:\n")
        for i, buoc in enumerate(duong_di):
            self.o_ket_qua.insert(tk.END, f"Bước {i}:\n")
            for hang in buoc[0] if isinstance(buoc, list) and len(buoc) == 1 else buoc:
                self.o_ket_qua.insert(tk.END, str(hang) + "\n")
            self.o_ket_qua.insert(tk.END, "\n")

        if not duong_di:
            self.o_ket_qua.insert(tk.END, "Không tìm thấy giải pháp trong giới hạn cho phép.\n")
            self.nhan_thong_tin_buoc.config(text="Không tìm thấy giải pháp!")
            return

        # Chuẩn hóa đường đi thành list các trạng thái 2D
        self.duong_di = []
        for buoc in duong_di:
            if isinstance(buoc, list) and len(buoc) == 1 and all(isinstance(hang, list) for hang in buoc[0]):
                self.duong_di.append(buoc[0])
            else:
                self.duong_di.append(buoc)

        self.nhan_so_buoc.config(text=f"Tổng số bước: {len(self.duong_di)}")
        self.nhan_thong_tin_buoc.config(text="Đã tìm thấy giải pháp! Nhấn 'Bước tiếp' hoặc 'Tự động' để xem.")
        self.buoc_hien_tai = 1
        self.capNhatBan(self.duong_di[0])
        if len(self.duong_di) > 1:
            self.capNhatBanMucTieu(self.duong_di[-1])
        self.nhan_buoc_hien_tai.config(text=f"Bước hiện tại: {self.buoc_hien_tai}")
        self.nut_buoc_tiep.config(state=tk.NORMAL)
        self.nut_tu_dong.config(state=tk.NORMAL)
        self.nut_dat_lai.config(state=tk.NORMAL)
        self.nut_lui.config(state=tk.DISABLED)
        self.dang_chay = False
        self.nut_tu_dong.config(text="Tự động")

    def buocTiep(self):
        if self.buoc_hien_tai < len(self.duong_di):
            self.buoc_hien_tai += 1
            self.capNhatBan(self.duong_di[self.buoc_hien_tai - 1])
            self.nhan_buoc_hien_tai.config(text=f"Bước hiện tại: {self.buoc_hien_tai}")
            self.nut_lui.config(state=tk.NORMAL)
            if self.buoc_hien_tai == len(self.duong_di):
                self.nut_buoc_tiep.config(state=tk.DISABLED)
                self.nhan_thong_tin_buoc.config(text="Đã hoàn thành đường đi!")
                messagebox.showinfo("Thông báo", "Đã hoàn thành đường đi!")

    def luiBuoc(self):
        if self.buoc_hien_tai > 1:
            self.buoc_hien_tai -= 1
            self.capNhatBan(self.duong_di[self.buoc_hien_tai - 1])
            self.nhan_buoc_hien_tai.config(text=f"Bước hiện tại: {self.buoc_hien_tai}")
            self.nut_buoc_tiep.config(state=tk.NORMAL)
            if self.buoc_hien_tai == 1:
                self.nut_lui.config(state=tk.DISABLED)

    def chayTuDong(self):
        if not self.dang_chay:
            self.dang_chay = True
            self.nut_tu_dong.config(text="Dừng lại")
            self.nut_buoc_tiep.config(state=tk.DISABLED)
            self.nut_lui.config(state=tk.DISABLED)
            self.hieuUng()
        else:
            self.dang_chay = False
            self.nut_tu_dong.config(text="Tự động")
            if self.buoc_hien_tai < len(self.duong_di):
                self.nut_buoc_tiep.config(state=tk.NORMAL)
            if self.buoc_hien_tai > 1:
                self.nut_lui.config(state=tk.NORMAL)

    def hieuUng(self):
        if self.buoc_hien_tai < len(self.duong_di) and self.dang_chay:
            self.buoc_hien_tai += 1
            self.capNhatBan(self.duong_di[self.buoc_hien_tai - 1])
            self.nhan_buoc_hien_tai.config(text=f"Bước hiện tại: {self.buoc_hien_tai}")
            self.cua_so.after(500, self.hieuUng)
        elif self.dang_chay:
            self.dang_chay = False
            self.nut_tu_dong.config(text="Tự động")
            self.nhan_thong_tin_buoc.config(text="Đã hoàn thành đường đi!")
            messagebox.showinfo("Thông báo", "Đã hoàn thành đường đi!")
            if self.buoc_hien_tai > 1:
                self.nut_lui.config(state=tk.NORMAL)

    def datLai(self):
        self.buoc_hien_tai = 1
        if self.duong_di:
            self.capNhatBan(self.duong_di[0])
            if len(self.duong_di) > 1:
                self.capNhatBanMucTieu(self.duong_di[-1])
        self.nhan_buoc_hien_tai.config(text=f"Bước hiện tại: {self.buoc_hien_tai}")
        self.nut_buoc_tiep.config(state=tk.NORMAL)
        self.nut_tu_dong.config(state=tk.NORMAL)
        self.nut_lui.config(state=tk.DISABLED)
        self.dang_chay = False
        self.nut_tu_dong.config(text="Tự động")
        self.nhan_thong_tin_buoc.config(text="Đã đặt lại! Nhấn 'Bước tiếp' hoặc 'Tự động' để xem lại.")

    def moCuaSoNiemTinKhongQuanSat(self, su_kien=None):
        self.cua_so.deiconify()

if __name__ == "__main__":
    goc = tk.Tk()
    ung_dung = CuaSoNiemTinKhongQuanSat(goc)
    goc.mainloop()
