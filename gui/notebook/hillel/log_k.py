from methods.hillel.ln_k_results import pipeline_lnk_result
from gui.notebook.hillel.curve_fit_tab import curve_frame

def set_log_k(notebook):
    try:
        if notebook.log_k_frame:
            log_k_frame = notebook.log_k_frame
            notebook.add(log_k_frame, text="Log(k) x θ")
            notebook.tab_list.append(log_k_frame)
        
    except:
        log_k_frame = curve_frame(notebook,
                                notebook.root.data,
                                pipeline_lnk_result,
                                lt="Log(k) x θ")
        notebook.log_k_frame = log_k_frame
        notebook.add(log_k_frame, text="Log(k) x θ")
        notebook.tab_list.append(log_k_frame)
        
    return notebook
