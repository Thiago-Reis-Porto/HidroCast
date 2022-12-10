import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from utils import reta
from plots import plot_ajuste_2, plot_ajuste, set_image_visualization
from plots import set_result_visualization

def get_a_b(data):
    THETA = data["THETAS TIME"]
    z = data["DEPTHS"]
    ln_time = np.log(data["TIME"])
    a_b = np.zeros(shape=(z.size, 2))
    for i, j in enumerate(z):
        a_b[i], _ = curve_fit(reta, ln_time, THETA[j])

    data["LN TIME"] = ln_time
    data["a_b"] = a_b

def get_water_storage(data):
    L = data["DEPTHS"] * 10
    L_list = np.array([*enumerate(L, 1)]).T
    THETA = data["THETAS TIME"]
    WS = THETA.cumsum(axis=1)\
                .apply(lambda x: x/L_list[0] * L_list[1], axis=1)
    data["WATER STORAGE"] = WS

def get_c_d(data):
    z = data["DEPTHS"]
    c_d = np.zeros(shape=(z.size, 2))
    WS = data["WATER STORAGE"]
    ln_time = data["LN TIME"]
    for i, j in enumerate(z):
        c_d[i], _ = curve_fit(reta, ln_time, WS[j])
    
    data["c_d"] = c_d

def get_e_f(data):
    PSI_T = data["PSI M"] + data["DEPTHS"]
    PSI_T = -PSI_T
    ln_time = data["LN TIME"]
    z = data["DEPTHS"]
    e_f = np.zeros(shape=(z.size, 2))
    for i, j in enumerate(z):
        e_f[i], _ = curve_fit(reta, ln_time, PSI_T[j]) 
    data["PSI T"] = PSI_T
    data["e_f"] = e_f

def get_el_fl(data):
    e_f = data["e_f"]
    z = data["DEPTHS"]
    el_fl = np.zeros(shape=(z.size, 2))
    e = e_f.T[1]
    f = e_f.T[0]
    
    for i, j in enumerate(z[1:-1], 1):
        zl = 2*(z[i+1] - j)
        el = (e[i-1] - e[i+1])/zl
        fl = (f[i-1] - f[i+1])/zl
        el_fl[i] = [el, fl]

    el_fl[0], el_fl[-1] = [np.NaN, np.NaN]
    el_fl[0] = [None, None]

    data["el_fl"] = el_fl

def get_table(data):
    a_b = data["a_b"]
    c_d = data["c_d"]
    e_f = data["e_f"]
    el_fl  = data["el_fl"]
    z = data["DEPTHS"]

    a, b = a_b.T[1], a_b.T[0]
    c, d = c_d.T[1], c_d.T[0]
    e, f = e_f.T[1], e_f.T[0]
    el, fl  = el_fl.T[0], el_fl.T[1]
    theta_0 = data["THETA 0"]

    resumo_df = pd.DataFrame({'z(m)':z,
                     'theta 0': theta_0,
                     'a': a,
                     'b': b,
                     'c': c,
                     'd': d,
                     'e': e,
                     'f':f,
                     'e\'': el,
                     'f\'':fl})

    resumo_df.reset_index()
    return resumo_df

def get_k0(data):
    a_b = data["a_b"]
    c_d = data["c_d"]
    el_fl  = data["el_fl"]
    
    a, b = a_b.T[1], a_b.T[0]
    d = c_d.T[0]
    el, fl  = el_fl.T[0], el_fl.T[1]
    theta_0 = data["THETA 0"]
    THETA = data["THETA TIME"]
    
    t1 = -d * np.exp((a - theta_0)/b)
    t2 = np.exp(-(THETA-theta_0)/b)
    t3 = el + fl/b *(THETA - a)
    K = t1 * t2 / t3
    data["K"] = K

def get_t1_term(data):
    a_b = data["a_b"]
    c_d = data["c_d"]
    el_fl  = data["el_fl"]
    
    a, b = a_b.T[1], a_b.T[0]
    d = c_d.T[0]
    el, fl  = el_fl.T[0], el_fl.T[1]
    theta_0 = data["THETA 0"]
    
    t1 = -d * np.exp((a - theta_0)/b)

    fl_b = fl/b
    term = el + fl_b*-a
    data["t1"] = t1
    data['term'] = term
    data['fl_b'] = fl_b

def pipeline_a_b(frame, data, **f_pos):
    
    get_a_b(data)
    THETA = data["THETAS TIME"]
    a_b = data['a_b']
    ln_tempo = data["LN TIME"]
    z = data['DEPTHS']

    titles =  [f'{z[i]}cm  y= {p[0]:.3f} *x + {p[1]:.3f}' for i,p in enumerate(a_b)]

    fig = plot_ajuste(ln_tempo,
                    THETA,
                    reta, 
                    a_b,  
                    titles, 
                    suptitle="Ajuste", 
                    xlabel=r"$ln(t)$", 
                    ylabel=r"$\theta$",
                    shape=(10,3),
                    figsize=(15, 32),
                    fit_name="a_b_curve_fit")                    

    set_image_visualization(frame, fig, **f_pos) 
    
def pipeline_c_d(frame, data, **f_pos):
    get_water_storage(data)
    get_c_d(data)
    WS = data["WATER STORAGE"]
    ln_tempo = data["LN TIME"]
    c_d = data["c_d"]
    z = data['DEPTHS']

    titles =  [f'{z[i]}cm  y= {p[0]:.3f} *x + {p[1]:.3f}' for i,p in enumerate(c_d)]

    fig = plot_ajuste(ln_tempo,
                    WS,
                    reta, 
                    c_d,  
                    titles, 
                    suptitle="Ajuste", 
                    xlabel=r"$ln(t)$", 
                    ylabel=r"$\theta$",
                    shape=(10,3),
                    figsize=(15, 32),
                    fit_name="a_b_curve_fit")                    

    set_image_visualization(frame, fig, **f_pos)


def pipeline_e_f(frame, data, **f_pos):
    get_e_f(data)
    get_el_fl(data)
    #get_k0(data)
    get_t1_term(data)
    PSI_T = data["PSI T"]
    ln_tempo = data["LN TIME"]
    e_f = data["e_f"]
    z = data['DEPTHS']

    titles =  [f'{z[i]}cm  y= {p[0]:.3f} *x + {p[1]:.3f}' for i,p in enumerate(e_f)]

    fig = plot_ajuste(ln_tempo,
                    PSI_T,
                    reta, 
                    e_f,  
                    titles, 
                    suptitle="Ajuste", 
                    xlabel=r"$ln(t)$", 
                    ylabel=r"$\Psi_t$",
                    shape=(10,3),
                    figsize=(15, 32),
                    fit_name="e_f_curve_fit")                    

    set_image_visualization(frame, fig, **f_pos)
    b = data["a_b"].T[0]
    
    t1, theta_0, term, fl_b = data['t1'], data['THETA 0'], data['term'], data['fl_b']
    eqc = lambda x :fr'$K_θ = \frac{{{x[0]:.4f}*e^{{{x[1]:.4f}*(θ - {x[2]:.4f})}}}} {{{x[3]:.4f} + {x[4]:.4f}θ}}$'
    result = [eqc(x) for x in np.array([t1, -1/b, theta_0.values, term, fl_b]).T]
    result[0], result[-1] = '_','_'

    units = [r'$\mathbf{cm}$', 
         r'$\mathbf{cm^3.cm^{-3}}$', 
         r'$\mathbf{cm / days}$']
    
    np_result = np.array([z, theta_0.values, result])
    np_result = np.insert(np_result, 0, units, axis=1)

    result_table = pd.DataFrame(np_result.T, 
                            columns=[r'z', 
                                     r'$\mathbf{θ_0}$',
                                     r'Equação $\mathbf{K(θ)}$'])

    data['EQC TABLE'] = result_table
    
    note = frame.master.master
    set_result_visualization(note.result_frame, data, bigger_font=True)  