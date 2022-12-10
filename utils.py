from tkinter import filedialog
from tkinter import messagebox
import re 
import os
import tkinter
import pandas as pd
import sympy as sy
import numpy as np
from gui.image_scroll import ScrollableImage

data = {"TENSIOMETER": None,
        "THETAS PHI": None,
        "PSI M": None,
        "THETAS TIME": None,
        "DEPTHS": None,
        "TIME": None,
        "DELTA": None,
        "THETA S": None,
        "THETA 0": None,
        "THETA_MEDIAN": None}


def only_numbers(char):
    return char.isdigit()


# Function for opening the
# file explorer window

def browse_files(label, data_dic, key):
    filename = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), "inputs"),
                                          title="Select a File",
                                          filetypes=(("Sheet files",
                                                      "*.csv* *.ots* *.xlsx* *.xls*"),
                                                     ("all files",
                                                      "*.*")))
                                        
    if filename:
        try:
            name = re.split(r'/+|\\+', filename)[-1]   
            if name[-4:] == ".csv":
                data_dic[key] = pd.read_csv(filename, sep=',|;', engine='python')
                df = data_dic[key]
                if df.columns.size > 1: 
                    df.set_index(df.columns[0], inplace=True) 
            else:
                data_dic[key] = pd.read_excel(filename)
                df = data_dic[key]
                if df.columns.size > 1: 
                    df.set_index(df.columns[0], inplace=True)
            label.configure(text="File Opened: "+name)
        except:
           messagebox.showerror("FILE ERROR", "Invalid file")
   
    return data_dic

def browse_files_2(label, data_dic, key):
    filename = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), "inputs"),
                                          title="Select a File",
                                          filetypes=(("Sheet files",
                                                      "*.csv* *.ots* *.xlsx* *.xls*"),
                                                     ("all files",
                                                      "*.*")))
                                        
    if filename:
        try:
            name = re.split(r'/+|\\+', filename)[-1]   
            if name[-4:] == ".csv":
                df = pd.read_csv(filename, sep=',|;', engine='python')
                s = pd.Series(df.set_index(df.columns[0]).T.values[0])
                s.index = df[df.columns[0]]
                data_dic[key] = s
            else:
                df = pd.read_excel(filename)
                s = pd.Series(df.set_index(df.columns[0]).T.values[0])
                s.index = df[df.columns[0]]
                data_dic[key] = s
            label.configure(text="File Opened: "+name)
        except:
           messagebox.showerror("FILE ERROR", "Invalide file")
   
    return data_dic

#Regressão logaritmica
def regresLog(x, p1, p2):
    return p1*np.log(x)+p2

#Regressão polinomial
def poly(x, p0, p1, p2):
    return p0*x**2 + p1*x + p2

#Regressão Linear
def reta(x, p0, p1):
    return x*p0 + p1

# retorna os residuais de acordo com um vetor prioridade
def error_prio(coeffs, *args):
    xdata, ydata, prio = args
    ress = regresLog(xdata, *coeffs)-ydata
    return prio*ress

# retorna os residuais de acordo com um vetor prioridade
def error_prio_2(coeffs, *args):
    xdata, ydata, prio, func = args
    ress = func(xdata, *coeffs)-ydata
    return prio*ress

def get_theta_mean(data):
    z = data['DEPTHS']
    data['THETA_MEDIAN'] = data['THETA'].cumsum(axis=1) / range(1, z.size+1)

def get_exp_dict():
    sy.var('x p0 p1 p2', real=True)
    exp = {'reta':{}, 'rlog':{}, 'poly':{}}
    exp['reta']['e'] = x*p0 + p1
    exp['reta']['sy'] = (x, p0, p1)
    exp['rlog']['e'] = p0*sy.log(x)+p1
    exp['rlog']['sy'] = (x, p0, p1)
    exp['poly']['e'] = p0*x**2 + p1*x + p2
    exp['poly']['sy'] = (x, p0, p1, p2)
    return exp

def get_derivative(inp, exp_f, params, df_m=None):
  exp = get_exp_dict()
  f_diff = exp[exp_f]['e'].diff(x)
  symbols = exp[exp_f]['sy']
  f = sy.lambdify(symbols, f_diff, 'numpy')
  df = df_m.copy()
  p = params.transpose() 
  if inp.size > params.shape[0]:
    inp = np.tile(inp, params.shape[0]).reshape(params.shape[0], inp.size).transpose()
    df[:] = f(inp, *p)
  else:
    p = np.repeat(p, inp.size, axis=1)
    df[:] = f(inp, *p).reshape(params.shape[0], inp.size)
  return abs(df)

class conv_tempo():
  def __init__(self):
    p = ['dias', 'horas', 'mins', 'segs']
    dias, horas, mins, segs = {}, {}, {}, {}
    
    dias['horas'] = lambda x: x*24
    dias['mins'] = lambda x: dias['horas'](x)*60
    dias['segs'] = lambda x: dias['mins'](x)*60

    horas['dias'] = lambda x: x/24
    horas['mins'] = lambda x: x*60
    horas['segs'] = lambda x:horas['mins'](x)*60

    mins['horas'] = lambda x: x/60
    mins['dias'] = lambda x: mins['horas'](x)/24
    mins['segs'] = lambda x: x*60

    segs['mins'] = lambda x: x/60
    segs['horas'] = lambda x: segs['mins'](x)/60
    segs['dias'] = lambda x: segs['horas'](x)/24
    
    self.__conversor = {}
    self.__conversor['dias'] = dias
    self.__conversor['horas'] = horas
    self.__conversor['mins'] = mins
    self.__conversor['segs'] = segs
    
  def conv(self, X, from_t, to_t):
    """
    --Converte os valores de uma medida de tempo para outra--
    Aceita: Dias, Horas, Minutos e segundos
    from_t - String Origem
    to_t - String Destino

    """
    return self.__conversor[from_t][to_t](X)

##Conversão de unidade de comprimento

class conv_espaco():
  def __init__(self):
    p = ['km', 'm', 'cm', 'mm']
    km, m, cm, mm = {}, {}, {}, {}
    
    km['m'] = lambda x: x*1000
    km['cm'] = lambda x: km['m'](x)*100
    km['mm'] = lambda x: km['cm'](x)*10

    m['km'] = lambda x: x/1000
    m['cm'] = lambda x: x*100
    m['mm'] = lambda x:m['cm'](x)*10

    cm['m'] = lambda x: x/100
    cm['km'] = lambda x: cm['m'](x)/1000
    cm['mm'] = lambda x: x*10

    mm['cm'] = lambda x: x/10
    mm['m'] = lambda x: mm['cm'](x)/100
    mm['km'] = lambda x: mm['m'](x)/1000
    
    self.__conversor = {}
    self.__conversor['km'] = km
    self.__conversor['m'] = m
    self.__conversor['cm'] = cm
    self.__conversor['mm'] = mm
    
  def conv(self, X, from_t, to_t):
    """
    --Converte os valores de uma medida de espaço para outra--
    Aceita: Quilometros, Metros, centimetros e milimetros
    from_t - String Origem
    to_t - String Destino

    """
    return self.__conversor[from_t][to_t](X)


def get_tables_list(data):
    df_type = pd.core.frame.DataFrame
    l = []
    for key in data.keys():
        if type(data[key]) == df_type:
            l.append(key)
    return l