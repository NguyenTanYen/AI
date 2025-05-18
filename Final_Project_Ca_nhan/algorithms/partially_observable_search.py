import time
import heapq
import random
from collections import defaultdict
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class POMDPBeliefStateSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_pq_size = 0
        self.max_visited_size = 0
        self.observation_noise = 0.2 
        self.gamma = 0.9  

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

    def transition(self, trang_thai, hanh_dong):
        idx = trang_thai.index("0")
        i, j = divmod(idx, 3)
        di, dj = {"0": (-1, 0), "1": (1, 0), "2": (0, -1), "3": (0, 1)}[hanh_dong]
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            vi_tri_moi = ni * 3 + nj
            trang_thai_moi = list(trang_thai)
            trang_thai_moi[idx], trang_thai_moi[vi_tri_moi] = trang_thai_moi[vi_tri_moi], trang_thai_moi[idx]
            return ''.join(trang_thai_moi)
        return trang_thai

    def reward(self, trang_thai):
        return 100 if trang_thai in self.goal_belief else -1

    def observation(self, trang_thai):
        if random.random() < self.observation_noise:
            return random.choice(list(self.all_states))
        return trang_thai

    def update_belief(self, niem_tin, hanh_dong, quan_sat):
        niem_tin_moi = defaultdict(float)
        for trang_thai in niem_tin:
            trang_thai_tiep = self.transition(trang_thai, hanh_dong)
            xac_suat = niem_tin[trang_thai] * (
                (1 - self.observation_noise) if trang_thai_tiep == quan_sat 
                else self.observation_noise / (len(self.all_states) - 1)
            )
            niem_tin_moi[trang_thai_tiep] += xac_suat
        tong = sum(niem_tin_moi.values())
        if tong > 0:
            for trang_thai in niem_tin_moi:
                niem_tin_moi[trang_thai] /= tong
        return dict(niem_tin_moi)

    def heuristic(self, niem_tin):
        tong_khoang_cach = 0
        for trang_thai, xac_suat in niem_tin.items():
            kc_min = manhattanDistance(int(trang_thai))
            tong_khoang_cach += xac_suat * kc_min
        return tong_khoang_cach

    def POMDPBeliefStateSearch(self, niem_tin_khoi_tao, niem_tin_dich, max_iterations=1000, time_limit=10):
        thoi_gian_bat_dau = time.perf_counter()
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.max_pq_size = 0
        self.max_visited_size = 0

        niem_tin_ban_dau = {self._state_to_string(trang_thai): 1.0 / len(niem_tin_khoi_tao) for trang_thai in niem_tin_khoi_tao}
        self.goal_belief = {self._state_to_string(trang_thai) for trang_thai in niem_tin_dich}
        self.all_states = niem_tin_khoi_tao + niem_tin_dich

        def goal_test_belief(niem_tin):
            trang_thai_max = max(niem_tin, key=niem_tin.get)
            return trang_thai_max in self.goal_belief

        if goal_test_belief(niem_tin_ban_dau):
            duong_di = [[self._string_to_2d(trang_thai) for trang_thai in niem_tin_ban_dau]]
            self.time_taken = time.perf_counter() - thoi_gian_bat_dau
            total_space = len(niem_tin_ban_dau)
            return duong_di, 0, 0, 0, self.time_taken, total_space

        hang_doi_uu_tien = []
        tap_da_tham = set()
        dem = 0
        h_score = self.heuristic(niem_tin_ban_dau)
        heapq.heappush(hang_doi_uu_tien, (h_score, dem, niem_tin_ban_dau, []))
        dem += 1

        while hang_doi_uu_tien and time.perf_counter() - thoi_gian_bat_dau < time_limit and dem < max_iterations:
            self.counter += 1
            if len(hang_doi_uu_tien) > self.max_pq_size:
                self.max_pq_size = len(hang_doi_uu_tien)
            if len(tap_da_tham) > self.max_visited_size:
                self.max_visited_size = len(tap_da_tham)

            f_score, _, niem_tin, cac_hanh_dong = heapq.heappop(hang_doi_uu_tien)
            niem_tin_tuple = tuple(sorted(niem_tin.items()))
            if niem_tin_tuple in tap_da_tham:
                continue
            tap_da_tham.add(niem_tin_tuple)

            if goal_test_belief(niem_tin):
                self.path = []
                niem_tin_hien_tai = niem_tin_ban_dau
                self.path.append([self._string_to_2d(trang_thai) for trang_thai in niem_tin_hien_tai])
                for hanh_dong in cac_hanh_dong:
                    trang_thai_mau = max(niem_tin_hien_tai, key=niem_tin_hien_tai.get)
                    trang_thai_tiep = self.transition(trang_thai_mau, hanh_dong)
                    quan_sat = self.observation(trang_thai_tiep)
                    niem_tin_hien_tai = self.update_belief(niem_tin_hien_tai, hanh_dong, quan_sat)
                    self.path.append([self._string_to_2d(trang_thai_tiep)])
                self.cost = len(cac_hanh_dong)
                self.depth = len(cac_hanh_dong)
                self.time_taken = time.perf_counter() - thoi_gian_bat_dau
                total_space = self.max_pq_size + self.max_visited_size
                return self.path, self.cost, self.counter, self.depth, self.time_taken, total_space

            for hanh_dong in self.get_possible_actions(niem_tin):
                trang_thai_mau = max(niem_tin, key=niem_tin.get)
                trang_thai_tiep = self.transition(trang_thai_mau, hanh_dong)
                quan_sat = self.observation(trang_thai_tiep)
                niem_tin_tiep = self.update_belief(niem_tin, hanh_dong, quan_sat)
                niem_tin_tuple_tiep = tuple(sorted(niem_tin_tiep.items()))
                if niem_tin_tuple_tiep not in tap_da_tham:
                    cac_hanh_dong_moi = cac_hanh_dong + [hanh_dong]
                    g_score = len(cac_hanh_dong_moi)
                    h_score = self.heuristic(niem_tin_tiep)
                    heapq.heappush(hang_doi_uu_tien, (g_score + h_score, dem, niem_tin_tiep, cac_hanh_dong_moi))
                    dem += 1

        self.time_taken = time.perf_counter() - thoi_gian_bat_dau
        total_space = self.max_pq_size + self.max_visited_size
        return [], 0, self.counter, self.depth, self.time_taken, total_space



