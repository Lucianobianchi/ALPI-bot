import robot_controller

CV = 20
CR = 20
BASE_VR = 0.5
DM_OFFSET = 0.0001
DT_OFFSET = 0.1

def dmean(d_l, d_r):
    return (d_l + d_r) / 2

def control_strategy(cv, base_vr, cr, dm_off, dt_off):
    def f(d_l, d_r):
        dt = d_l - d_r
        dm = dmean(d_l, d_r)

        if abs(dt) > dt_off:
            vr = base_vr + cr * (abs(dt) - dt_off)
            if d_l > d_r: # Rotate clockwise
                return (vr, -vr)
            else: # Rotate counterclockwise
                return (-vr, vr)            
        elif dm > dm_off: # Go forward
            vf = cv * (dm - dm_off)
            return (vf, vf)
        else: # Stop
            return (0, 0)

    return f

robot_controller.start(control_strategy(CV, BASE_VR, CR, DM_OFFSET, DT_OFFSET))
