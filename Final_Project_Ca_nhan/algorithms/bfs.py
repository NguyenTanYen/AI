import time
from collections import deque
from algorithms.common import Algorithm, goalTest, getPath, getChildren, getStringRepresentation

class BFSAlgorithm(Algorithm):
    def __init__(self):
        super().__init__()
        self.max_queue_size = 0
        self.max_visited_size = 0

    def BFS(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.perf_counter()

        hang_doi = deque()
        tap_trang_thai_da_tham = set()
        bang_cha = {}
        bang_chi_phi = {}
        trang_thai_so = int(trang_thai_dau_vao)
        hang_doi.append(trang_thai_so)
        bang_chi_phi[trang_thai_so] = 0

        while hang_doi:
            self.counter += 1

            if len(hang_doi) > self.max_queue_size:
                self.max_queue_size = len(hang_doi)

            if len(tap_trang_thai_da_tham) > self.max_visited_size:
                self.max_visited_size = len(tap_trang_thai_da_tham)
            
            trang_thai = hang_doi.popleft()

            if trang_thai in tap_trang_thai_da_tham:
                continue

            if goalTest(trang_thai):
                self.path = getPath(bang_cha, int(trang_thai_dau_vao))
                self.cost = len(self.path) - 1
                self.depth = bang_chi_phi[trang_thai]
                self.time_taken = time.perf_counter() - thoi_gian_bat_dau
                self.memory_size = self.max_queue_size + self.max_visited_size
                return self.get_metrics()
            
            tap_trang_thai_da_tham.add(trang_thai)

            cac_con = getChildren(getStringRepresentation(trang_thai))
            for con in cac_con:
                con_so = int(con)
                if con_so not in tap_trang_thai_da_tham:
                    hang_doi.append(con_so)
                    bang_cha[con_so] = trang_thai
                    bang_chi_phi[con_so] = 1 + bang_chi_phi[trang_thai]

        self.time_taken = time.perf_counter() - thoi_gian_bat_dau
        self.memory_size = self.max_queue_size + self.max_visited_size
        return self.get_metrics()
