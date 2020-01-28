import robot_controller

CV = 15
CA = 10
D_OFFSET = 0.0001

def dmean(d_l, d_r):
    return (d_l + d_r) / 2

def control_strategy(cv, ca, doff):
    def f(d_l, d_r):
        dm = dmean(d_l, d_r)
        if dm < doff:
            return (0, 0)
        
        vtar = cv * (dm - doff)
        v_l = vtar + ca * (d_l - d_r)
        v_r = vtar - ca * (d_l - d_r)
        return (v_l, v_r)
    return f

robot_controller.start(control_strategy(CV, CA, D_OFFSET))
