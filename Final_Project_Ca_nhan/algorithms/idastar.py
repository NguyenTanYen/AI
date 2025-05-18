import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class IDAStarAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_path_stack_size = 0 
        self.max_parent_size = 0  

    def IDAStar(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.perf_counter()  
        trang_thai_so = int(trang_thai_dau_vao)
        dem = 0

        def tim_kiem(trang_thai, chi_phi_g, gioi_han_f, bang_cha, ngan_xep_duong_di):
            nonlocal dem, gioi_han_f_tiep_theo, self
            chi_phi_h = manhattanDistance(trang_thai)
            chi_phi_f = chi_phi_h + chi_phi_g

            if len(ngan_xep_duong_di) > self.max_path_stack_size:
                self.max_path_stack_size = len(ngan_xep_duong_di)

            if len(bang_cha) > self.max_parent_size:
                self.max_parent_size = len(bang_cha)

            if chi_phi_f > gioi_han_f:
                gioi_han_f_tiep_theo = min(gioi_han_f_tiep_theo, chi_phi_f)
                return False, []
            
            if goalTest(trang_thai):
                return True, getPath(bang_cha, trang_thai_so)
            
            cac_con = getChildren(getStringRepresentation(trang_thai))
            ngan_xep_duong_di.append(trang_thai)
            for con in cac_con:
                con_so = int(con)
                if con_so in ngan_xep_duong_di:
                    continue
                
                dem += 1
                bang_cha[con_so] = trang_thai
                tim_thay, duong_di = tim_kiem(con_so, chi_phi_g + 1, gioi_han_f, bang_cha, ngan_xep_duong_di)
                if tim_thay:
                    return True, duong_di
            ngan_xep_duong_di.pop()
            return False, []

        chi_phi_h_khoi_tao = manhattanDistance(trang_thai_so)
        gioi_han_f = chi_phi_h_khoi_tao
        while True:
            bang_cha = {}
            ngan_xep_duong_di = []  # tránh lặp chu trình
            gioi_han_f_tiep_theo = float('inf')
            tim_thay, duong_di = tim_kiem(trang_thai_so, 0, gioi_han_f, bang_cha, ngan_xep_duong_di)

            if tim_thay:
                self.counter = dem
                self.path = duong_di
                self.cost = len(duong_di) - 1
                self.depth = len(duong_di) - 1
                self.time_taken = time.perf_counter() - thoi_gian_bat_dau
                total_space = self.max_path_stack_size + self.max_parent_size
                return (self.path, self.cost, self.counter, self.depth, self.time_taken, total_space)
            
            if gioi_han_f_tiep_theo == float('inf'):
                self.counter = dem
                self.time_taken = time.perf_counter() - thoi_gian_bat_dau
                total_space = self.max_path_stack_size + self.max_parent_size
                return [], 0, self.counter, self.depth, self.time_taken, total_space
            
            gioi_han_f = gioi_han_f_tiep_theo