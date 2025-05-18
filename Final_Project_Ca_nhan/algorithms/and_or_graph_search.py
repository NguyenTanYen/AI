import time
from algorithms.common import goalTest, getStringRepresentation
from algorithms.q_learning import manhattanDistance

dx = [-1, 1, 0, 0]  
dy = [0, 0, -1, 1]
ten_hanh_dong = ["0", "1", "2", "3"]  

def kiemTraHopLe(i, j):
    return 0 <= i < 3 and 0 <= j < 3

def sinhTrangThaiCon(trang_thai):
    cac_con = {}
    vi_tri_0 = trang_thai.index("0")
    hang, cot = divmod(vi_tri_0, 3)
    for x in range(4):
        nx = hang + dx[x]
        ny = cot + dy[x]
        if kiemTraHopLe(nx, ny):
            vi_tri_moi = int(nx * 3 + ny)
            tam = list(trang_thai)
            tam[vi_tri_0], tam[vi_tri_moi] = tam[vi_tri_moi], tam[vi_tri_0]
            trang_thai_con = "".join(tam)
            cac_con[ten_hanh_dong[x]] = trang_thai_con
    return cac_con

class AndOrGraphSearchAlgorithm:
    def __init__(self):
        self.dem = 0       
        self.duong_di = []         
        self.chi_phi = 0         
        self.do_sau = 0         
        self.thoi_gian = 0    
        self.kich_thuoc_bo_nho = 0   

    def _string_to_2d(self, chuoi_trang_thai):
        nums = [int(c) for c in chuoi_trang_thai]
        return [nums[i:i+3] for i in range(0, 9, 3)]

    def _2d_to_string(self, trang_thai_2d):
        return ''.join(str(num) for row in trang_thai_2d for num in row)

    def _2d_to_int(self, trang_thai_2d):
        return int(self._2d_to_string(trang_thai_2d))

    def AndOrGraphSearch(self, trang_thai_dau_vao, trang_thai_dich):
        thoi_gian_bat_dau = time.perf_counter()
        self.dem = 0
        self.duong_di = []
        self.chi_phi = 0
        self.do_sau = 0
        self.kich_thuoc_bo_nho = 0
        do_sau_de_quy_max = 0

        trang_thai_khoi_tao = getStringRepresentation(trang_thai_dau_vao)
        trang_thai_muc_tieu = getStringRepresentation(trang_thai_dich)
        tap_trang_thai_da_tham = set()

        def or_search(trang_thai, duong_di_hien_tai, do_sau_de_quy=0):
            nonlocal do_sau_de_quy_max
            self.dem += 1
            do_sau_de_quy_max = max(do_sau_de_quy_max, do_sau_de_quy)

            if goalTest(int(trang_thai)):
                kich_thuoc_bo_nho = (len(tap_trang_thai_da_tham) * 8) + (do_sau_de_quy_max * 16)
                return [], self.dem, kich_thuoc_bo_nho
            if trang_thai in duong_di_hien_tai:
                kich_thuoc_bo_nho = (len(tap_trang_thai_da_tham) * 8) + (do_sau_de_quy_max * 16)
                return None, self.dem, kich_thuoc_bo_nho

            tap_trang_thai_da_tham.add(trang_thai)
            cac_con = sinhTrangThaiCon(trang_thai)
            cac_trang_thai_di_chuyen = [(manhattanDistance(int(trang_thai_con)), hanh_dong) for hanh_dong, trang_thai_con in cac_con.items()]
            cac_trang_thai_di_chuyen.sort(key=lambda x: x[0])

            for _, hanh_dong in cac_trang_thai_di_chuyen:
                trang_thai_moi = cac_con.get(hanh_dong, trang_thai)
                ke_hoach, dem, kich_thuoc_bo_nho = and_search(trang_thai_moi, duong_di_hien_tai + [trang_thai], do_sau_de_quy + 1)
                if ke_hoach is not None:
                    return [hanh_dong] + ke_hoach, dem, kich_thuoc_bo_nho
            kich_thuoc_bo_nho = (len(tap_trang_thai_da_tham) * 8) + (do_sau_de_quy_max * 16)
            return None, self.dem, kich_thuoc_bo_nho

        def and_search(trang_thai, duong_di_hien_tai, do_sau_de_quy):
            return or_search(trang_thai, duong_di_hien_tai, do_sau_de_quy)

        ke_hoach, so_trang_thai_tham, self.kich_thuoc_bo_nho = or_search(trang_thai_khoi_tao, [])

        if ke_hoach:
            duong_di = [trang_thai_khoi_tao]
            hien_tai = trang_thai_khoi_tao
            for hanh_dong in ke_hoach:
                hien_tai = sinhTrangThaiCon(hien_tai).get(hanh_dong, hien_tai)
                duong_di.append(hien_tai)

            self.duong_di = [int(trang_thai) for trang_thai in duong_di]
            self.chi_phi = len(ke_hoach)
            self.do_sau = len(ke_hoach)
        else:
            self.duong_di = []
            self.chi_phi = 0
            self.do_sau = 0

        self.thoi_gian = time.perf_counter() - thoi_gian_bat_dau
        return self.duong_di, self.chi_phi, self.dem, self.do_sau, self.thoi_gian, self.kich_thuoc_bo_nho
