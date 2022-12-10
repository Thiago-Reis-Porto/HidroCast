from gui.notebook.hillel.log_k import set_log_k
from gui.notebook.hillel.psi_t import set_psi_t
from gui.notebook.hillel.theta import set_theta
from gui.notebook.libard.a  import set_a
from gui.notebook.libard.AB import set_AB
from gui.notebook.reichardt.a_b import set_a_b
from gui.notebook.reichardt.c_d import set_c_d
from gui.notebook.reichardt.e_f import set_e_f
from gui.notebook.result import set_result

def forget_tabs(notebook):
    tl = notebook.tab_list
    for t in tl:
        notebook.forget(t)
    
    notebook.tab_list.clear()    

def set_method(method, notebook):

    if not notebook:
        return
    
    if notebook.actual_method == method:
        return

    forget_tabs(notebook)
    if method == "Hillel et al. (1972)":
        #notebook = set_psi_m_vg(notebook)
        notebook = set_theta(notebook)
        notebook = set_psi_t(notebook)
        notebook = set_log_k(notebook)
        notebook.actual_method = "Hillel et al. (1972)"

    elif method == "Libardi et al. (1980)":
        notebook = set_a(notebook)
        notebook = set_AB(notebook)
        notebook.actual_method = "Libardi et al. (1980)"
    
    elif method == "Reichardt et al. (2004)":
        notebook.actual_method = "Reichardt et al. (2004)"
        notebook = set_a_b(notebook)
        notebook = set_c_d(notebook)
        notebook = set_e_f(notebook)

    notebook = set_result(notebook, notebook.actual_method)
    
    return notebook
