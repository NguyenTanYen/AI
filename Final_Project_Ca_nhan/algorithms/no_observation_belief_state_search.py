import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class NoObservationBeliefStateSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_pq_size = 0  
        self.max_visited_size = 0  

    def _state_to_string(self, trang_thai_2d):
        phang = [str(num) for row in trang_thai_2d for num in row]
        return ''.join(phang)

    def _string_to_2d(self, chuoi_trang_thai):
        nums = [int(c) for c in chuoi_trang_thai]
        return [nums[i:i+3] for i in range(0, 9, 3)]
    
    def get_possible_actions(self, niem_tin):
        cac_hanh_dong = set()
        for trang_thai in niem_tin:
            idx = trang_thai.index("0")
            i, j = divmod(idx, 3)
            cac_nuoc_di = [(-1, 0, "0"), (1, 0, "1"), (0, -1, "2"), (0, 1, "3")]
            for di, dj, hanh_dong in cac_nuoc_di:
                ni, nj = i + di, j + dj
                if 0 <= ni < 3 and 0 <= nj < 3:  
                    cac_hanh_dong.add(hanh_dong)
        return list(cac_hanh_dong)

    def transition(self, niem_tin, hanh_dong):
        niem_tin_tiep = set()
        for trang_thai in niem_tin:
            cac_con = getChildren(trang_thai)  
            idx = trang_thai.index("0")
            i, j = divmod(idx, 3)
            di, dj = {"0": (-1, 0), "1": (1, 0), "2": (0, -1), "3": (0, 1)}[hanh_dong]
            ni, nj = i + di, j + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                vi_tri_moi = ni * 3 + nj
                for con in cac_con:
                    if con[vi_tri_moi] == "0" and con[idx] == trang_thai[vi_tri_moi]:
                        niem_tin_tiep.add(con)
                        break
                else:
                    niem_tin_tiep.add(trang_thai)
            else:
                niem_tin_tiep.add(trang_thai)
        return niem_tin_tiep

    def NoObsBeliefStateSearch(self, niem_tin_khoi_tao, niem_tin_dich, max_iterations=1000, time_limit=10):
        thoi_gian_bat_dau = time.perf_counter()

        niem_tin_ban_dau = {self._state_to_string(trang_thai) for trang_thai in niem_tin_khoi_tao}
        niem_tin_muc_tieu = {self._state_to_string(trang_thai) for trang_thai in niem_tin_dich}

        def goal_test_belief(niem_tin):
            return set(niem_tin) == set(niem_tin_muc_tieu)

        def heuristic(niem_tin):

            tong = 0
            for trang_thai in niem_tin:
                kc_min = manhattanDistance(int(trang_thai))
                tong += kc_min
            return tong / len(niem_tin) if niem_tin else float('inf')

        if goal_test_belief(niem_tin_ban_dau):
            duong_di = [[self._string_to_2d(trang_thai) for trang_thai in niem_tin_ban_dau]]
            self.time_taken = time.perf_counter() - thoi_gian_bat_dau
            total_space = len(niem_tin_ban_dau)
            return duong_di, 0, 0, 0, self.time_taken, total_space


        hang_doi_uu_tien = []  
        tap_da_tham = set()
        dem = 0
        h_score = heuristic(niem_tin_ban_dau)
        heapq.heappush(hang_doi_uu_tien, (h_score, dem, niem_tin_ban_dau, []))
        dem += 1

        while hang_doi_uu_tien:
            self.counter += 1

            if len(hang_doi_uu_tien) > self.max_pq_size:
                self.max_pq_size = len(hang_doi_uu_tien)

            if len(tap_da_tham) > self.max_visited_size:
                self.max_visited_size = len(tap_da_tham)

            f_score, _, niem_tin, cac_hanh_dong = heapq.heappop(hang_doi_uu_tien)

            niem_tin_tuple = tuple(sorted(niem_tin))
            if niem_tin_tuple in tap_da_tham:
                continue
            tap_da_tham.add(niem_tin_tuple)

            if goal_test_belief(niem_tin):
                self.path = []
                niem_tin_hien_tai = niem_tin_ban_dau
                self.path.append([self._string_to_2d(trang_thai) for trang_thai in niem_tin_hien_tai])
                for hanh_dong in cac_hanh_dong:
                    niem_tin_hien_tai = self.transition(niem_tin_hien_tai, hanh_dong)
                    self.path.append([self._string_to_2d(trang_thai) for trang_thai in niem_tin_hien_tai])
                self.cost = len(cac_hanh_dong)
                self.depth = len(cac_hanh_dong)
                self.time_taken = time.perf_counter() - thoi_gian_bat_dau
                total_space = self.max_pq_size + self.max_visited_size
                return self.path, self.cost, self.counter, self.depth, self.time_taken, total_space

            for hanh_dong in self.get_possible_actions(niem_tin):
                niem_tin_tiep = self.transition(niem_tin, hanh_dong)
                niem_tin_tuple_tiep = tuple(sorted(niem_tin_tiep))
                if niem_tin_tuple_tiep not in tap_da_tham:
                    cac_hanh_dong_moi = cac_hanh_dong + [hanh_dong]
                    g_score = len(cac_hanh_dong_moi)
                    h_score = heuristic(niem_tin_tiep)
                    heapq.heappush(hang_doi_uu_tien, (g_score + h_score, dem, niem_tin_tiep, cac_hanh_dong_moi))
                    dem += 1

        self.time_taken = time.perf_counter() - thoi_gian_bat_dau
        total_space = self.max_pq_size + self.max_visited_size
        return [], 0, self.counter, self.depth, self.time_taken, total_space