import numpy as np
from scipy.optimize import curve_fit
from utils import reta, get_derivative
from plots import plot_ajuste, set_image_visualization

def psit_curve_fit(data):
    param_psi_t = np.zeros((data["TIME"].size, 2))
    
    for i in range(data["TIME"].size):
        param_psi_t[i], _ = curve_fit(reta, data["DEPTHS"].to_numpy('float'), data["PSI T"].iloc[i])
    data["PARAMS PSI T"] = param_psi_t

def pipeline_psi_t_ln_k(frame, data, **f_pos):
    
    psit_curve_fit(data)
    
    TIME = data["TIME"]
    param_psi_t = data["PARAMS PSI T"]
    DEPTHS = data["DEPTHS"].to_numpy("float")
    PSI_T = data ["PSI T"]
    titles =  [f'{TIME[i]}  y= {p[0]:.3f} *x + {p[1]:.3f}' for i,p in enumerate(param_psi_t)]
    
    fig = plot_ajuste(DEPTHS,
                PSI_T.transpose(),
                reta, 
                param_psi_t,  
                titles, 
                suptitle='Ajuste de  $Ψ_t$  em função de $t$ para cada profundidade:', 
                xlabel='Z(m)', 
                ylabel=r'$\Psi_t$',
                shape=(10,3),
                figsize=(15, 32),
                loc='upper left',
                fit_name='psi_t_curve_fit'
                )

    set_image_visualization(frame, fig, **f_pos)

    DPSI_T = get_derivative(DEPTHS, 'reta', param_psi_t, df_m=data["THETA"])
    data["DPSI_T"] = DPSI_T

    K = data["Q"]/DPSI_T
    K = K.astype('float')
    data["K"] = K

    data["LNK"] = np.log(K)

    