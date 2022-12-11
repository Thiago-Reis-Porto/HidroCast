import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from utils import reta, export_tables
from plots import plot_ajuste_2,plot_ajuste, set_image_visualization
from plots import set_result_visualization

def get_a_params(data):
    z = data["DEPTHS"]
    THETA = data ["THETAS TIME"]
    data["THETA_MEAN"] = THETA.cumsum(axis=1) / range(1, z.size+1)
    parametros = np.zeros(shape=(z.size, 2))
    for i, j in enumerate(z):
        parametros[i], _ = curve_fit(reta, THETA[j], data["THETA_MEAN"][j])

    data["lib_params"] = parametros

def get_A_B(data):
    # Calculo de A e B
    THETA = data["THETAS TIME"]
    z = data['DEPTHS']
    ln_time = np.log(data["TIME"])
    
    parametros_AB = np.zeros(shape=(z.size, 2))
    y = THETA.copy()
    theta_0 = data["THETA 0"]
    
    for i, j in enumerate(z):
        y[j] = (theta_0[j] - y[j])
        parametros_AB[i], _ = curve_fit(reta, ln_time, y[j])
    data['A_B'] = parametros_AB
    data['THETA_0_SUB'] = y
    data['LN_TIME'] = ln_time

def get_beta(data):
    A = data['A_B'][:, 0]
    data['Beta'] = 1/A

def get_k0(data):
    a = data['lib_params'][:, 0]
    Beta = data['Beta']
    B = data['A_B'][:, 1]
    z = data['DEPTHS']
    k0 = a * z.to_numpy('float') * np.exp(B*Beta) / Beta
    data['k0'] = k0

def pipeline_a(frame, data, **f_pos):
    get_a_params(data)
    params = data["lib_params"]
    z = data["DEPTHS"]
    THETA = data["THETAS TIME"]
    THETA_MEAN = data["THETA_MEAN"]
    titles =  [f'{z[i]}  y= {p[0]:.3f} *x + {p[1]:.3f}' for i,p in enumerate(params)]
    fig = plot_ajuste_2(THETA,
                        THETA_MEAN,
                        reta, 
                        params,  
                        titles, 
                        suptitle="Ajuste", 
                        xlabel=r"$\theta$", 
                        ylabel=r"$\bar{\theta}$",
                        shape=(10,3),
                        figsize=(15, 32),
                        fit_name="a_curve_fit")

    set_image_visualization(frame, fig, **f_pos) 

def pipeline_A_B(frame, data, **f_pos):
    get_A_B(data)
    get_beta(data)
    get_k0(data)
    ln_time = data['LN_TIME']
    params = data["A_B"]
    z = data["DEPTHS"]
    y = data['THETA_0_SUB']
    
    titles =  [f'{z[i]}  y= {p[0]:.3f} *x + {p[1]:.3f}' for i,p in enumerate(params)]
    fig = plot_ajuste(ln_time,
                        y,
                        reta, 
                        params,  
                        titles, 
                        suptitle='Ajuste ', 
                        xlabel='Z(m)', 
                        ylabel=r'$\Psi_t$',
                        shape=(10,3),
                        figsize=(15, 32),
                        fit_name='a_curve_fit')

    set_image_visualization(frame, fig, **f_pos)
    k0, Beta, theta_0 = data['k0'], data['Beta'], data['THETA 0']
    eqc = lambda x :f'$K_θ = {x[0]:.3f}*e^{{{x[1]:.3f}*(θ - {x[2]:.3f})}}$'
    result = np.apply_along_axis(eqc, 0, np.array([k0, Beta, theta_0.values]))
    
    units = [r'$\mathbf{cm}$', 
             r'$\mathbf{cm^3.cm^{-3}}$', 
             r'-', 
             r'$\mathbf{cm / day}$', 
             r'$\mathbf{cm / day}$']

    np_result = np.array([z, theta_0.values, np.round(Beta, 3), np.round(k0, 3), result])
    np_result = np.insert(np_result, 0, units, axis=1)
    result_table = pd.DataFrame(np_result.T, 
                                columns=[r'z', 
                                         r'$\mathbf{θ_0}$',
                                         r'$\mathbf{\beta}$',
                                         r'$\mathbf{K_0}$',
                                         r'Equação $\mathbf{K(θ)}$'])

    data['EQC TABLE'] = result_table

    note = frame.master.master
    set_result_visualization(note.result_frame, data)
    
    data["Result Libard"] = data["EQC TABLE"]
    data["Result Libard"].columns = ['z',
                                     'Theta 0',
                                     'Beta',
                                     'K0',
                                     'Equation K theta']

    data["Result Libard"].loc[0] =  ['cm',
                                     'cm^3*cm^(-3)',
                                     '-',
                                     'cm / day',
                                     'cm / day']
    data["EQC TABLE"] = None
    export_tables(data)                          
