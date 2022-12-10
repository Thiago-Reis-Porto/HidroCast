import numpy as np
from VG import *
from plots import plot_ajuste_VG
from plots import set_image_visualization

def tensio_to_psiM(H_hg, z, hc=0.2):
    tempo_s = H_hg.shape[0]
    H_it = np.tile(z, tempo_s).reshape(tempo_s, len(z))
    psi_m = -12.6*H_hg + hc + H_it
    return psi_m


def set_psiM_from_tensio(data):
    H_hg = data["TENSIOMETER"]
    DEPTHS = data["DEPTHS"]
    PSI_M = tensio_to_psiM(H_hg, DEPTHS.to_numpy('float'))
    data["PSI M"] = PSI_M.abs()
    return data


def get_VG_params_set_theta_time(data, frame, **grid_pos):
    data["PARAMETERS"] = ajuste_p_VG(data["THETAS PHI"].index, 
                     data["THETAS PHI"], 
                     data["DEPTHS"],
                     theta_s=data["THETA S"].values
                     )

    p = data["PARAMETERS"]
    PSI_M = data["PSI M"]
    data["THETAS TIME"] = pd.DataFrame(columns=data["DEPTHS"], index=data["TIME"])
    for z in data["DEPTHS"]:
        data["THETAS TIME"][z] = van_genutchen(p[z].loc['Theta_r'],
                                         p[z].loc['alpha'],
                                         p[z].loc['n'],
                                         p[z].loc['Theta_s'],
                                         PSI_M[z])

    fig = plot_ajuste_VG(data["PARAMETERS"], data["THETAS PHI"])
    set_image_visualization(frame, fig, **grid_pos)