import random
def backtracking_with_steps(trang_thai_ban_dau, trang_thai_dich):
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

    dich = [[dich_phang[i * 3 + j] for j in range(3)] for i in range(3)]
    ban_co = [[None for _ in range(3)] for _ in range(3)]
    cac_buoc = []
    so_trang_thai_da_tham = 0


    def quay_lui(vi_tri, cac_so_con_lai):
        nonlocal so_trang_thai_da_tham
        i, j = divmod(vi_tri, 3)
        
        if vi_tri == 9:
            if all(ban_co[i][j] == dich[i][j] for i in range(3) for j in range(3)):
                cac_buoc.append([row[:] for row in ban_co])
                return True
            return False
        
        for idx, so in enumerate(cac_so_con_lai):
            ban_co[i][j] = so
            if not la_day_lien_tuc(ban_co, vi_tri):
                ban_co[i][j] = None
                continue
            cac_buoc.append([row[:] for row in ban_co])
            so_trang_thai_da_tham += 1
            cac_so_tiep = cac_so_con_lai[:idx] + cac_so_con_lai[idx+1:]
            if quay_lui(vi_tri + 1, cac_so_tiep):
                return True
            ban_co[i][j] = None
            cac_buoc.append([row[:] for row in ban_co])
        
        return False

    cac_so = list(range(9))
    random.shuffle(cac_so)
    thanh_cong = quay_lui(0, cac_so)
    
    if not thanh_cong:
        return [], so_trang_thai_da_tham
    
    return cac_buoc, so_trang_thai_da_tham