import random
def ac3(bai_toan_csp):
    hang_doi = [(bien1, bien2) for bien1 in bai_toan_csp['variables'] for bien2 in bai_toan_csp['variables'] if bien1 != bien2 and (bien1, bien2) in bai_toan_csp['constraints']]
    ac3_log = []
    mien_gia_tri = {bien: gia_tri[:] for bien, gia_tri in bai_toan_csp['domains'].items()}  # Sao chép miền
    
    while hang_doi:
        (xi, xj) = hang_doi.pop(0)
        if revise(bai_toan_csp, xi, xj, mien_gia_tri, ac3_log):
            
            if not mien_gia_tri[xi]:
                ac3_log.append(f"Domain of {xi} became empty, CSP is unsolvable.")
                return False, None, ac3_log
            for xk in [v for v in bai_toan_csp['variables'] if v != xi and v != xj and (v, xi) in bai_toan_csp['constraints']]:
                hang_doi.append((xk, xi))
    
    return True, mien_gia_tri, ac3_log
    
def revise(bai_toan_csp, xi, xj, mien_gia_tri, ac3_log):
    
    da_sua = False
    mien_xi = mien_gia_tri[xi].copy()
    for x in mien_xi:
        if not any(bai_toan_csp['constraints'][(xi, xj)](x, y) for y in mien_gia_tri[xj]):
            mien_gia_tri[xi].remove(x)
            ac3_log.append(f"Removed value {x} from domain of {xi} due to constraint with {xj}")
            da_sua = True
    return da_sua

def backtracking_with_ac3(trang_thai_ban_dau, trang_thai_dich):
    
    def chuyen_ve_dang_phang(trang_thai):
        if isinstance(trang_thai, (list, tuple)) and len(trang_thai) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in trang_thai):
            return [trang_thai[i][j] for i in range(3) for j in range(3)]
        elif isinstance(trang_thai, (list, tuple)) and len(trang_thai) == 9:
            return list(trang_thai)
        else:
            raise ValueError("State must be a 3x3 grid or a flat list/tuple with 9 elements")

    def la_day_lien_tuc(ban_co, vi_tri):
        if vi_tri == 0:
            return True
        so_lon_nhat = -1
        for i in range(vi_tri):
            hang, cot = divmod(i, 3)
            if ban_co[hang][cot] is not None:
                so_lon_nhat = max(so_lon_nhat, ban_co[hang][cot])
        if so_lon_nhat == 8:
            return ban_co[vi_tri // 3][vi_tri % 3] == 0
        return ban_co[vi_tri // 3][vi_tri % 3] == so_lon_nhat + 1

    dich_phang = chuyen_ve_dang_phang(trang_thai_dich)
    if set(dich_phang) != set(range(9)):
        raise ValueError("Goal state must contain exactly the numbers 0 to 8")

    cac_bien = [(i, j) for i in range(3) for j in range(3)]
    mien_cac_bien = {(i, j): list(range(9)) for i, j in cac_bien}
    for bien in cac_bien:
        random.shuffle(mien_cac_bien[bien])
    
    rang_buoc = {}
    for bien1 in cac_bien:
        for bien2 in cac_bien:
            if bien1 != bien2:
                rang_buoc[(bien1, bien2)] = lambda x, y: x != y
    for i in range(3):
        for j in range(3):
            if trang_thai_dich[i][j] == 0:
                bien = (i, j)
                for bien_khac in cac_bien:
                    if bien_khac != bien:
                        rang_buoc[(bien, bien_khac)] = lambda x, y, v=0: x == v
                        rang_buoc[(bien_khac, bien)] = lambda y, x, v=0: x == v
    
    bai_toan_csp = {
        'variables': cac_bien,
        'domains': mien_cac_bien,
        'constraints': rang_buoc
    }
    
    co_nhat_quan, mien_cac_bien, ac3_log = ac3(bai_toan_csp)
    if not co_nhat_quan:
        return [], 0, ac3_log

    dich = [[dich_phang[i * 3 + j] for j in range(3)] for i in range(3)]
    ban_co = [[None for _ in range(3)] for _ in range(3)]
    cac_buoc = []
    so_trang_thai_da_tham = 0

    def la_gan_hop_le(vi_tri, gia_tri):
        i, j = divmod(vi_tri, 3)
        for k in range(vi_tri):
            ki, kj = divmod(k, 3)
            if ban_co[ki][kj] == gia_tri:
                return False
        return True

    def quay_lui(vi_tri):
        nonlocal so_trang_thai_da_tham
        i, j = divmod(vi_tri, 3)
        
        if vi_tri == 9:
            if all(ban_co[i][j] == dich[i][j] for i in range(3) for j in range(3)):
                cac_buoc.append([row[:] for row in ban_co])
                return True
            return False
        
        for gia_tri in mien_cac_bien[(i, j)]:
            if not la_gan_hop_le(vi_tri, gia_tri):
                continue
            ban_co[i][j] = gia_tri
            if not la_day_lien_tuc(ban_co, vi_tri):
                ban_co[i][j] = None
                continue
            cac_buoc.append([row[:] for row in ban_co])
            so_trang_thai_da_tham += 1
            if quay_lui(vi_tri + 1):
                return True
            ban_co[i][j] = None
            cac_buoc.append([row[:] for row in ban_co])
        
        return False

    thanh_cong = quay_lui(0)
    
    if not thanh_cong:
        ac3_log.append("Backtracking failed to find a solution after AC-3.")
        return [], so_trang_thai_da_tham, ac3_log
    
    return cac_buoc, so_trang_thai_da_tham, ac3_log