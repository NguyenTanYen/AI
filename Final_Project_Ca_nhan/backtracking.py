import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import deque
from algorithms.test import chay_kiem_tra_thuat_toan, vi_pham_rang_buoc
from algorithms.backtracking_ac3 import backtracking_with_ac3
from algorithms.backtracking import backtracking_with_steps

class CuaSoBacktracking:
    def __init__(self, chuong_trinh):
        self.cua_so = tk.Toplevel(chuong_trinh)
        self.cua_so.title("Backtracking 8-Puzzle")
        self.cua_so.geometry("650x750")
        self.cua_so.configure(bg="#e0f7fa")

        self.trang_thai_muc_tieu = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.muc_tieu_phang = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        self.taoBanBacktracking()

        khung_dieu_khien = ttk.Frame(self.cua_so, style="TFrame")
        khung_dieu_khien.pack(pady=15, padx=10)

        self.nut_khoi_dong = ttk.Button(khung_dieu_khien, text="Khởi động", 
                                        command=self.khoiDongBacktracking)
        self.nut_khoi_dong.pack(side=tk.LEFT, padx=8)

        self.nut_tung_buoc = ttk.Button(khung_dieu_khien, text="Bước tiếp", 
                                        command=self.buocTiepBacktracking, state=tk.DISABLED)
        self.nut_tung_buoc.pack(side=tk.LEFT, padx=8)

        self.nut_tu_dong = ttk.Button(khung_dieu_khien, text="Chạy tự động", 
                                      command=self.tuDongBacktracking, state=tk.DISABLED)
        self.nut_tu_dong.pack(side=tk.LEFT, padx=8)

        self.nut_ac3 = ttk.Button(khung_dieu_khien, text="AC-3", 
                                  command=self.chayAC3)
        self.nut_ac3.pack(side=tk.LEFT, padx=8)

        self.nut_csp = ttk.Button(khung_dieu_khien, text="CSP", 
                                  command=self.hienThiCSP)
        self.nut_csp.pack(side=tk.LEFT, padx=8)

        self.nut_backtrack = ttk.Button(khung_dieu_khien, text="Backtrack", 
                                        command=self.chayBacktrack)
        self.nut_backtrack.pack(side=tk.LEFT, padx=8)

        self.nut_kiem_tra = ttk.Button(khung_dieu_khien, text="Kiểm thử", 
                                       command=self.chayKiemTra)
        self.nut_kiem_tra.pack(side=tk.LEFT, padx=8)

        self.nut_lui = ttk.Button(khung_dieu_khien, text="Lùi lại", 
                                  command=self.luiBuocBacktracking, state=tk.DISABLED)
        self.nut_lui.pack(side=tk.LEFT, padx=8)

        self.nut_dat_lai = ttk.Button(khung_dieu_khien, text="Đặt lại", 
                                      command=self.datLaiBacktracking, state=tk.DISABLED)
        self.nut_dat_lai.pack(side=tk.LEFT, padx=8)

        self.nhan_thong_tin_buoc = tk.Label(
            self.cua_so,
            text="Nhấn 'Khởi động' để bắt đầu Backtracking",
            font=("Arial", 14),
            wraplength=600,
            bg="#e0f7fa",
            fg="#006064"
        )
        self.nhan_thong_tin_buoc.pack(pady=15)

        self.nhan_so_buoc = tk.Label(
            self.cua_so,
            text="Tổng số bước: 0",
            font=("Arial", 13),
            bg="#e0f7fa",
            fg="#006064"
        )
        self.nhan_so_buoc.pack(pady=5)

        self.nhan_buoc_hien_tai = tk.Label(
            self.cua_so,
            text="Bước hiện tại: 0",
            font=("Arial", 13),
            bg="#e0f7fa",
            fg="#006064"
        )
        self.nhan_buoc_hien_tai.pack(pady=5)

        self.cac_buoc_backtracking = []
        self.thong_tin_buoc = []
        self.buoc_hien_tai = 0
        self.dang_chay_backtracking = False
        self.csp = None

    def taoBanBacktracking(self):
        khung_ban = ttk.Frame(self.cua_so, style="TFrame")
        khung_ban.pack(pady=25)

        khung_luoi = ttk.Frame(khung_ban)
        khung_luoi.pack()

        self.o_vuong_backtracking = []
        for i in range(3):
            hang = []
            for j in range(3):
                o = tk.Label(
                    khung_luoi,
                    text="",
                    font=("Arial", 28, "bold"),
                    width=5,
                    height=2,
                    relief="ridge",
                    bg="#ffffff",
                    fg="#004d40"
                )
                o.grid(row=i, column=j, padx=3, pady=3)
                hang.append(o)
            self.o_vuong_backtracking.append(hang)

        khung_muc_tieu = ttk.Frame(self.cua_so, style="TFrame")
        khung_muc_tieu.pack(pady=15)

        tk.Label(khung_muc_tieu, text="Trạng thái mục tiêu:", 
                 font=("Arial", 14, "bold"), bg="#e0f7fa", fg="#006064").pack()

        khung_luoi_muc_tieu = ttk.Frame(khung_muc_tieu)
        khung_luoi_muc_tieu.pack()

        for i in range(3):
            for j in range(3):
                chi_so = i * 3 + j
                gia_tri = self.muc_tieu_phang[chi_so] if self.muc_tieu_phang[chi_so] != 0 else ""
                tk.Label(
                    khung_luoi_muc_tieu,
                    text=str(gia_tri),
                    font=("Arial", 18),
                    width=5,
                    height=2,
                    relief="groove",
                    bg="#b2dfdb",
                    fg="#004d40"
                ).grid(row=i, column=j, padx=3, pady=3)

    def khoiDongBacktracking(self):
        trang_thai_ban_dau = [[None for _ in range(3)] for _ in range(3)]
        self.cac_buoc_backtracking = []
        self.thong_tin_buoc = []
        self.buoc_hien_tai = 0
        self.nhan_thong_tin_buoc.config(text="Đang tìm kiếm giải pháp...")

        ket_qua = self.giai(trang_thai_ban_dau)
        if ket_qua['giai_phap']:
            self.cac_buoc_backtracking = ket_qua['duong_di']
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[0], 0)
            self.nut_tung_buoc.config(state=tk.NORMAL)
            self.nut_tu_dong.config(state=tk.NORMAL)
            self.nut_dat_lai.config(state=tk.NORMAL)
            self.nut_lui.config(state=tk.DISABLED)
            self.nhan_thong_tin_buoc.config(text=f"Đã tìm thấy giải pháp! Số node mở rộng: {ket_qua['so_node_mo_rong']}, Độ sâu tối đa: {ket_qua['do_sau_toi_da']}")
        else:
            self.nhan_thong_tin_buoc.config(text="Không tìm thấy giải pháp!")
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")

    def demSoNghichThe(self, gan_gia_tri):
        phang = [0] * 9
        for bien, gia_tri in gan_gia_tri.items():
            chi_so = int(bien[1:]) - 1
            phang[chi_so] = gia_tri
        
        so = [num for num in phang if num != 0]
        so_nghich_the = 0
        for i in range(len(so)):
            for j in range(i + 1, len(so)):
                if so[i] > so[j]:
                    so_nghich_the += 1
        return so_nghich_the

    def taoRangBuoc(self):
        rang_buoc = []
        rang_buoc.append((lambda gan_gia_tri: len(set(gan_gia_tri.values())) == len(gan_gia_tri) if gan_gia_tri else True))
        return rang_buoc

    def kiemTraNhatQuan(self, bien, gia_tri, gan_gia_tri, csp):
        if gia_tri in gan_gia_tri.values() and len(gan_gia_tri) > 0:
            return False

        gan_gia_tri_tam = gan_gia_tri.copy()
        gan_gia_tri_tam[bien] = gia_tri

        for rang_buoc in csp['rang_buoc']:
            if callable(rang_buoc):
                if not rang_buoc(gan_gia_tri_tam):
                    return False
            elif len(rang_buoc) == 2:
                ten, ham_rang_buoc = rang_buoc
                if ten in gan_gia_tri_tam:
                    if not ham_rang_buoc(gan_gia_tri_tam[ten]):
                        return False
        return True

    def ac3(self, csp):
        hang_cho = deque([(xi, xj) for xi in csp['bien'] for xj in csp['bien'] if xi != xj])
        mien = {bien: gia_tri[:] for bien, gia_tri in csp['mien'].items()}
        
        while hang_cho:
            xi, xj = hang_cho.popleft()
            if self.suaDoi(csp, xi, xj, mien):
                if not mien[xi]:
                    return None
                for xk in [v for v in csp['bien'] if v != xi and v != xj]:
                    hang_cho.append((xk, xi))
        
        return mien

    def suaDoi(self, csp, xi, xj, mien):
        da_sua = False
        gia_tri_can_xoa = []
        
        for x in mien[xi]:
            nhat_quan = False
            for y in mien[xj]:
                gan_gia_tri_tam = {xi: x, xj: y}
                nhat_quan = all(
                    rang_buoc(gan_gia_tri_tam) if callable(rang_buoc) else
                    (rang_buoc[1](gan_gia_tri_tam[rang_buoc[0]]) if rang_buoc[0] in gan_gia_tri_tam else True)
                    for rang_buoc in csp['rang_buoc']
                )
                if nhat_quan:
                    break
            if not nhat_quan:
                gia_tri_can_xoa.append(x)
                da_sua = True
        
        for x in gia_tri_can_xoa:
            mien[xi].remove(x)
        
        return da_sua

    def chayAC3(self):
        self.cac_buoc_backtracking = []
        self.thong_tin_buoc = []
        self.buoc_hien_tai = 0
        self.nhan_thong_tin_buoc.config(text="Đang chạy Backtracking với AC-3...")
        self.nhan_so_buoc.config(text="Tổng số bước: 0")
        self.nhan_buoc_hien_tai.config(text="Bước hiện tại: 0")
        
        trang_thai_ban_dau = [[None for _ in range(3)] for _ in range(3)]
        cac_buoc, so_node_tham, nhat_ky_ac3 = backtracking_with_ac3(trang_thai_ban_dau, self.trang_thai_muc_tieu)
        
        self.thong_tin_buoc = nhat_ky_ac3 + [f"Trạng thái Backtracking: {buoc}" for buoc in cac_buoc]
        self.cac_buoc_backtracking = cac_buoc
        
        if cac_buoc:
            self.nhan_so_buoc.config(text=f"Tổng số bước: {len(cac_buoc)}")
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[0], 0)
            self.nut_tung_buoc.config(state=tk.NORMAL)
            self.nut_tu_dong.config(state=tk.NORMAL)
            self.nut_dat_lai.config(state=tk.NORMAL)
            self.nut_lui.config(state=tk.DISABLED)
            self.nhan_thong_tin_buoc.config(text=f"AC-3 + Backtracking: Tìm thấy giải pháp! Nodes: {so_node_tham}")
            messagebox.showinfo("Thông báo", f"AC-3 + Backtracking: Tìm thấy giải pháp sau {so_node_tham} nodes!")
        else:
            self.nhan_thong_tin_buoc.config(text="AC-3 + Backtracking: Không tìm thấy giải pháp!")
            messagebox.showinfo("Thông báo", "AC-3 + Backtracking: Không tìm thấy giải pháp!")

    def hienThiCSP(self):
        self.cac_buoc_backtracking = []
        self.thong_tin_buoc = []
        self.buoc_hien_tai = 0
        self.nhan_thong_tin_buoc.config(text="Đang chạy Backtracking...")
        self.nhan_so_buoc.config(text="Tổng số bước: 0")
        self.nhan_buoc_hien_tai.config(text="Bước hiện tại: 0")
        
        trang_thai_ban_dau = [[None for _ in range(3)] for _ in range(3)]
        cac_buoc, so_node_tham = backtracking_with_steps(trang_thai_ban_dau, self.trang_thai_muc_tieu)
        
        self.thong_tin_buoc = [f"Trạng thái Backtracking: {buoc}" for buoc in cac_buoc]
        self.cac_buoc_backtracking = cac_buoc
        
        if cac_buoc:
            self.nhan_so_buoc.config(text=f"Tổng số bước: {len(cac_buoc)}")
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[0], 0)
            self.nut_tung_buoc.config(state=tk.NORMAL)
            self.nut_tu_dong.config(state=tk.NORMAL)
            self.nut_dat_lai.config(state=tk.NORMAL)
            self.nut_lui.config(state=tk.DISABLED)
            self.nhan_thong_tin_buoc.config(text=f"Backtracking: Tìm thấy giải pháp! Nodes: {so_node_tham}")
            messagebox.showinfo("Thông báo", f"Backtracking: Tìm thấy giải pháp sau {so_node_tham} nodes!")
        else:
            self.nhan_thong_tin_buoc.config(text="Backtracking: Không tìm thấy giải pháp!")
            messagebox.showinfo("Thông báo", "Backtracking: Không tìm thấy giải pháp!")

    def chayKiemTra(self):
        self.cac_buoc_backtracking = []
        self.thong_tin_buoc = []
        self.buoc_hien_tai = 0
        self.nhan_thong_tin_buoc.config(text="Đang chạy kiểm tra...")
        self.nhan_so_buoc.config(text="Tổng số bước: 0")
        self.nhan_buoc_hien_tai.config(text="Bước hiện tại: 0")

        duong_di, thong_tin_buoc, so_buoc = chay_kiem_tra_thuat_toan(self.trang_thai_muc_tieu)
        
        self.cac_buoc_backtracking = duong_di
        self.thong_tin_buoc = thong_tin_buoc
        
        self.nhan_so_buoc.config(text=f"Tổng số bước: {so_buoc}")
        self.capNhatBanBacktracking(self.cac_buoc_backtracking[0], 0)
        self.nut_tung_buoc.config(state=tk.NORMAL)
        self.nut_tu_dong.config(state=tk.NORMAL)
        
        if not vi_pham_rang_buoc(duong_di[-1], self.trang_thai_muc_tieu):
            self.nhan_thong_tin_buoc.config(text="Kiểm tra: Đã đạt mục tiêu!")
            messagebox.showinfo("Kết quả kiểm tra", f"Đã đạt mục tiêu sau {so_buoc} bước!")
        else:
            self.nhan_thong_tin_buoc.config(text=f"Kiểm tra: Không đạt mục tiêu sau {so_buoc} bước!")
            messagebox.showinfo("Kết quả kiểm tra", f"Không đạt mục tiêu sau {so_buoc} bước!")

    def giai(self, trang_thai_ban_dau):
        so_node_mo_rong = [0]
        do_sau_toi_da = [0]
        duong_di = []
        thong_tin_buoc = []

        trang_thai_phang = [num if num is not None else 0 for hang in trang_thai_ban_dau for num in hang]
        bien = [f"X{i+1}" for i in range(9)]
        thu_tu_gia_tri = list(range(9))
        mien = {var: thu_tu_gia_tri.copy() for var in bien}
        rang_buoc = self.taoRangBuoc()

        self.csp = {
            'bien': bien,
            'mien': mien,
            'rang_buoc': rang_buoc,
            'gan_gia_tri_ban_dau': {}
        }

        ket_qua = self.luiLai({}, 0, self.csp, so_node_mo_rong, do_sau_toi_da, duong_di, thong_tin_buoc)

        if ket_qua:
            luoi_giai_phap = [[0 for _ in range(3)] for _ in range(3)]
            for bien, gia_tri in ket_qua.items():
                chi_so = int(bien[1:]) - 1
                hang, cot = chi_so // 3, chi_so % 3
                luoi_giai_phap[hang][cot] = gia_tri
            self.thong_tin_buoc = thong_tin_buoc
            return {
                'duong_di': duong_di,
                'so_node_mo_rong': so_node_mo_rong[0],
                'do_sau_toi_da': do_sau_toi_da[0],
                'giai_phap': luoi_giai_phap
            }
        else:
            self.thong_tin_buoc = thong_tin_buoc
            return {
                'duong_di': duong_di,
                'so_node_mo_rong': so_node_mo_rong[0],
                'do_sau_toi_da': do_sau_toi_da[0],
                'giai_phap': None
            }

    def luiLai(self, gan_gia_tri, chi_so, csp, so_node_mo_rong, do_sau_toi_da, duong_di, thong_tin_buoc):
        so_node_mo_rong[0] += 1
        do_sau_toi_da[0] = max(do_sau_toi_da[0], len(gan_gia_tri))

        def chupLuoi(gan_gia_tri_hien_tai):
            luoi = [[None for _ in range(3)] for _ in range(3)]
            for bien, gia_tri in gan_gia_tri_hien_tai.items():
                chi_so = int(bien[1:]) - 1
                hang, cot = chi_so // 3, chi_so % 3
                luoi[hang][cot] = gia_tri
            return [hang[:] for hang in luoi]

        if gan_gia_tri:
            duong_di.append(chupLuoi(gan_gia_tri))

        if chi_so == len(csp['bien']):
            luoi = [[0 for _ in range(3)] for _ in range(3)]
            for bien, gia_tri in gan_gia_tri.items():
                chi_so = int(bien[1:]) - 1
                hang, cot = chi_so // 3, chi_so % 3
                luoi[hang][cot] = gia_tri
            so_nghich_the = self.demSoNghichThe(gan_gia_tri)
            if so_nghich_the % 2 == 0 and luoi == self.trang_thai_muc_tieu:
                return gan_gia_tri
            return None

        bien = csp['bien'][chi_so]
        gia_tri = csp['mien'][bien][:]

        random.shuffle(gia_tri)

        for gt in gia_tri:
            gan_gia_tri[bien] = gt
            thong_tin_buoc.append(f"Thử {gt} tại {bien}")
            duong_di.append(chupLuoi(gan_gia_tri))
            if self.kiemTraNhatQuan(bien, gt, gan_gia_tri, csp):
                ket_qua = self.luiLai(gan_gia_tri, chi_so + 1, csp, so_node_mo_rong, do_sau_toi_da, duong_di, thong_tin_buoc)
                if ket_qua:
                    return ket_qua
            del gan_gia_tri[bien]
            thong_tin_buoc.append(f"Backtrack: Xóa {gt} tại {bien}")
            duong_di.append(chupLuoi(gan_gia_tri))

        return None

    def capNhatBanBacktracking(self, trang_thai, chi_so_buoc):
        for i in range(3):
            for j in range(3):
                gia_tri = trang_thai[i][j] if trang_thai[i][j] is not None else ""
                self.o_vuong_backtracking[i][j].config(text=str(gia_tri), bg="#ffffff")

        trang_thai_phang = [trang_thai[i][j] if trang_thai[i][j] is not None else 0 for i in range(3) for j in range(3)]
        for chi_so in range(9):
            i, j = divmod(chi_so, 3)
            if trang_thai_phang[chi_so] == 0 or (chi_so < 8 and trang_thai_phang[chi_so] != self.muc_tieu_phang[chi_so]):
                self.o_vuong_backtracking[i][j].config(bg="#fff9c4")
                break

        if chi_so_buoc < len(self.thong_tin_buoc):
            self.nhan_thong_tin_buoc.config(text=self.thong_tin_buoc[chi_so_buoc])
        else:
            self.nhan_thong_tin_buoc.config(text="Hoàn thành!")
        
        self.nhan_buoc_hien_tai.config(text=f"Bước hiện tại: {chi_so_buoc + 1}")

    def buocTiepBacktracking(self):
        if self.buoc_hien_tai < len(self.cac_buoc_backtracking):
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[self.buoc_hien_tai], self.buoc_hien_tai)
            self.buoc_hien_tai += 1
            self.nut_lui.config(state=tk.NORMAL)
            if self.buoc_hien_tai == len(self.cac_buoc_backtracking):
                self.nut_tung_buoc.config(state=tk.DISABLED)
                trang_thai_phang_cuoi = [self.cac_buoc_backtracking[-1][i][j] for i in range(3) for j in range(3) if self.cac_buoc_backtracking[-1][i][j] is not None]
                trang_thai_phang_cuoi = [0 if x is None else x for x in trang_thai_phang_cuoi] + [0] * (9 - len(trang_thai_phang_cuoi))
                if trang_thai_phang_cuoi == self.muc_tieu_phang:
                    self.nhan_thong_tin_buoc.config(text="Đã đạt mục tiêu 123456780!")
                    messagebox.showinfo("Thông báo", "Đã đạt mục tiêu 123456780!")
                else:
                    self.nhan_thong_tin_buoc.config(text="Không tìm thấy giải pháp!")
                    messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")
        else:
            self.nut_tung_buoc.config(state=tk.DISABLED)
            trang_thai_phang_cuoi = [self.cac_buoc_backtracking[-1][i][j] for i in range(3) for j in range(3) if self.cac_buoc_backtracking[-1][i][j] is not None]
            trang_thai_phang_cuoi = [0 if x is None else x for x in trang_thai_phang_cuoi] + [0] * (9 - len(trang_thai_phang_cuoi))
            if trang_thai_phang_cuoi == self.muc_tieu_phang:
                self.nhan_thong_tin_buoc.config(text="Đã đạt mục tiêu 123456780!")
                messagebox.showinfo("Thông báo", "Đã đạt mục tiêu 123456780!")
            else:
                self.nhan_thong_tin_buoc.config(text="Không tìm thấy giải pháp!")
                messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")

    def tuDongBacktracking(self):
        if not self.dang_chay_backtracking:
            self.dang_chay_backtracking = True
            self.nut_tu_dong.config(text="Tạm dừng")
            self.nut_tung_buoc.config(state=tk.DISABLED)
            self.nut_lui.config(state=tk.DISABLED)
            self.hieuUngBacktracking()
        else:
            self.dang_chay_backtracking = False
            self.nut_tu_dong.config(text="Chạy tự động")
            if self.buoc_hien_tai < len(self.cac_buoc_backtracking):
                self.nut_tung_buoc.config(state=tk.NORMAL)
            if self.buoc_hien_tai > 0:
                self.nut_lui.config(state=tk.NORMAL)

    def hieuUngBacktracking(self):
        if self.buoc_hien_tai < len(self.cac_buoc_backtracking) and self.dang_chay_backtracking:
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[self.buoc_hien_tai], self.buoc_hien_tai)
            self.buoc_hien_tai += 1
            self.cua_so.after(400, self.hieuUngBacktracking)
        elif self.dang_chay_backtracking:
            self.dang_chay_backtracking = False
            self.nut_tu_dong.config(text="Chạy tự động")
            trang_thai_phang_cuoi = [self.cac_buoc_backtracking[-1][i][j] for i in range(3) for j in range(3) if self.cac_buoc_backtracking[-1][i][j] is not None]
            trang_thai_phang_cuoi = [0 if x is None else x for x in trang_thai_phang_cuoi] + [0] * (9 - len(trang_thai_phang_cuoi))
            if trang_thai_phang_cuoi == self.muc_tieu_phang:
                self.nhan_thong_tin_buoc.config(text="Đã đạt mục tiêu 123456780!")
                messagebox.showinfo("Thông báo", "Đã đạt mục tiêu 123456780!")
            else:
                self.nhan_thong_tin_buoc.config(text="Không tìm thấy giải pháp!")
                messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")
            if self.buoc_hien_tai > 0:
                self.nut_lui.config(state=tk.NORMAL)
            self.nut_dat_lai.config(state=tk.NORMAL)

    def luiBuocBacktracking(self):
        if self.buoc_hien_tai > 0:
            self.buoc_hien_tai -= 1
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[self.buoc_hien_tai], self.buoc_hien_tai)
            if self.buoc_hien_tai < len(self.cac_buoc_backtracking) - 1:
                self.nut_tung_buoc.config(state=tk.NORMAL)
            if self.buoc_hien_tai == 0:
                self.nut_lui.config(state=tk.DISABLED)
    
    def datLaiBacktracking(self):
        if self.cac_buoc_backtracking:
            self.buoc_hien_tai = 0
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[0], 0)
            self.nut_tung_buoc.config(state=tk.NORMAL)
            self.nut_lui.config(state=tk.DISABLED)
            self.nut_tu_dong.config(state=tk.NORMAL)
            self.dang_chay_backtracking = False
            self.nut_tu_dong.config(text="Chạy tự động")

    def chayBacktrack(self):
        trang_thai_ban_dau = [[None for _ in range(3)] for _ in range(3)]
        self.cac_buoc_backtracking = []
        self.thong_tin_buoc = []
        self.buoc_hien_tai = 0
        self.nhan_thong_tin_buoc.config(text="Đang chạy Backtracking (không ràng buộc cố định)...")
        self.nhan_so_buoc.config(text="Tổng số bước: 0")
        self.nhan_buoc_hien_tai.config(text="Bước hiện tại: 0")

        ket_qua = self.giai(trang_thai_ban_dau)
        if ket_qua['giai_phap']:
            self.cac_buoc_backtracking = ket_qua['duong_di']
            self.capNhatBanBacktracking(self.cac_buoc_backtracking[0], 0)
            self.nut_tung_buoc.config(state=tk.NORMAL)
            self.nut_tu_dong.config(state=tk.NORMAL)
            self.nut_dat_lai.config(state=tk.NORMAL)
            self.nut_lui.config(state=tk.DISABLED)
            self.nhan_thong_tin_buoc.config(text=f"Backtracking: Tìm thấy giải pháp! Nodes: {ket_qua['so_node_mo_rong']}, Độ sâu tối đa: {ket_qua['do_sau_toi_da']}")
            self.nhan_so_buoc.config(text=f"Tổng số bước: {len(ket_qua['duong_di'])}")
            messagebox.showinfo("Thông báo", f"Backtracking: Tìm thấy giải pháp sau {ket_qua['so_node_mo_rong']} nodes!")
        else:
            self.nhan_thong_tin_buoc.config(text="Backtracking: Không tìm thấy giải pháp!")
            self.nhan_so_buoc.config(text="Tổng số bước: 0")
            messagebox.showinfo("Thông báo", "Backtracking: Không tìm thấy giải pháp!")