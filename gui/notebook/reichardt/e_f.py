from gui.notebook.hillel.curve_fit_tab import curve_frame
from methods.reichardt import pipeline_e_f

def set_e_f(notebook):
    try:
        if notebook.e_f_frame:
            e_f_frame = notebook.e_f_frame
            notebook.add(e_f_frame, text="e f")
            notebook.tab_list.append(e_f_frame)
    except:
        e_f_frame = curve_frame(notebook,
                                notebook.root.data,
                                pipeline_e_f,
                                lt=r"e f")
                                
        notebook.e_f_frame = e_f_frame
        notebook.add(e_f_frame, text="e f")
        notebook.tab_list.append(e_f_frame)

    return notebook