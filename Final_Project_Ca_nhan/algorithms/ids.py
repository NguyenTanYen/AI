import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation

class IDSAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_stack_size = 0 
        self.max_visited_size = 0 

    def IDS(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.perf_counter()
        trang_thai_so = int(trang_thai_dau_vao)
        dem = 0

        def tim_kiem_gioi_han_do_sau(trang_thai, gioi_han_do_sau, bang_cha, bang_chi_phi, ngan_xep_duong_di):
            nonlocal dem

            if bang_chi_phi[trang_thai] > gioi_han_do_sau:
                return False, []

            if goalTest(trang_thai):
                return True, getPath(bang_cha, trang_thai_so)

            ngan_xep_duong_di.append(trang_thai)
            if len(ngan_xep_duong_di) > self.max_stack_size:
                self.max_stack_size = len(ngan_xep_duong_di)
            if len(ngan_xep_duong_di) > self.max_visited_size:
                self.max_visited_size = len(ngan_xep_duong_di)

            cac_con = getChildren(getStringRepresentation(trang_thai))

            for con in cac_con:
                con_so = int(con)

                if con_so in ngan_xep_duong_di:
                    continue

                dem += 1
                bang_cha[con_so] = trang_thai
                bang_chi_phi[con_so] = bang_chi_phi[trang_thai] + 1

                tim_thay, duong_di = tim_kiem_gioi_han_do_sau(
                    con_so, gioi_han_do_sau, bang_cha, bang_chi_phi, ngan_xep_duong_di
                )

                if tim_thay:
                    return True, duong_di

            ngan_xep_duong_di.pop()
            return False, []

        gioi_han_do_sau = 0
        while True:
            bang_cha = {trang_thai_so: None}
            bang_chi_phi = {trang_thai_so: 0}
            ngan_xep_duong_di = []

            tim_thay, duong_di = tim_kiem_gioi_han_do_sau(
                trang_thai_so, gioi_han_do_sau, bang_cha, bang_chi_phi, ngan_xep_duong_di
            )

            if tim_thay:
                self.counter = dem
                self.path = duong_di
                self.cost = len(duong_di) - 1
                self.depth = len(duong_di) - 1
                self.time_taken = float(time.perf_counter() - thoi_gian_bat_dau)
                return self.path, self.cost, self.counter, self.depth, self.time_taken, self.max_stack_size + self.max_visited_size

            gioi_han_do_sau += 1
