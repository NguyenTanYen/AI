import heapq
import math
import time
import random

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

dfs_counter = 0
bfs_counter = 0
ucs_counter = 0
id_counter = 0 
bfs_best_counter = 0
astar_counter = 0
idastar_counter = 0
shc_counter = 0
sa_counter = 0
beam_counter = 0

dfs_path = []
bfs_path = []
ucs_path = []
id_path = []
bfs_best_path = []
astar_path = []
idastar_path = []
shc_path = []
sa_path = []
beam_path = []

dfs_cost = 0
bfs_cost = 0
ucs_cost = 0
id_cost = 0
bfs_best_cost = 0
astar_cost = 0
idastar_cost = 0
shc_cost = 0
sa_cost = 0
beam_cost = 0

dfs_depth = 0
bfs_depth = 0
ucs_depth = 0
id_depth = 0
bfs_best_depth = 0
astar_depth = 0
idastar_depth = 0
shc_depth = 0
sa_depth = 0
beam_depth = 0

time_bfs = 0
time_dfs = 0
time_ucs = 0
time_id = 0
time_bfs_best = 0
time_astar = 0
time_idastar = 0
time_shc = 0
time_sa = 0
time_beam = 0

def getStringRepresentation(x):
    return str(x).zfill(9)

def goalTest(trang_thai):
    return trang_thai == 123456780

def getPath(bang_cha, trang_thai_bat_dau):
    duong_di = []
    temp = 123456780
    while temp != trang_thai_bat_dau:
        duong_di.append(temp)
        temp = bang_cha[temp]
    duong_di.append(trang_thai_bat_dau)
    duong_di.reverse()
    return duong_di

def getChildren(trang_thai):
    cac_con = []
    idx = trang_thai.index("0")
    i, j = divmod(idx, 3)
    for x in range(0, 4):
        nx = i + dx[x]
        ny = j + dy[x]
        vi_tri_moi = int(nx * 3 + ny)
        if checkValid(nx, ny):
            tam = list(trang_thai)
            tam[idx], tam[vi_tri_moi] = tam[vi_tri_moi], tam[idx]
            cac_con.append("".join(tam))
    return cac_con

def checkValid(i, j):
    if i >= 3 or i < 0 or j >= 3 or j < 0:
        return 0
    return 1

def manhattanDistance(trang_thai):
    trang_thai_str = getStringRepresentation(trang_thai)
    tong_khoang_cach = 0
    for i in range(9):
        if trang_thai_str[i] != '0':
            so_hien_tai = int(trang_thai_str[i])
            dich_x, dich_y = divmod(so_hien_tai - 1, 3)
            hien_tai_x, hien_tai_y = divmod(i, 3)
            tong_khoang_cach += abs(dich_x - hien_tai_x) + abs(dich_y - hien_tai_y)
    return tong_khoang_cach

def BFS(trang_thai_dau_vao):
    thoi_gian_bat_dau = time.time()
    hang_doi = []
    tap_da_tham = set()
    bang_cha = {}
    bang_chi_phi = {}
    trang_thai_so = int(trang_thai_dau_vao)
    hang_doi.append(trang_thai_so)
    cnt = 0
    global bfs_counter, bfs_cost, bfs_depth, bfs_path, time_bfs
    bfs_cost = bfs_depth = 0
    bang_chi_phi[trang_thai_so] = 0

    while hang_doi:
        cnt += 1
        trang_thai = hang_doi.pop(0)

        if trang_thai in tap_da_tham:
            continue

        tap_da_tham.add(trang_thai)
        bfs_depth = max(bfs_depth, bang_chi_phi[trang_thai])

        if goalTest(trang_thai):
            duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
            bfs_counter = cnt
            bfs_path = duong_di
            bfs_cost = len(duong_di) - 1
            time_bfs = float(time.time() - thoi_gian_bat_dau)
            return True

        cac_con = getChildren(getStringRepresentation(trang_thai))
        for con in cac_con:
            con_so = int(con)
            if con_so not in tap_da_tham:
                hang_doi.append(con_so)
                bang_cha[con_so] = trang_thai
                bang_chi_phi[con_so] = 1 + bang_chi_phi[trang_thai]

    bfs_path = []
    bfs_cost = 0
    bfs_counter = cnt
    time_bfs = float(time.time() - thoi_gian_bat_dau)
    return False

def DFS(trang_thai_dau_vao):
    thoi_gian_bat_dau = time.time()
    ngan_xep = []
    tap_da_tham = set()
    bang_cha = {}
    bang_chi_phi = {}
    trang_thai_so = int(trang_thai_dau_vao)
    ngan_xep.append(trang_thai_so)
    cnt = 0
    global dfs_counter, dfs_cost, dfs_depth, dfs_path, time_dfs
    dfs_cost = dfs_depth = 0
    bang_chi_phi[trang_thai_so] = 0

    while ngan_xep:
        cnt += 1
        trang_thai = ngan_xep.pop()
        if trang_thai not in tap_da_tham:
            tap_da_tham.add(trang_thai)
            dfs_depth = max(dfs_depth, bang_chi_phi[trang_thai])

            if goalTest(trang_thai):
                duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
                dfs_counter = cnt
                dfs_path = duong_di
                dfs_cost = len(duong_di) - 1
                time_dfs = float(time.time() - thoi_gian_bat_dau)
                return True

            cac_con = getChildren(getStringRepresentation(trang_thai))
            for con in cac_con:
                con_so = int(con)
                if con_so not in tap_da_tham:
                    ngan_xep.append(con_so)
                    bang_cha[con_so] = trang_thai
                    bang_chi_phi[con_so] = 1 + bang_chi_phi[trang_thai]

    dfs_path = []
    dfs_cost = 0
    dfs_counter = cnt
    time_dfs = float(time.time() - thoi_gian_bat_dau)
    return False

def UCS(trang_thai_dau_vao):
    thoi_gian_bat_dau = time.time()
    hang_doi_uu_tien = []
    tap_da_tham = set()
    bang_cha = {}
    bang_chi_phi = {}
    trang_thai_so = int(trang_thai_dau_vao)
    heapq.heappush(hang_doi_uu_tien, (0, trang_thai_so))
    cnt = 0
    global ucs_counter, ucs_cost, ucs_depth, ucs_path, time_ucs
    ucs_cost = ucs_depth = 0
    bang_chi_phi[trang_thai_so] = 0

    while hang_doi_uu_tien:
        cnt += 1
        chi_phi_hien_tai, trang_thai = heapq.heappop(hang_doi_uu_tien)
        if trang_thai not in tap_da_tham:
            tap_da_tham.add(trang_thai)
            ucs_depth = max(ucs_depth, chi_phi_hien_tai)

            if goalTest(trang_thai):
                duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
                ucs_counter = cnt
                ucs_path = duong_di
                ucs_cost = len(duong_di) - 1
                time_ucs = float(time.time() - thoi_gian_bat_dau)
                return True

            cac_con = getChildren(getStringRepresentation(trang_thai))
            for con in cac_con:
                con_so = int(con)
                if con_so not in tap_da_tham:
                    chi_phi_moi = chi_phi_hien_tai + 1
                    heapq.heappush(hang_doi_uu_tien, (chi_phi_moi, con_so))
                    bang_cha[con_so] = trang_thai
                    bang_chi_phi[con_so] = chi_phi_moi

    ucs_path = []
    ucs_cost = 0
    ucs_counter = cnt
    time_ucs = float(time.time() - thoi_gian_bat_dau)
    return False

def IDS(trang_thai_dau_vao):
    thoi_gian_bat_dau = time.time()
    trang_thai_so = int(trang_thai_dau_vao)
    global id_counter, id_cost, id_depth, id_path, time_id
    id_counter = 0
    id_cost = 0
    id_path = []
    id_depth = 0

    def tim_kiem_gioi_han_do_sau(trang_thai, gioi_han_do_sau, tap_da_tham, bang_cha, bang_chi_phi):
        nonlocal cnt
        cnt += 1
        if goalTest(trang_thai):
            return True, getPath(bang_cha, trang_thai_so)
        if bang_chi_phi[trang_thai] >= gioi_han_do_sau:
            return False, []
        cac_con = getChildren(getStringRepresentation(trang_thai))
        for con in cac_con:
            con_so = int(con)
            if con_so not in tap_da_tham:
                tap_da_tham.add(con_so)
                bang_cha[con_so] = trang_thai
                bang_chi_phi[con_so] = bang_chi_phi[trang_thai] + 1
                tim_thay, duong_di = tim_kiem_gioi_han_do_sau(
                    con_so, gioi_han_do_sau, tap_da_tham, bang_cha, bang_chi_phi
                )
                if tim_thay:
                    return True, duong_di
        return False, []

    cnt = 0
    gioi_han_do_sau = 0
    while True:
        tap_da_tham = set()
        bang_cha = {}
        bang_chi_phi = {}
        bang_chi_phi[trang_thai_so] = 0
        tap_da_tham.add(trang_thai_so)
        tim_thay, duong_di = tim_kiem_gioi_han_do_sau(
            trang_thai_so, gioi_han_do_sau, tap_da_tham, bang_cha, bang_chi_phi
        )
        if tim_thay:
            id_counter = cnt
            id_path = duong_di
            id_cost = len(duong_di) - 1
            id_depth = max(id_depth, len(duong_di) - 1)
            time_id = time.time() - thoi_gian_bat_dau
            return True
        gioi_han_do_sau += 1

def BestFirstSearch(trang_thai_dau_vao):
    thoi_gian_bat_dau = time.time()
    hang_doi_uu_tien = []
    tap_da_tham = set()
    bang_cha = {}
    bang_chi_phi = {}
    trang_thai_so = int(trang_thai_dau_vao)
    bang_chi_phi[trang_thai_so] = 0
    chi_phi_manhattan = manhattanDistance(trang_thai_so)
    heapq.heappush(hang_doi_uu_tien, (chi_phi_manhattan, trang_thai_so))
    cnt = 0

    global bfs_best_counter, bfs_best_cost, bfs_best_depth, bfs_best_path, time_bfs_best
    bfs_best_cost = bfs_best_depth = 0

    while hang_doi_uu_tien:
        cnt += 1
        _, trang_thai = heapq.heappop(hang_doi_uu_tien)
        if trang_thai not in tap_da_tham:
            tap_da_tham.add(trang_thai)
            bfs_best_depth = max(bfs_best_depth, bang_chi_phi[trang_thai])
            if goalTest(trang_thai):
                duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
                bfs_best_counter = cnt
                bfs_best_path = duong_di
                bfs_best_cost = len(duong_di) - 1
                time_bfs_best = float(time.time() - thoi_gian_bat_dau)
                return True
            cac_con = getChildren(getStringRepresentation(trang_thai))
            for con in cac_con:
                con_so = int(con)
                if con_so not in tap_da_tham:
                    bang_chi_phi[con_so] = bang_chi_phi[trang_thai] + 1
                    chi_phi_moi = manhattanDistance(con_so)
                    heapq.heappush(hang_doi_uu_tien, (chi_phi_moi, con_so))
                    bang_cha[con_so] = trang_thai
    bfs_best_path = []
    bfs_best_cost = 0
    bfs_best_counter = cnt
    time_bfs_best = float(time.time() - thoi_gian_bat_dau)
    return False

def AStar(trang_thai_dau_vao):
    thoi_gian_bat_dau = time.time()
    hang_doi_uu_tien = []
    tap_da_tham = {}
    bang_cha = {}
    g_cost = {}
    trang_thai_so = int(trang_thai_dau_vao)
    g_cost[trang_thai_so] = 0
    h_cost = manhattanDistance(trang_thai_so)
    f_cost = h_cost
    heapq.heappush(hang_doi_uu_tien, (f_cost, 0, trang_thai_so))
    cnt = 0

    global astar_counter, astar_cost, astar_depth, astar_path, time_astar
    astar_cost = astar_depth = 0

    while hang_doi_uu_tien:
        cnt += 1
        f_cost, curr_cost, trang_thai = heapq.heappop(hang_doi_uu_tien)

        if trang_thai in tap_da_tham and curr_cost >= tap_da_tham[trang_thai]:
            continue

        tap_da_tham[trang_thai] = curr_cost
        astar_depth = max(astar_depth, curr_cost)

        if goalTest(trang_thai):
            duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
            astar_counter = cnt
            astar_path = duong_di
            astar_cost = len(duong_di) - 1
            time_astar = float(time.time() - thoi_gian_bat_dau)
            return True

        cac_con = getChildren(getStringRepresentation(trang_thai))
        for con in cac_con:
            con_so = int(con)
            new_g_cost = curr_cost + 1
            h_cost = manhattanDistance(con_so)
            new_f_cost = new_g_cost + h_cost

            if con_so not in tap_da_tham or new_g_cost < tap_da_tham[con_so]:
                heapq.heappush(hang_doi_uu_tien, (new_f_cost, new_g_cost, con_so))
                bang_cha[con_so] = trang_thai
                g_cost[con_so] = new_g_cost
    astar_path = []
    astar_cost = 0
    astar_counter = cnt
    time_astar = float(time.time() - thoi_gian_bat_dau)
    return False

def IDAStar(trang_thai_dau_vao):
    thoi_gian_bat_dau = time.time()
    trang_thai_so = int(trang_thai_dau_vao)
    global idastar_counter, idastar_cost, idastar_depth, idastar_path, time_idastar
    idastar_counter = 0
    idastar_cost = 0
    idastar_depth = 0
    idastar_path = []

    def tim_kiem(trang_thai, chi_phi_g, gioi_han_f, bang_cha, tap_da_tham):
        nonlocal cnt, gioi_han_f_tiep_theo
        cnt += 1
        chi_phi_h = manhattanDistance(trang_thai)
        chi_phi_f = chi_phi_h + chi_phi_g

        if chi_phi_f > gioi_han_f:
            gioi_han_f_tiep_theo = min(gioi_han_f_tiep_theo, chi_phi_f)
            return False, []

        if goalTest(trang_thai):
            return True, getPath(bang_cha, int(trang_thai_dau_vao))

        cac_con = getChildren(getStringRepresentation(trang_thai))
        for con in cac_con:
            con_so = int(con)
            if con_so not in tap_da_tham:
                tap_da_tham.add(con_so)
                bang_cha[con_so] = trang_thai
                tim_thay, duong_di = tim_kiem(con_so, chi_phi_g + 1, gioi_han_f, bang_cha, tap_da_tham)
                if tim_thay:
                    return True, duong_di
        return False, []

    cnt = 0
    chi_phi_h_khoi_tao = manhattanDistance(trang_thai_so)
    gioi_han_f = chi_phi_h_khoi_tao
    while True:
        tap_da_tham = set()
        bang_cha = {}
        tap_da_tham.add(trang_thai_so)
        gioi_han_f_tiep_theo = float('inf')
        tim_thay, duong_di = tim_kiem(trang_thai_so, 0, gioi_han_f, bang_cha, tap_da_tham)

        if tim_thay:
            idastar_counter = cnt
            time_idastar = float(time.time() - thoi_gian_bat_dau)
            idastar_cost = len(duong_di) - 1
            idastar_depth = idastar_cost
            idastar_path = duong_di
            return True

        if gioi_han_f_tiep_theo == float('inf'):
            idastar_counter = cnt
            idastar_path = []
            idastar_cost = 0
            idastar_depth = 0
            time_idastar = float(time.time() - thoi_gian_bat_dau)
            return False
        gioi_han_f = gioi_han_f_tiep_theo

def SimpleHillClimbing(trang_thai_dau_vao):
    thoi_gian_bat_dau = time.time()
    trang_thai_so = int(trang_thai_dau_vao)
    global shc_counter, shc_cost, shc_depth, shc_path, time_shc
    shc_counter = 0
    shc_cost = 0
    shc_depth = 0
    shc_path = []

    trang_thai_hien_tai = trang_thai_so
    bang_cha = {}
    tap_da_tham = set()
    do_sau = 0

    while True:
        shc_counter += 1
        tap_da_tham.add(trang_thai_hien_tai)

        if goalTest(trang_thai_hien_tai):
            duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
            shc_path = duong_di
            shc_cost = len(duong_di) - 1
            shc_depth = do_sau
            time_shc = float(time.time() - thoi_gian_bat_dau)
            return True

        cac_con = getChildren(getStringRepresentation(trang_thai_hien_tai))
        con_tot_nhat = None
        heuristic_tot_nhat = manhattanDistance(trang_thai_hien_tai)

        for con in cac_con:
            con_so = int(con)
            if con_so not in tap_da_tham:
                heuristic = manhattanDistance(con_so)
                if heuristic < heuristic_tot_nhat:
                    heuristic_tot_nhat = heuristic
                    con_tot_nhat = con_so

        if con_tot_nhat is None:
            shc_path = []
            shc_cost = 0
            shc_depth = do_sau
            shc_counter = shc_counter
            time_shc = float(time.time() - thoi_gian_bat_dau)
            return False

        bang_cha[con_tot_nhat] = trang_thai_hien_tai
        trang_thai_hien_tai = con_tot_nhat
        do_sau += 1

def SimulatedAnnealing(trang_thai_dau_vao):
    thoi_gian_bat_dau = time.time()
    trang_thai_so = int(trang_thai_dau_vao)
    global sa_counter, sa_cost, sa_depth, sa_path, time_sa
    sa_counter = 0
    sa_cost = 0
    sa_depth = 0
    sa_path = []

    trang_thai_hien_tai = trang_thai_so
    trang_thai_tot_nhat = trang_thai_hien_tai
    bang_cha = {}
    tap_da_tham = set()
    nhiet_do = 1000.0
    toc_do_giam = 0.995
    nhiet_do_nho_nhat = 0.01

    heuristic_hien_tai = manhattanDistance(trang_thai_hien_tai)
    heuristic_tot_nhat = heuristic_hien_tai

    while nhiet_do > nhiet_do_nho_nhat:
        sa_counter += 1
        tap_da_tham.add(trang_thai_hien_tai)

        if goalTest(trang_thai_hien_tai):
            duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
            sa_path = duong_di
            sa_cost = len(duong_di) - 1
            sa_depth = sa_cost
            time_sa = float(time.time() - thoi_gian_bat_dau)
            return True

        cac_con = [int(con) for con in getChildren(getStringRepresentation(trang_thai_hien_tai)) if int(con) not in tap_da_tham]
        if not cac_con:
            break

        trang_thai_tiep = int(random.choice(cac_con))
        heuristic_tiep = manhattanDistance(trang_thai_tiep)
        delta_e = heuristic_tiep - heuristic_hien_tai

        if delta_e < 0 or random.random() < math.exp(-delta_e / nhiet_do):
            bang_cha[trang_thai_tiep] = trang_thai_hien_tai
            trang_thai_hien_tai = trang_thai_tiep
            heuristic_hien_tai = heuristic_tiep
            sa_depth += 1

        if heuristic_hien_tai < heuristic_tot_nhat:
            trang_thai_tot_nhat = trang_thai_hien_tai
            heuristic_tot_nhat = heuristic_hien_tai

        nhiet_do *= toc_do_giam

    if trang_thai_tot_nhat != trang_thai_so:
        trang_thai_hien_tai = trang_thai_tot_nhat
        if goalTest(trang_thai_hien_tai):
            duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
            sa_path = duong_di
            sa_cost = len(duong_di) - 1
            sa_depth = sa_cost
            time_sa = float(time.time() - thoi_gian_bat_dau)
            return True

    sa_path = []
    sa_cost = 0
    sa_depth = sa_depth
    time_sa = float(time.time() - thoi_gian_bat_dau)
    return False

def BeamSearch(trang_thai_dau_vao, beam_width=2):
    thoi_gian_bat_dau = time.time()
    trang_thai_so = int(trang_thai_dau_vao)
    global beam_counter, beam_cost, beam_depth, beam_path, time_beam
    beam_counter = 0
    beam_cost = 0
    beam_depth = 0
    beam_path = []

    hang_doi_uu_tien = [(manhattanDistance(trang_thai_so), 0, trang_thai_so)]
    tap_da_tham = set()
    bang_cha = {}
    bang_do_sau = {trang_thai_so: 0}

    while hang_doi_uu_tien:
        beam_counter += 1

        current_beam = []
        for _ in range(min(len(hang_doi_uu_tien), beam_width)):
            if hang_doi_uu_tien:
                h_cost, do_sau, trang_thai = heapq.heappop(hang_doi_uu_tien)
                if trang_thai not in tap_da_tham:
                    current_beam.append((h_cost, do_sau, trang_thai))

        if not current_beam:
            break

        for _, do_sau, trang_thai in current_beam:
            if trang_thai in tap_da_tham:
                continue
            tap_da_tham.add(trang_thai)
            beam_depth = max(do_sau, beam_depth)

            if goalTest(trang_thai):
                duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
                beam_path = duong_di
                beam_cost = len(duong_di) - 1
                beam_depth = beam_cost
                time_beam = float(time.time() - thoi_gian_bat_dau)
                return True

            cac_con = getChildren(getStringRepresentation(trang_thai))
            next_beam = []
            for con in cac_con:
                con_so = int(con)
                if con_so not in tap_da_tham:
                    h_cost = manhattanDistance(con_so)
                    next_beam.append((h_cost, do_sau + 1, con_so))
                    bang_cha[con_so] = trang_thai
                    bang_do_sau[con_so] = do_sau + 1

            next_beam.sort()
            for h_cost, new_depth, con_so in next_beam[:beam_width]:
                heapq.heappush(hang_doi_uu_tien, (h_cost, new_depth, con_so))
    beam_path = []
    beam_cost = 0
    time_beam = float(time.time() - thoi_gian_bat_dau)
    return False
