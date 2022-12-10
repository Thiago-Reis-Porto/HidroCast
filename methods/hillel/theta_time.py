import numpy as np
from scipy.optimize import least_squares
from utils import error_prio, get_derivative, regresLog
from plots import plot_ajuste, set_image_visualization


def curve_fit_theta(data, prio_index=0):
    # Vetor prioridade
    prio = np.ones(data["TIME"].size)
    prio[prio_index] = 5
    # prio[(TEMPO.size)//2] = 5
    # prio[-9] = 5
    # prio[-1] = 5
    DEPTHS = data["DEPTHS"]
    TEMPO = data["TIME"]

    params_log = np.zeros((DEPTHS.size, 2))
    for i, Z in enumerate(DEPTHS):
        theta = data["THETAS TIME"][Z]
        res = least_squares(error_prio, x0=[.5, .5], args=(
            TEMPO, theta, prio),)  # bounds=(0,np.inf))
        params_log[i] = res.x

    data["PARAMS LOG"] = params_log


def pipeline_theta_dtheta_pst(data):
    data["THETA"] = data["THETAS TIME"].copy()
    THETA = data["THETA"]
    time = data["TIME"]
    depths = data["DEPTHS"].to_numpy('float')
    PARAMS_LOG = data["PARAMS LOG"]
    PSI_M = data["PSI M"]

    tempo_bc = np.tile(time, depths.size).reshape(
        depths.size, time.size).transpose()
    pt = PARAMS_LOG.transpose()
    THETA[:] = pt[0]*np.log(tempo_bc) + pt[1]
    DTHETA = get_derivative(time, 'rlog', PARAMS_LOG, df_m=THETA)
    DTHETA_Z = DTHETA*data["DELTA"]

    data["Q"] = DTHETA_Z.cumsum(axis=1)
    data["PSI T"] = PSI_M + depths
    data["DTHETA"] = DTHETA
    data["DTHETA_Z"] = DTHETA_Z


def run_theta_time_pipeline(frame, data, **f_pos):
    curve_fit_theta(data)
    pipeline_theta_dtheta_pst(data)

    THETAS_TIME = data['THETAS TIME']
    DEPTHS = data['DEPTHS']
    TIME = data['TIME']
    params_log = data["PARAMS LOG"]
    titles = [
        f'{DEPTHS[i]}  y= {p[0]:.3f} *log(x) + {p[1]:.3f}' for i, p in enumerate(params_log)]

    fig = plot_ajuste(TIME,
                      THETAS_TIME,
                      regresLog,
                      params_log,
                      titles,
                      suptitle='',
                      xlabel='Time',
                      ylabel=r'$\theta(m^3)$',
                      figsize=(17, 15),
                      fit_name="theta_curve_fit")

    set_image_visualization(frame, fig, **f_pos)
