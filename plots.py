import tkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from sklearn.metrics import r2_score
from VG import van_genutchen
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui.image_scroll import ScrollableImage
import os

#matplotlib.use('TkAgg')

def gen_sticks(values):
  mx = values.max()
  mn =  values.min()
  dst = mx - mn
  sticks = [mn, mn+dst/4, mn+2*dst/4, mn+3*dst/4, mx]
  return np.round(sticks,2)

def n_plots(data, y, columns, title='', xlabel='', 
            ylabel='', shape=(4,2), log=False):
  plt.style.use('fivethirtyeight')
  #plt.style.use('ggplot')
  
  fig = plt.figure(figsize=(15, 17))
  fig.suptitle(title,fontsize=20)
  for i in range(7):
      column = columns[i]
      ax_pos = shape +(1+i,)
      ax = fig.add_subplot(*ax_pos)
      ax.plot(data[column], y, 'o')
      ax.set_title(column, fontsize=15)
      ax.set_xlabel(xlabel)
      ax.set_ylabel(ylabel)
      if log: ax.set_xscale('log')
  plt.tight_layout()
  plt.subplots_adjust(top=0.93)
  return fig

def plot_ajuste(x, y_data, func, params, titles, suptitle='', xlabel='', fit_name='curve_fit',
                ylabel='', shape=(3,3), log=False, figsize=(12,9), loc='upper right'):
  plt.style.use('fivethirtyeight')
  fig = plt.figure(figsize=figsize)
  fig.suptitle(suptitle, fontsize=18)
  columns = y_data.columns
  
  for i, j in enumerate(columns):
      ajuste = func(x, *params[i])
      sticks_Y = gen_sticks(y_data[j])
      sticks_X = gen_sticks(x)
      r2 = r2_score(y_data[j], ajuste)
      pos = shape+(1+i,)
      ax = fig.add_subplot(*pos)
      ax.plot(x, ajuste)
      ax.plot(x, y_data[j], 'o', color='red')
      ax.set_title(titles[i])
      ax.set_xlabel(xlabel)#, fontsize=12)
      ax.set_ylabel(ylabel)#, fontsize=12)
      ax.set_xticks(sticks_X)
      ax.set_yticks(sticks_Y)
      at = AnchoredText(f'$R^2$: {r2:.3f}',
                        prop=dict(size=12), 
                        frameon=True, 
                        loc=loc)
      at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
      ax.add_artist(at)
      # plt.grid(False)
      # plt.gca().invert_xaxis()
      # plt.annotate(f'$R^2$: {r2:.3f}', xy=xy, xycoords='axes fraction')
  plt.tight_layout()
  plt.subplots_adjust(top=0.95)
  path = os.path.join('images', fit_name)
  plt.savefig(path, bbox_inches='tight',dpi=100)
  return path+".png"

def plot_ajuste_2(x, y_data, func, params, titles, suptitle='', xlabel='', fit_name='curve_fit', 
                ylabel='', shape=(3,3), log=False, figsize=(18,20), r2_return=False):
  plt.style.use('fivethirtyeight')
  fig = plt.figure(figsize=figsize)
  fig.suptitle(suptitle, fontsize=25)
  columns = y_data.columns
  r2_l = []
  for i, j in enumerate(columns):
      ajuste = func(x[j], *params[i])
      sticks_Y = gen_sticks(y_data[j])
      sticks_X = gen_sticks(x[j])
      r2 = r2_score(y_data[j], ajuste)
      pos = shape+(1+i,)
      ax = fig.add_subplot(*pos)
      ax.plot(x[j], ajuste)
      ax.plot(x[j], y_data[j], 'o', color='red')
      ax.set_title(titles[i])
      ax.set_xlabel(xlabel)#, fontsize=12)
      ax.set_ylabel(ylabel)#, fontsize=12)
      ax.set_xticks(sticks_X)
      ax.set_yticks(sticks_Y)
      at = AnchoredText(f'$R^2$: {r2:.3f}',
                        prop=dict(size=12), 
                        frameon=True, 
                        loc='upper left')
      at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
      ax.add_artist(at)
      r2_l.append(r2)
      # plt.grid(False)
      # plt.gca().invert_xaxis()
      # plt.annotate(f'$R^2$: {r2:.3f}', xy=xy, xycoords='axes fraction')
  plt.tight_layout()
  plt.subplots_adjust(top=0.95)
  path = os.path.join('images', fit_name)
  plt.savefig(path, bbox_inches='tight',dpi=100)
  fig = path+".png"

  if r2_return:
    return r2_l, fig

  return fig

def plot_ajuste_VG(df_params, df_theta, phi_lns=(0,500,100000)):
  """
  df_params: Data frame dos parametros de ajuste 
  df_theta: Data frame com os thetas
  phi_lns: - atributos do phi linspace
  """
  phitest = np.linspace(*phi_lns)
  fig = plt.figure(figsize=[12,9])
  plt.style.use('fivethirtyeight')
  p = df_params
  profundidades = p.columns
  phi_m = df_theta.index

  for i, z in enumerate(profundidades):
      ajuste = van_genutchen(p[z].loc['Theta_r'], 
                                    p[z].loc['alpha'],
                                    p[z].loc['n'],
                                    p[z].loc['Theta_s'],
                                    phitest)
      ax = fig.add_subplot(331+i)
      ax.plot(phitest, ajuste)
      ax.plot(phi_m, df_theta[z], 'ro')
      ax.set_xscale('log')
      ax.set_title(z)
      ax.set_xlabel(r'ln $\phi_m$')
      ax.set_ylabel(r'$\theta(m^3)$')

  plt.tight_layout()
  plt.subplots_adjust(hspace=0.6,)
  path = os.path.join('images','VG_curves')
  plt.savefig(path)
  return path+".png"

def set_image_visualization(master, path, **grid_pos):
  img = tkinter.PhotoImage(file=path)
  image_window = ScrollableImage(master, image=img, scrollbarwidth=6, 
                               )
  image_window.grid(grid_pos)
  master.image_viz.grid_forget()
  master.image_viz.destroy()
  master.image_viz = image_window

def plot_result(data, fig_size=(9.7, 6.7), bigger_font=False):
  tabela_eqc = data["EQC TABLE"]
  fig, ax = plt.subplots(figsize=fig_size)
  fs = 10
  if bigger_font:
    fs = 15
  table = ax.table(cellText=tabela_eqc.values,
            # rowLabels=tabela_eqc.index,
            colLabels=tabela_eqc.columns,
            bbox=[0,0,1,1],
            cellLoc='center',
            rowLoc='center',)

  #table.auto_set_font_size(True)
  table.set_fontsize(fs)
  table.auto_set_column_width(col=list(range(tabela_eqc.columns.size)))
  #plt.rc('text', usetex=True)
  from matplotlib.font_manager import FontProperties

  for (row, col), cell in table.get_celld().items():
    if (row == 0) or (col == -1):
      cell.set_text_props(fontproperties=FontProperties(weight='bold', size=fs))

  ax.axis('off')
  ax.axis("tight")

  path = os.path.join('images','result')
  plt.savefig(path, bbox_inches="tight")
  return path+".png"

def set_result_visualization(frame, data, bigger_font=False):
  for widget in frame.winfo_children():
    widget.destroy()
  path = plot_result(data, bigger_font=bigger_font)
  img = tkinter.PhotoImage(file=path)
  image_window = ScrollableImage(frame, image=img, scrollbarwidth=6)
  image_window.pack(fill="both", expand=True)#fill="both", expand=True )
  #fill="both", expand=True, padx=20, pady=2