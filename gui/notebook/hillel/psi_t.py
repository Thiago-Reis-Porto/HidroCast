from gui.notebook.hillel.curve_fit_tab import curve_frame
from methods.hillel.psi_t import pipeline_psi_t_ln_k

def set_psi_t(notebook):
    try:
        if notebook.psi_t_frame:
            psi_t_frame = notebook.psi_t_frame
            notebook.add(psi_t_frame, text="Ψt x Time")
            notebook.tab_list.append(psi_t_frame)
            
    except:
        psi_t_frame = curve_frame(notebook,
                                notebook.root.data,
                                pipeline_psi_t_ln_k,
                                lt="Ψt x Time")
                                
        notebook.psi_t_frame = psi_t_frame
        notebook.add(psi_t_frame, text="Ψt x Time")
        notebook.tab_list.append(psi_t_frame)
        
    return notebook

    