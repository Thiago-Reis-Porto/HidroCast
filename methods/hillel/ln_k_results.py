import numpy as np
import pandas as pd
from plots import plot_ajuste_2, set_image_visualization, set_result_visualization
from scipy.optimize import curve_fit
from utils import reta


def ln_k_curve_fit(data):
    depths = data["DEPTHS"]
    THETA = data["THETAS TIME"]
    LNK = data["LNK"]
    p_lnk = np.zeros(shape=(depths.size, 2))
    for i, j in enumerate(depths):
        p_lnk[i], _ = curve_fit(reta, THETA[j], LNK[j])
    data["PARAMS LNK"] = p_lnk


def pipeline_lnk_result(frame, data, **f_pos):
    ln_k_curve_fit(data)
    DEPTHS = data["DEPTHS"]
    p_lnk = data["PARAMS LNK"]
    titles = [f'{DEPTHS[i]} y= {p[0]:.3f} *x + {p[1]:.3f}' for i,
              p in enumerate(p_lnk)]
    THETA = data["THETA"]
    LNK = data["LNK"]
    
    r2, fig = plot_ajuste_2(THETA,
                            LNK,
                            reta,
                            p_lnk,
                            titles,
                            suptitle='$ln(k)$  curve fit for every depth:',
                            xlabel=r'$\theta$',
                            ylabel=r'$\ln(k)$',
                            shape=(10, 3),
                            figsize=(20, 35),
                            fit_name="lnk_curve_fit",
                            r2_return=True)
                            
    set_image_visualization(frame, fig, **f_pos)

    T0 = data["THETA 0"].values

    def f_eqc_1(i): 
        return f'$ln(k) = {p_lnk[i][0]:.3f}θ {p_lnk[i][1]:.3f}$, r2: {np.round(r2[i], 3)}'

    equacao = [f_eqc_1(i) for i, _ in enumerate(DEPTHS)]
    lnk0 = np.array([reta(T0[i], *p_lnk[i]) for i, j in enumerate(DEPTHS)])

    k0 = np.e**lnk0

    def f_eqc_2(i, j): 
        return f'$K(θ) = {k0[i]:.3f}e^{{{p_lnk[i][0]:.3f}(θ - {T0[i]:.3f})}}$'

    equacaok = [f_eqc_2(i, j) for i, j in enumerate(DEPTHS)]
    dados = np.column_stack((DEPTHS, equacao, T0, np.round(
        lnk0, 3), np.round(k0, 3), equacaok))

    units = [r'$\mathbf{cm}$',
             r'$\mathbf{cm / days}$',
             r'$\mathbf{cm^3.cm^{-3}}$',
             r'$\mathbf{cm / days}$',
             r'$\mathbf{cm / days}$',
             r'$\mathbf{cm / days}$']

    dados = np.insert(dados, 0, units, 0)

    tabela_eqc = pd.DataFrame(data=dados)
    
    tabela_eqc.columns = ['z',
                          'Equação ln(K)',
                          '$\mathbf{θ_0}$',
                          'ln($\mathbf{K_0}$)',
                          '$\mathbf{K_0}$',
                          'Equação $\mathbf{K(θ)}$']

    data["EQC TABLE"] = tabela_eqc
    note = frame.master.master
    set_result_visualization(note.result_frame, data)
  