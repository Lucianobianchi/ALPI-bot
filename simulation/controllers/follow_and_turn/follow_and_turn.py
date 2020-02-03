import robot_controller

CV = 15
CR = 10
D_OFFSET = 0.0001

def dmean(d_l, d_r):
    return (d_l + d_r) / 2

def control_strategy(cv, cr, doff):
    def f(d_l, d_r):
        dm = dmean(d_l, d_r)
        if dm < doff:
            return (0, 0)
        
        vtar = cv * (dm - doff)
        v_l = vtar + cr * (d_l - d_r)
        v_r = vtar - cr * (d_l - d_r)
        return (v_l, v_r)
    return f

robot_controller.start(control_strategy(CV, CR, D_OFFSET))
