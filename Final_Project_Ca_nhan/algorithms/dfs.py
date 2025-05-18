import time
from algorithms.common import Algorithm, goalTest, getPath, getChildren, getStringRepresentation

class DFSAlgorithm(Algorithm):
    def __init__(self):
        super().__init__()
        self.max_stack_size = 0
        self.max_visited_size = 0

    def DFS(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.perf_counter()
        ngan_xep = []
        tap_trang_thai_da_tham = set()
        bang_cha = {}
        bang_chi_phi = {}
        trang_thai_so = int(trang_thai_dau_vao)
        ngan_xep.append(trang_thai_so)
        bang_chi_phi[trang_thai_so] = 0

        while ngan_xep:
            self.counter += 1
            if len(ngan_xep) > self.max_stack_size:
                self.max_stack_size = len(ngan_xep)
            if len(tap_trang_thai_da_tham) > self.max_visited_size:
                self.max_visited_size = len(tap_trang_thai_da_tham)
            trang_thai = ngan_xep.pop()
            if trang_thai in tap_trang_thai_da_tham:
                continue
            if goalTest(trang_thai):
                self.path = getPath(bang_cha, int(trang_thai_dau_vao))
                self.cost = len(self.path) - 1
                self.depth = bang_chi_phi[trang_thai]
                self.time_taken = time.perf_counter() - thoi_gian_bat_dau
                self.memory_size = self.max_stack_size + self.max_visited_size
                return self.get_metrics()
            tap_trang_thai_da_tham.add(trang_thai)
            cac_con = getChildren(getStringRepresentation(trang_thai))
            for con in reversed(cac_con):  # Đảo ngược để giữ thứ tự giống BFS
                con_so = int(con)
                if con_so not in tap_trang_thai_da_tham:
                    ngan_xep.append(con_so)
                    bang_cha[con_so] = trang_thai
                    bang_chi_phi[con_so] = 1 + bang_chi_phi[trang_thai]
        self.time_taken = time.perf_counter() - thoi_gian_bat_dau
        self.memory_size = self.max_stack_size + self.max_visited_size
        return self.get_metrics()
