import time
from collections import deque
from algorithms.common import goalTest, getChildren, getStringRepresentation

class BeliefStateSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.actions = []  

    def apply_action(self, tap_niem_tin, hanh_dong):
        """Áp dụng một hành động cho tất cả trạng thái trong belief state"""
        tap_niem_tin_moi = set()
        ban_do_hanh_dong = {
            "up": lambda trang_thai: self.move(trang_thai, -3),
            "down": lambda trang_thai: self.move(trang_thai, 3),
            "left": lambda trang_thai: self.move(trang_thai, -1),
            "right": lambda trang_thai: self.move(trang_thai, 1)
        }
        ham_move = ban_do_hanh_dong[hanh_dong]

        for trang_thai in tap_niem_tin:
            trang_thai_moi = ham_move(trang_thai)
            if trang_thai_moi is not None:
                tap_niem_tin_moi.add(trang_thai_moi)
        return tap_niem_tin_moi

    def move(self, trang_thai, buoc):
        """Thực hiện di chuyển ô trống"""
        trang_thai_str = getStringRepresentation(trang_thai)
        vi_tri_0 = trang_thai_str.index('0')
        vi_tri_moi = vi_tri_0 + buoc

        if buoc == -3 and vi_tri_0 >= 3: 
            trang_thai_moi = list(trang_thai_str)
            trang_thai_moi[vi_tri_0], trang_thai_moi[vi_tri_moi] = trang_thai_moi[vi_tri_moi], trang_thai_moi[vi_tri_0]
            return int(''.join(trang_thai_moi))
        elif buoc == 3 and vi_tri_0 <= 5:  
            trang_thai_moi = list(trang_thai_str)
            trang_thai_moi[vi_tri_0], trang_thai_moi[vi_tri_moi] = trang_thai_moi[vi_tri_moi], trang_thai_moi[vi_tri_0]
            return int(''.join(trang_thai_moi))
        elif buoc == -1 and vi_tri_0 % 3 > 0:  
            trang_thai_moi = list(trang_thai_str)
            trang_thai_moi[vi_tri_0], trang_thai_moi[vi_tri_moi] = trang_thai_moi[vi_tri_moi], trang_thai_moi[vi_tri_0]
            return int(''.join(trang_thai_moi))
        elif buoc == 1 and vi_tri_0 % 3 < 2:  
            trang_thai_moi = list(trang_thai_str)
            trang_thai_moi[vi_tri_0], trang_thai_moi[vi_tri_moi] = trang_thai_moi[vi_tri_moi], trang_thai_moi[vi_tri_0]
            return int(''.join(trang_thai_moi))
        return None  

    def BeliefStateSearch(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.time()
        trang_thai_khoi_tao = int(trang_thai_dau_vao)
        tap_niem_tin = {trang_thai_khoi_tao}
        hang_doi = deque([(tap_niem_tin, [])])
        tap_da_tham = set()  
        trang_thai_toi_duong_di = {trang_thai_khoi_tao: [trang_thai_khoi_tao]}  

        while hang_doi:
            self.counter += 1
            tap_niem_tin_hien_tai, cac_hanh_dong = hang_doi.popleft()
            tap_niem_tin_tuple = tuple(sorted(tap_niem_tin_hien_tai))
            if tap_niem_tin_tuple in tap_da_tham:
                continue
            tap_da_tham.add(tap_niem_tin_tuple)
            tat_ca_la_dich = all(goalTest(trang_thai) for trang_thai in tap_niem_tin_hien_tai)
            if tat_ca_la_dich:
                trang_thai = trang_thai_khoi_tao
                self.path = [trang_thai]
                for hanh_dong in cac_hanh_dong:
                    tap_niem_tin_moi = self.apply_action({trang_thai}, hanh_dong)
                    trang_thai = next(iter(tap_niem_tin_moi))  
                    self.path.append(trang_thai)
                self.actions = cac_hanh_dong
                self.cost = len(self.path) - 1
                self.depth = self.cost
                self.time_taken = float(time.time() - thoi_gian_bat_dau)
                return self.path, self.cost, self.counter, self.depth, self.time_taken
            for hanh_dong in ["up", "down", "left", "right"]:
                tap_niem_tin_moi = self.apply_action(tap_niem_tin_hien_tai, hanh_dong)
                if tap_niem_tin_moi:  
                    hang_doi.append((tap_niem_tin_moi, cac_hanh_dong + [hanh_dong]))

        self.path = []
        self.actions = []       
        self.cost = 0
        self.depth = 0
        self.time_taken = float(time.time() - thoi_gian_bat_dau)
        return self.path, self.cost, self.counter, self.depth, self.time_taken