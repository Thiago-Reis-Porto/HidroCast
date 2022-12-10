from scipy.optimize import least_squares
import pandas as pd
import numpy as np


def van_genutchen(theta_r, alpha, n, theta_s, phi_m):
    m = 1 - 1/n
    den = (1 + (alpha * abs(phi_m))**n)**m

    result = theta_r + (theta_s - theta_r)/den
    return result

# Equação de VG com h isolado


def van_genutchen_h(theta, theta_r, theta_s, alpha, n):
    p = 1/n
    m = 1 - p
    T = (theta_s - theta_r)/(theta-theta_r)
    resultado = ((T**(1/m) - 1)**p) / (alpha)
    return resultado

# Equação de VG com h isolado
def van_genutchen_h_2(theta_r, alpha, n, theta_s, theta):
    p = 1/n
    m = 1 - p
    T = (theta_s - theta_r)/(theta-theta_r)
    resultado = ((T**(1/m) - 1)**p) / (alpha)
    return resultado

 # Função do Erro Residual
def erro_VG(*params, true_value):
    x0, *xl = params
    p = *x0, *xl
    residual = (true_value - van_genutchen(*p)).values
    #residual[-1] *= 5
    return residual

# Função do Erro Residual


def erro_VG_H(*params, true_value):
    x0, *xl = params
    p = *x0, *xl
    residual = (true_value - van_genutchen_h_2(*p)).values
    #residual[-1] *= 5
    #prio comes from
    return prio*residual


def ajuste_parametros_VG_ts(phi_m, theta, z, theta_s=.5, theta_r=0.1, alpha=0.1, n=1.1):
    parametros = []

    for i, j in enumerate(z):

        x0 = [theta_r, alpha, n, theta_s]
        args = (phi_m,)
        b = [-np.inf, 0, 0, 0], [np.inf, 5, np.inf, np.inf]

        res1 = least_squares(erro_VG, x0, args=args, kwargs={
                             'true_value': theta[j]},)
        parametros.append(res1.x)

    par = pd.DataFrame(parametros, columns=[
                       'Theta_r', 'alpha', 'n', 'Theta_s'], index=z)
    par = par[['Theta_s', 'Theta_r', 'alpha', 'n']]

    return par.transpose()


def ajuste_parametros_VG(phi_m, theta, z, theta_s, theta_r=0.1, alpha=0.05, n=2):
    parametros = []

    for i, j in enumerate(z):
        
        ts = theta_s[i]
        x0 = [theta_r, alpha, n]
        args = (ts, phi_m)

        res1 = least_squares(erro_VG, x0, args=args, kwargs={
                             'true_value': theta[j]})
        parametros.append(res1.x)

    par = pd.DataFrame(parametros, columns=['Theta_r', 'alpha', 'n'], index=z)
    par.insert(0, 'Theta_s', theta_s)

    return par.transpose()


def ajuste_p_VG(phi_m, df_theta, z, theta_s=.5, theta_r=0.1, alpha=0.1, n=1.1):
    
    if type(theta_s) == float:
        return ajuste_parametros_VG_ts(phi_m, 
                                        df_theta, 
                                        z,
                                        theta_s=theta_s,
                                        theta_r=theta_r,
                                        alpha=alpha,
                                        n=n)

    return ajuste_parametros_VG(phi_m, 
                                df_theta, 
                                z, 
                                theta_s,
                                theta_r=theta_r,
                                alpha=alpha,
                                n=n)


def ajuste_parametros_VG_H(theta, phi_m, z, theta_s, theta_r=0.1, alpha=0.05, n=2):
    parametros = []

    for i, j in enumerate(z):

        ts = theta_s[j]
        t = theta[j]
        x0 = [theta_r, alpha, n]
        args = (ts, t)

        res1 = least_squares(erro_VG_H, x0, args=args,
                             kwargs={'true_value': phi_m[j]})
        parametros.append(res1.x)

    par = pd.DataFrame(parametros, columns=['Theta_r', 'alpha', 'n'], index=z)
    par.insert(0, 'Theta_s', theta_s)

    return par.transpose()
