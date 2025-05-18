import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
import random
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import seaborn as sns

from backtracking import CuaSoBacktracking
from partially import CuaSoNiemTinQuanSatMotPhan
from no_obs import CuaSoNiemTinKhongQuanSat
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import AI

from algorithms import (
    bfs,
    dfs,
    greed_best_first_search,
    ucs,
    ids,
    astar,
    idastar,
    simple_hill_climbing,
    stochastic_hill_climbing,
    simulated_annealing,
    beam_search,
    genetic_search,
    and_or_graph_search,
    belief_state_search,
    backtracking,
    q_learning,
    no_observation_belief_state_search,
    partially_observable_search,
)


class GiaoDien:
    def __init__(self, chuong_trinh=None):
        self.chuong_trinh = chuong_trinh
        self.thuat_toan = None
        self.trang_thai_ban_dau = None
        self.con_tro_trang_thai = 0
        self.chi_phi = 0
        self.bo_dem = 0
        self.do_sau = 0
        self.thoi_gian_chay = 0.0
        self.duong_di = []
        self.kich_thuoc_bo_nho = 0
        self.du_lieu_thoi_gian_chay = {}
        self.cong_viec = None
        self.khung_ung_dung = ttk.Frame(chuong_trinh)
        self.khung_ung_dung.configure(height=800, width=1000)
        self.khung_ung_dung.pack(side="top", fill="both", expand=True)
        self.nhan_chinh = ttk.Label(self.khung_ung_dung)

        chieu_rong_man_hinh = self.chuong_trinh.winfo_screenwidth()
        chieu_cao_man_hinh = self.chuong_trinh.winfo_screenheight()

        chieu_rong_cua_so = 1000
        chieu_cao_cua_so = 800

        vi_tri_x = (chieu_rong_man_hinh - chieu_rong_cua_so) // 2
        vi_tri_y = (chieu_cao_man_hinh - chieu_cao_cua_so) // 2

        self.chuong_trinh.geometry(f"{chieu_rong_cua_so}x{chieu_cao_cua_so}+{vi_tri_x}+{vi_tri_y}")

        self.nhan_chinh.configure(
            anchor="center",
            font="{Roboto} 36 {bold}",
            foreground="#003e3e",
            justify="center",
            text="Giải 8-Puzzle",
        )
        self.nhan_chinh.place(anchor="center", x=500, y=50)

        # Khung nội dung chính
        self.khung_noi_dung = ttk.Frame(self.khung_ung_dung)
        self.khung_noi_dung.pack(fill="both", expand=True, padx=20, pady=10)

        # Bảng điều khiển bên trái - Bảng puzzle
        self.bang_trai = ttk.Frame(self.khung_noi_dung)
        self.bang_trai.pack(side="left", fill="both", expand=True, padx=10)

        # Tạo lưới puzzle
        self.taoLuoiPuzzle()

        # Bảng điều khiển bên phải - Điều khiển
        self.bang_phai = ttk.Frame(self.khung_noi_dung)
        self.bang_phai.pack(side="right", fill="both", padx=10)

        # Chọn thuật toán
        self.nhan_thuat_toan = ttk.Label(self.bang_phai, text="Chọn thuật toán:")
        self.nhan_thuat_toan.pack(pady=5)

        self.hop_thuat_toan = ttk.Combobox(
            self.bang_phai,
            state="readonly",
            values=(
                "BFS",
                "DFS",
                "Uniform Cost Search",
                "Iterative Deepening",
                "Greed Best First Search",
                "A*",
                "IDA*",
                "Simple Hill Climbing",
                "Stochastic Hill Climbing",
                "Simulated Annealing",
                "Beam Search",
                "Genetic Search",
                "AND OR Graph Search",
                "QLearning",
            )
        )
        self.hop_thuat_toan.pack(pady=5)
        self.hop_thuat_toan.bind("<<ComboboxSelected>>", self.chonThuatToan)

        # Các nút điều khiển
        self.taoNutDieuKhien()

        # Hộp phân tích
        self.hop_phan_tich = ttk.Label(
            self.bang_phai,
            text="",
            background="#f5f5f5",
            borderwidth=2,
            relief="sunken",
            wraplength=200
        )
        self.hop_phan_tich.pack(pady=10, fill="x")

        # Bộ đếm bước
        self.dem_buoc = ttk.Label(
            self.bang_phai,
            text="0 / 0",
            background="#f5f5f5",
            font=("Arial", 12)
        )
        self.dem_buoc.pack(pady=5)

        # Các nút điều hướng
        self.taoNutDieuHuong()

        # Khởi tạo trạng thái puzzle
        self.hienThiTrangThaiTrenLuoi("000000000")

        self.cua_so_chinh = self.khung_ung_dung

        # Thêm các nút cho các tính năng bổ sung
        self.taoNutTinhNangBoSung()

    def taoNutDieuHuong(self):
        # Khung các nút điều hướng
        khung_dieu_huong = ttk.Frame(self.bang_phai)
        khung_dieu_huong.pack(pady=10)

        # Nút trước
        self.nut_lui = ttk.Button(
            khung_dieu_huong,
            text="Trước",
            command=self.luiDay
        )
        self.nut_lui.pack(side="left", padx=5)

        # Nút tiếp
        self.nut_tiep = ttk.Button(
            khung_dieu_huong,
            text="Tiếp",
            command=self.tiepDay
        )
        self.nut_tiep.pack(side="left", padx=5)

        # Nút lùi nhanh
        self.nut_lui_nhanh = ttk.Button(
            khung_dieu_huong,
            text="Lùi nhanh",
            command=self.luiNhanh
        )
        self.nut_lui_nhanh.pack(side="left", padx=5)

        # Nút tiến nhanh
        self.nut_tien_nhanh = ttk.Button(
            khung_dieu_huong,
            text="Tiến nhanh",
            command=self.tienNhanh
        )
        self.nut_tien_nhanh.pack(side="left", padx=5)

        # Nút dừng
        self.nut_dung = ttk.Button(
            khung_dieu_huong,
            text="Dừng",
            command=self.dungTienNhanh,
            state="disabled"
        )
        self.nut_dung.pack(side="left", padx=5)

        # Nút đặt lại
        self.nut_dat_lai = ttk.Button(
            khung_dieu_huong,
            text="Đặt lại",
            command=self.datLaiBoDemBuoc,
            state="disabled"
        )
        self.nut_dat_lai.pack(side="left", padx=5)

    def taoNutTinhNangBoSung(self):
        # Khung cho các nút tính năng bổ sung
        khung_bo_sung = ttk.Frame(self.bang_phai)
        khung_bo_sung.pack(pady=10)

        # Nút niềm tin không quan sát
        #self.nut_khong_quan_sat = ttk.Button(
        #   khung_bo_sung,
        #   text="Niềm tin không quan sát",
        #  command=self.cuaSoNiemTinKhongQuanSat
        #)
        #self.nut_khong_quan_sat.pack(pady=5)

        # Nút niềm tin quan sát một phần
        self.nut_quan_sat_mot_phan = ttk.Button(
            khung_bo_sung,
            text="Niềm tin quan sát một phần",
            command=self.cuaSoNiemTinQuanSatMotPhan
        )
        self.nut_quan_sat_mot_phan.pack(pady=5)

        # Nút backtracking
        self.nut_backtracking = ttk.Button(
            khung_bo_sung,
            text="Backtracking",
            command=self.moCuaSoBacktracking
        )
        self.nut_backtracking.pack(pady=5)

    def hienThiPhanTichTimKiem(self, bat_buoc_hien_thi=False):
        if self.daGiai() or bat_buoc_hien_thi is True:
            phan_tich = (
                "Thuật toán:"
                + str(self.thuat_toan)
                + "\nTrạng thái bắt đầu:"
                + str(self.trang_thai_ban_dau)
            )
            if bat_buoc_hien_thi:
                phan_tich += "\n< Không thể giải >"
            phan_tich += (
                "\n"
                + "Số trạng thái đã duyệt: "
                + str(self.bo_dem)
                + "\n"
                + "Độ sâu: "
                + str(self.do_sau)
                + "\n"
                + "Chi phí: "
                + str(self.chi_phi)
                + "\n"
                + "Thời gian chạy: "
                + str(self.thoi_gian_chay)
                + " s"
                + "\nKích thước bộ nhớ: "
                + str(self.kich_thuoc_bo_nho)
            )
        else:
            phan_tich = ""
        self.hop_phan_tich.configure(text=phan_tich)

    def chay(self):
        self.hienThiTrangThaiTrenLuoi("000000000")
        self.lamMoiKhung()
        self.cua_so_chinh.mainloop()

    # ------------ Chức năng của các nút ---------------

    def luiDay(self, su_kien=None):
        if self.con_tro_trang_thai > 0:
            self.dungTienNhanh()
            self.con_tro_trang_thai -= 1
            self.lamMoiKhung()

    def chonThuatToanTuCay(self, su_kien=None):
        muc_duoc_chon = self.cay_thuat_toan.selection()[0]
        thuat_toan = self.cay_thuat_toan.item(muc_duoc_chon, "text")
        if thuat_toan not in ["Uninformed Search", "Informed Search", "Local Search", "Non-deterministic Search"]:
            self.thuat_toan = thuat_toan
            self.datLai()

    def cuaSoNiemTinQuanSatMotPhan(self, su_kien=None):
        CuaSoNiemTinQuanSatMotPhan(self.chuong_trinh)

    def cuaSoNiemTinKhongQuanSat(self, su_kien=None):
        CuaSoNiemTinKhongQuanSat(self.chuong_trinh)

    def moCuaSoBacktracking(self, su_kien=None):
        CuaSoBacktracking(self.chuong_trinh)

    def taoBanBacktracking(self, cua_so):
        # Tạo khung chính cho bảng
        khung_ban = ttk.Frame(cua_so)
        khung_ban.pack(pady=20)

        # Tạo khung riêng cho bảng 3x3
        khung_luoi = ttk.Frame(khung_ban)
        khung_luoi.pack()

        self.o_backtracking = []
        for i in range(3):
            hang = []
            for j in range(3):
                o = tk.Label(
                    khung_luoi,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2,
                    relief="raised",
                    bg="white"
                )
                o.grid(row=i, column=j, padx=2, pady=2)
                hang.append(o)
            self.o_backtracking.append(hang)

        # Tạo khung riêng cho mục tiêu
        khung_muc_tieu = ttk.Frame(cua_so)
        khung_muc_tieu.pack(pady=10)

        tk.Label(khung_muc_tieu, text="Mục tiêu:", font=("Arial", 12)).pack()

        # Tạo khung riêng cho bảng mục tiêu
        khung_luoi_muc_tieu = ttk.Frame(khung_muc_tieu)
        khung_luoi_muc_tieu.pack()

        trang_thai_muc_tieu = [1,2,3,4,5,6,7,8,0]
        for i in range(3):
            for j in range(3):
                chi_so = i*3 + j
                gia_tri = trang_thai_muc_tieu[chi_so] if trang_thai_muc_tieu[chi_so] != 0 else ""
                tk.Label(
                    khung_luoi_muc_tieu,
                    text=str(gia_tri),
                    font=("Arial", 16),
                    width=4,
                    height=2,
                    relief="sunken"
                ).grid(row=i, column=j, padx=2, pady=2)

    def batDauBacktracking(self, cua_so):
        # Khởi tạo trạng thái ban đầu (rỗng)
        trang_thai_ban_dau = [0]*9
        self.giai_phap_backtracking = []
        self.buoc_hien_tai = 0

        # Tìm giải pháp
        if self.giaiBacktracking(trang_thai_ban_dau, 0):
            self.cac_buoc_backtracking = self.giai_phap_backtracking.copy()
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[0])
            self.nut_buoc.config(state=tk.NORMAL)
            self.nut_tu_dong.config(state=tk.NORMAL)
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp")

    def giaiBacktracking(self, trang_thai, vi_tri):
        if vi_tri == 9:
            return True

        gia_tri_mong_muon = vi_tri + 1 if vi_tri < 8 else 0

        if trang_thai[vi_tri] == gia_tri_mong_muon:
            return self.giaiBacktracking(trang_thai, vi_tri + 1)

        if trang_thai[vi_tri] != 0:
            return False

        trang_thai[vi_tri] = gia_tri_mong_muon
        self.giai_phap_backtracking.append(trang_thai.copy())

        if self.giaiBacktracking(trang_thai, vi_tri + 1):
            return True

        trang_thai[vi_tri] = 0
        self.giai_phap_backtracking.append(trang_thai.copy())
        return False

    def capNhatBanBacktracking(self, trang_thai):
        for i in range(3):
            for j in range(3):
                chi_so = i*3 + j
                gia_tri = trang_thai[chi_so] if trang_thai[chi_so] != 0 else ""
                self.o_backtracking[i][j].config(text=str(gia_tri))

        for i in range(9):
            if trang_thai[i] == 0 or (i < 8 and trang_thai[i] != i+1):
                hang, cot = i//3, i%3
                self.o_backtracking[hang][cot].config(bg="lightyellow")
                break

    def buocTiepTheoBacktracking(self):
        if self.buoc_hien_tai < len(self.cac_buoc_backtracking):
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[self.buoc_hien_tai])
            self.buoc_hien_tai += 1
        else:
            self.nut_buoc.config(state=tk.DISABLED)
            messagebox.showinfo("Thông báo", "Đã hoàn thành backtracking!")

    def tuDongBacktracking(self):
        if not self.dang_chay_backtracking:
            self.dang_chay_backtracking = True
            self.nut_tu_dong.config(text="Dừng lại")
            self.hieuUngBacktracking()
        else:
            self.dang_chay_backtracking = False
            self.nut_tu_dong.config(text="Tự động")

    def hieuUngBacktracking(self):
        if self.buoc_hien_tai < len(self.cac_buoc_backtracking) and self.dang_chay_backtracking:
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[self.buoc_hien_tai])
            self.buoc_hien_tai += 1
            self.chuong_trinh.after(500, self.hieuUngBacktracking)
        elif self.dang_chay_backtracking:
            self.dang_chay_backtracking = False
            self.nut_tu_dong.config(text="Tự động")
            messagebox.showinfo("Thông báo", "Đã hoàn thành backtracking!")

    def chayBacktracking(self, o_vuong):
        def cap_nhat_luoi(ban, trang_thai, o_vuong):
            for i in range(3):
                for j in range(3):
                    gia_tri = ban[i * 3 + j]
                    o_vuong[i][j].configure(
                        text=gia_tri if gia_tri is not None else "",
                        background="#5aadad" if gia_tri is not None else "#ffffff",
                    )

        giai = backtracking.Backtracking8Puzzle(update_callback=lambda ban, trang_thai: cap_nhat_luoi(ban, trang_thai, o_vuong))
        giai.giai()

    def tiepDay(self, su_kien=None):
        if self.con_tro_trang_thai < len(self.duong_di) - 1:
            self.dungTienNhanh()
            self.con_tro_trang_thai += 1
            self.lamMoiKhung()

    def giai(self, su_kien=None):
        if self.sanSangGiai():
            thong_bao = (
                "Thuật toán: "
                + str(self.thuat_toan)
                + "\nTrạng thái ban đầu = "
                + str(self.trang_thai_ban_dau)
            )
            self.datLaiLuoi()
            self.giaiTrangThai()
            if len(self.duong_di) == 0:
                messagebox.showinfo(
                    "Không thể giải", "Trạng thái ban đầu không thể giải!"
                )
                self.hienThiPhanTichTimKiem(True)
            else:
                self.lamMoiKhung()
        else:
            loi_giai = (
                "Không thể giải.\n"
                "Thuật toán sử dụng: " + str(self.thuat_toan) + "\n"
                "Trạng thái ban đầu   : " + str(self.trang_thai_ban_dau)
            )
            messagebox.showerror("Không thể giải!", loi_giai)

    def nhapTrangThaiBanDau(self, su_kien=None):
        trang_thai_nhap = simpledialog.askstring(
            "Nhập trạng thái ban đầu", "Vui lòng nhập trạng thái ban đầu!"
        )
        if trang_thai_nhap is not None:
            if self.kiemTraTrangThai(trang_thai_nhap):
                # Kiểm tra số nghịch thế
                so_nghich_the = self.demSoNghichThe(trang_thai_nhap)
                if so_nghich_the % 2 != 0:
                    messagebox.showerror(
                        "Lỗi đầu vào",
                        "Trạng thái ban đầu không thể giải được (số nghịch thế là lẻ)!",
                    )
                    return
                if (
                    trang_thai_nhap != self.trang_thai_ban_dau
                ):
                    self.trang_thai_ban_dau = trang_thai_nhap
                    self.du_lieu_thoi_gian_chay = {}
                self.datLai()
                self.hienThiTrangThaiTrenLuoi(self.trang_thai_ban_dau)
                self.capNhatLuoiTrangThaiBanDau(self.trang_thai_ban_dau)
            else:
                messagebox.showerror("Lỗi đầu vào", "Trạng thái ban đầu không hợp lệ!")

    def chonThuatToan(self, su_kien=None):
        try:
            lua_chon = self.hop_thuat_toan.get()
            self.datLai()
            self.thuat_toan = lua_chon
        except:
            pass

    def xuatTep(self, su_kien=None):
        if not self.daGiai():
            messagebox.showwarning(
                "Cảnh báo", "Chưa có đường dẫn để xuất! Vui lòng nhấn Giải trước."
            )
            return

        ten_tep = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Tệp Excel", "*.xlsx"), ("Tất cả tệp", "*.*")],
            initialfile=f"{self.thuat_toan}_duong_di",
            title="Chọn nơi lưu tệp Excel",
        )
        if not ten_tep:
            return

        du_lieu = []
        for i, trang_thai in enumerate(self.duong_di):
            chuoi_trang_thai = AI.getStringRepresentation(trang_thai)
            ma_tran = [
                [
                    self.dieuChinhChuSo(chuoi_trang_thai[0]),
                    self.dieuChinhChuSo(chuoi_trang_thai[1]),
                    self.dieuChinhChuSo(chuoi_trang_thai[2]),
                ],
                [
                    self.dieuChinhChuSo(chuoi_trang_thai[3]),
                    self.dieuChinhChuSo(chuoi_trang_thai[4]),
                    self.dieuChinhChuSo(chuoi_trang_thai[5]),
                ],
                [
                    self.dieuChinhChuSo(chuoi_trang_thai[6]),
                    self.dieuChinhChuSo(chuoi_trang_thai[7]),
                    self.dieuChinhChuSo(chuoi_trang_thai[8]),
                ],
            ]
            du_lieu.append(
                {"Bước": f"Ma trận bước {i}", "Cột 1": "", "Cột 2": "", "Cột 3": ""}
            )
            du_lieu.append(
                {
                    "Bước": "",
                    "Cột 1": ma_tran[0][0],
                    "Cột 2": ma_tran[0][1],
                    "Cột 3": ma_tran[0][2],
                }
            )
            du_lieu.append(
                {
                    "Bước": "",
                    "Cột 1": ma_tran[1][0],
                    "Cột 2": ma_tran[1][1],
                    "Cột 3": ma_tran[1][2],
                }
            )
            du_lieu.append(
                {
                    "Bước": "",
                    "Cột 1": ma_tran[2][0],
                    "Cột 2": ma_tran[2][1],
                    "Cột 3": ma_tran[2][2],
                }
            )
            du_lieu.append({"Bước": "", "Cột 1": "", "Cột 2": "", "Cột 3": ""})

        df = pd.DataFrame(du_lieu)

        du_lieu_phan_tich = {
            "Thuật toán": [str(self.thuat_toan)],
            "Trạng thái ban đầu": [str(self.trang_thai_ban_dau)],
            "Số trạng thái đã duyệt qua": [self.bo_dem],
            "Độ sâu": [self.do_sau],
            "Chi phí": [self.chi_phi],
            "Thời gian chạy (s)": [self.thoi_gian_chay],
        }
        df_phan_tich = pd.DataFrame(du_lieu_phan_tich)

        try:
            with pd.ExcelWriter(ten_tep, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Đường dẫn", index=False)
                df_phan_tich.to_excel(writer, sheet_name="Phân tích", index=False)
            messagebox.showinfo("Thành công", f"Đã xuất đường dẫn ra tệp: {ten_tep}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất tệp: {str(e)}")

    def tienNhanh(self, su_kien=None):
        self.dungTienNhanh()
        if self.con_tro_trang_thai < self.chi_phi:
            self.nut_dung.configure(state="enabled")
            self.con_tro_trang_thai += 1
            self.lamMoiKhung()
            ms = 100
            if 100 < self.chi_phi <= 1000:
                ms = 20
            if self.chi_phi > 1000:
                ms = 1
            self.cong_viec = self.dem_buoc.after(ms, self.tienNhanh)
        else:
            self.dungTienNhanh()

    def luiNhanh(self, su_kien=None):
        self.dungTienNhanh()
        if self.con_tro_trang_thai > 0:
            self.nut_dung.configure(state="enabled")
            self.con_tro_trang_thai -= 1
            ms = 50
            if self.chi_phi > 1000:
                ms = 1
            self.cong_viec = self.dem_buoc.after(ms, self.luiNhanh)
        else:
            self.dungTienNhanh()
        self.lamMoiKhung()

    def dungTienNhanh(self, su_kien=None):
        if self.cong_viec is not None:
            self.nut_dung.configure(state="disabled")
            self.dem_buoc.after_cancel(self.cong_viec)
            self.cong_viec = None

    def datLaiBoDemBuoc(self, su_kien=None):
        if self.con_tro_trang_thai > 0:
            self.dungTienNhanh()
            self.con_tro_trang_thai = 0
            self.lamMoiKhung()

    def xaoTron(self, su_kien=None):
        while True:
            puzzle = list("012345678")
            random.shuffle(puzzle)
            self.trang_thai_ban_dau = "".join(puzzle)
            so_nghich_the = self.demSoNghichThe(self.trang_thai_ban_dau)
            if so_nghich_the % 2 == 0:
                break
        self.datLai()
        self.hienThiTrangThaiTrenLuoi(self.trang_thai_ban_dau)
        self.capNhatLuoiTrangThaiBanDau(self.trang_thai_ban_dau)
        messagebox.showinfo(
            "Trạng thái mới", f"Trạng thái ban đầu: {self.trang_thai_ban_dau}"
        )

    def hienThiTrangThaiTrenLuoi(self, trang_thai):
        if not self.kiemTraTrangThai(trang_thai):
            trang_thai = "000000000"
        for i in range(3):
            for j in range(3):
                chi_so = i * 3 + j
                self.o_vuong[i][j].configure(text=self.dieuChinhChuSo(trang_thai[chi_so]))
                if self.con_tro_trang_thai == 0:
                    self.o_vuong_ban_dau[i][j].configure(text=self.dieuChinhChuSo(trang_thai[chi_so]))

    def capNhatLuoiTrangThaiBanDau(self, trang_thai):
        if not self.kiemTraTrangThai(trang_thai):
            trang_thai = "000000000"
        for i in range(3):
            for j in range(3):
                chi_so = i * 3 + j
                self.o_vuong_ban_dau[i][j].configure(text=self.dieuChinhChuSo(trang_thai[chi_so]))


    # ------------- Các hàm hỗ trợ -----------------

    @staticmethod
    def kiemTraTrangThai(trang_thai_nhap):
        da_thay = []
        if trang_thai_nhap is None or len(trang_thai_nhap) != 9 or not trang_thai_nhap.isnumeric():
            return False
        for chu_so in trang_thai_nhap:
            if chu_so in da_thay or chu_so == "9":
                return False
            da_thay.append(chu_so)
        return True

    @staticmethod
    def dieuChinhChuSo(chu_so):
        if chu_so == "0":
            return " "
        return chu_so

    def lamMoiKhung(self):
        if self.chi_phi > 0:
            trang_thai = AI.getStringRepresentation(self.duong_di[self.con_tro_trang_thai])
            self.hienThiTrangThaiTrenLuoi(trang_thai)
            self.dem_buoc.configure(text=self.layChuoiDemBuoc())
            self.hienThiPhanTichTimKiem()
        if self.con_tro_trang_thai == 0:
            self.nut_dat_lai.configure(state="disabled")
            self.nut_lui.configure(state="disabled")
            self.nut_lui_nhanh.configure(state="disabled")
        else:
            self.nut_dat_lai.configure(state="enabled")
            self.nut_lui.configure(state="enabled")
            self.nut_lui_nhanh.configure(state="enabled")
        if self.chi_phi == 0 or self.con_tro_trang_thai == self.chi_phi:
            self.nut_tien_nhanh.configure(state="disabled")
            self.nut_tiep.configure(state="disabled")
        else:
            self.nut_tien_nhanh.configure(state="enabled")
            self.nut_tiep.configure(state="enabled")

    def layChuoiDemBuoc(self):
        return str(self.con_tro_trang_thai) + "/" + str(self.chi_phi)

    @staticmethod
    def demSoNghichThe(trang_thai):
        danh_sach_trang_thai = [int(d) for d in trang_thai if d != "0"]
        so_nghich_the = 0
        for i in range(len(danh_sach_trang_thai)):
            for j in range(i + 1, len(danh_sach_trang_thai)):
                if danh_sach_trang_thai[i] > danh_sach_trang_thai[j]:
                    so_nghich_the += 1
        return so_nghich_the

    def daGiai(self):
        return len(self.duong_di) > 0

    def sanSangGiai(self):
        return self.trang_thai_ban_dau is not None and self.thuat_toan is not None

    def datLaiLuoi(self):
        self.con_tro_trang_thai = 0
        self.lamMoiKhung()
        self.dem_buoc.configure(text=self.layChuoiDemBuoc())

    def giaiTrangThai(self):
        if self.thuat_toan == "BFS":
            self.giaiBFS()
        elif str(self.thuat_toan) == "DFS":
            self.giaiDFS()
        elif str(self.thuat_toan) == "Uniform Cost Search":
            self.giaiUCS()
        elif str(self.thuat_toan) == "Iterative Deepening":
            self.giaiIDS()
        elif str(self.thuat_toan) == "Greed Best First Search":
            self.giaiGreedBestFirstSearch()
        elif str(self.thuat_toan) == "A*":
            self.giaiAStar()
        elif str(self.thuat_toan) == "IDA*":
            self.giaiIDAStar()
        elif str(self.thuat_toan) == "Simple Hill Climbing":
            self.giaiSimpleHillClimbing()
        elif str(self.thuat_toan) == "Stochastic Hill Climbing":
            self.giaiStochasticHillClimbing()
        elif str(self.thuat_toan) == "Simulated Annealing":
            self.giaiSimulatedAnnealing()
        elif str(self.thuat_toan) == "Beam Search":
            self.giaiBeamSearch()
        elif str(self.thuat_toan) == "Genetic Search":
            self.giaiGeneticSearch()
        elif str(self.thuat_toan) == "AND OR Graph Search":
            self.giaiAndOrGraphSearch()
        elif str(self.thuat_toan) == "QLearning":
            self.giaiQLearning()

        if self.thuat_toan and self.trang_thai_ban_dau:
            self.du_lieu_thoi_gian_chay[self.thuat_toan] = {
                "do_sau": self.do_sau,
                "kich_thuoc_bo_nho": self.kich_thuoc_bo_nho,
                "thoi_gian_chay": self.thoi_gian_chay,
                "bo_dem": self.bo_dem,
            }

    def datLai(self):
        self.duong_di = []
        self.chi_phi = self.bo_dem = 0
        self.thoi_gian_chay = 0.0
        self.datLaiLuoi()
        self.hop_phan_tich.configure(text="")

    # ----------------- Các thuật toán ------------------

    def giaiBFS(self):
        giai_bfs = bfs.BFSAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_bfs.BFS(
            self.trang_thai_ban_dau
        )

    def giaiDFS(self):
        giai_dfs = dfs.DFSAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_dfs.DFS(
            self.trang_thai_ban_dau
        )

    def giaiUCS(self):
        giai_ucs = ucs.UCSAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_ucs.UCS(
            self.trang_thai_ban_dau
        )

    def giaiIDS(self):
        giai_ids = ids.IDSAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_ids.IDS(
            self.trang_thai_ban_dau
        )

    def giaiGreedBestFirstSearch(self):
        giai_best_first = greed_best_first_search.GreedBestFirstSearchAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_best_first.BestFirstSearch(
            self.trang_thai_ban_dau
        )

    def giaiAStar(self):
        giai_astar = astar.AStarAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_astar.AStar(
            self.trang_thai_ban_dau
        )

    def giaiIDAStar(self):
        giai_idastar = idastar.IDAStarAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_idastar.IDAStar(
            self.trang_thai_ban_dau
        )

    def giaiSimpleHillClimbing(self):
        giai_simple_hill_climbing = simple_hill_climbing.SimpleHillClimbingAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_simple_hill_climbing.SimpleHillClimbing(
            self.trang_thai_ban_dau
        )

    def giaiStochasticHillClimbing(self):
        giai_stochastic_hill_climbing = stochastic_hill_climbing.StochasticHillClimbingAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_stochastic_hill_climbing.StochasticHillClimbing(
            self.trang_thai_ban_dau
        )

    def giaiSimulatedAnnealing(self):
        giai_simulated_annealing = simulated_annealing.SimulatedAnnealingAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_simulated_annealing.SimulatedAnnealing(
            self.trang_thai_ban_dau
        )

    def giaiBeamSearch(self):
        giai_beam_search = beam_search.BeamSearchAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_beam_search.BeamSearch(
            self.trang_thai_ban_dau
        )

    def giaiGeneticSearch(self):
        giai_genetic_search = genetic_search.GeneticAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_genetic_search.GeneticSearch(
            self.trang_thai_ban_dau
        )

    def giaiAndOrGraphSearch(self):
        giai_and_or_graph_search = and_or_graph_search.AndOrGraphSearchAlgorithm()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_and_or_graph_search.AndOrGraphSearch(
            self.trang_thai_ban_dau, 123456780
        )

    def giaiQLearning(self):
        giai_q_learning = q_learning.QLearning()
        self.duong_di, self.chi_phi, self.bo_dem, self.do_sau, self.thoi_gian_chay, self.kich_thuoc_bo_nho = giai_q_learning.train(
            self.trang_thai_ban_dau, 123456780
        )

    def taoLuoiPuzzle(self):
        # Tạo các khung cho puzzle chính, trạng thái ban đầu và trạng thái đích
        khung_chinh = ttk.Frame(self.bang_trai)
        khung_chinh.pack(pady=20)

        khung_ban_dau = ttk.Frame(self.bang_trai)
        khung_ban_dau.pack(pady=10)

        khung_muc_tieu = ttk.Frame(self.bang_trai)
        khung_muc_tieu.pack(pady=10)

        # Nhãn cho từng phần
        ttk.Label(khung_chinh, text="Trạng thái hiện tại", font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(khung_ban_dau, text="Trạng thái ban đầu", font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(khung_muc_tieu, text="Trạng thái đích", font=("Arial", 14, "bold")).pack(pady=5)

        # Tạo các khung lưới cho từng phần
        khung_luoi_chinh = ttk.Frame(khung_chinh)
        khung_luoi_chinh.pack()

        khung_luoi_ban_dau = ttk.Frame(khung_ban_dau)
        khung_luoi_ban_dau.pack()

        khung_luoi_muc_tieu = ttk.Frame(khung_muc_tieu)
        khung_luoi_muc_tieu.pack()

        # Tạo lưới puzzle chính
        self.o_vuong = []
        for i in range(3):
            hang = []
            for j in range(3):
                o = ttk.Label(
                    khung_luoi_chinh,
                    text=" ",
                    font=("Arial", 36, "bold"),
                    background="#3498db",
                    foreground="white",
                    width=3,
                    relief="raised",
                    borderwidth=2,
                    anchor="center",
                    justify="center"
                )
                o.grid(row=i, column=j, padx=2, pady=2)
                hang.append(o)
            self.o_vuong.append(hang)

        # Tạo lưới trạng thái ban đầu
        self.o_vuong_ban_dau = []
        for i in range(3):
            hang = []
            for j in range(3):
                o = ttk.Label(
                    khung_luoi_ban_dau,
                    text=" ",
                    font=("Arial", 24, "bold"),
                    background="#3498db",
                    foreground="white",
                    width=2,
                    relief="raised",
                    borderwidth=2,
                    anchor="center",
                    justify="center"
                )
                o.grid(row=i, column=j, padx=2, pady=2)
                hang.append(o)
            self.o_vuong_ban_dau.append(hang)

        # Tạo lưới trạng thái đích
        self.o_vuong_muc_tieu = []
        trang_thai_muc_tieu = "123456780"
        for i in range(3):
            hang = []
            for j in range(3):
                o = ttk.Label(
                    khung_luoi_muc_tieu,
                    text=self.dieuChinhChuSo(trang_thai_muc_tieu[i*3 + j]),
                    font=("Arial", 24, "bold"),
                    background="#3498db",
                    foreground="white",
                    width=2,
                    relief="raised",
                    borderwidth=2,
                    anchor="center",
                    justify="center"
                )
                o.grid(row=i, column=j, padx=2, pady=2)
                hang.append(o)
            self.o_vuong_muc_tieu.append(hang)

    def taoNutDieuKhien(self):
        # Khung các nút điều khiển
        khung_dieu_khien = ttk.Frame(self.bang_phai)
        khung_dieu_khien.pack(pady=10)

        # Nút giải
        self.nut_giai = ttk.Button(
            khung_dieu_khien,
            text="Giải",
            command=self.giai
        )
        self.nut_giai.pack(side="left", padx=5)

        # Nút xáo trộn
        self.nut_xao_tron = ttk.Button(
            khung_dieu_khien,
            text="Trạng thái mới",
            command=self.xaoTron
        )
        self.nut_xao_tron.pack(side="left", padx=5)

        # Nút nhập trạng thái
        self.nut_nhap_trang_thai = ttk.Button(
            khung_dieu_khien,
            text="Nhập trạng thái",
            command=self.nhapTrangThaiBanDau
        )
        self.nut_nhap_trang_thai.pack(side="left", padx=5)

        # Nút xuất tệp
        self.nut_xuat_tep = ttk.Button(
            khung_dieu_khien,
            text="Xuất đường dẫn",
            command=self.xuatTep
        )
        self.nut_xuat_tep.pack(side="left", padx=5)